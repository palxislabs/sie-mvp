from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.request import urlopen, Request

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from sie_lib import b64d


@dataclass(frozen=True)
class RegistrySnapshot:
    data: Dict[str, Any]


class RegistryClient:
    """
    MVP registry client:
    - load registry snapshot from local dir OR from a base URL
    - verify signature using pinned registry root public key
    - cache remote snapshot locally
    - provide objective queries only (no safety opinions)
    """

    def __init__(
        self,
        registry_dir: Path = Path("registry"),
        base_url: Optional[str] = None,
        cache_dir: Path = Path(".cache") / "sie_registry",
        timeout_seconds: int = 10,
    ):
        self.registry_dir = registry_dir
        self.base_url = base_url.rstrip("/") if base_url else None
        self.cache_dir = cache_dir
        self.timeout_seconds = timeout_seconds

    # ---------- Remote fetch + cache ----------

    def _fetch_text(self, url: str) -> str:
        req = Request(url, headers={"User-Agent": "sie-mvp/0.1"})
        with urlopen(req, timeout=self.timeout_seconds) as r:
            return r.read().decode("utf-8")

    def _fetch_bytes(self, url: str) -> bytes:
        req = Request(url, headers={"User-Agent": "sie-mvp/0.1"})
        with urlopen(req, timeout=self.timeout_seconds) as r:
            return r.read()

    def _remote_paths(self) -> tuple[str, str, str]:
        """
        Returns full URLs for (registry.json, registry.sig, registry_root_public_key.b64)
        """
        assert self.base_url
        return (
            f"{self.base_url}/registry/registry.json",
            f"{self.base_url}/registry/registry.sig",
            f"{self.base_url}/registry/registry_root_public_key.b64",
        )

    def refresh_cache(self) -> None:
        """
        Fetch remote registry snapshot and cache it locally.
        Cache is verified at read time; fetch just writes.
        """
        if not self.base_url:
            return

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        reg_url, sig_url, pub_url = self._remote_paths()
        reg_bytes = self._fetch_bytes(reg_url)
        sig_text = self._fetch_text(sig_url).strip()
        pub_text = self._fetch_text(pub_url).strip()

        (self.cache_dir / "registry.json").write_bytes(reg_bytes)
        (self.cache_dir / "registry.sig").write_text(sig_text, encoding="utf-8")
        (self.cache_dir / "registry_root_public_key.b64").write_text(pub_text, encoding="utf-8")

    # ---------- Load + verify ----------

    def _local_files_dir(self) -> Path:
        """
        Priority:
        - If base_url set, use cache dir (remote snapshot)
        - Else use registry_dir (repo local files)
        """
        return self.cache_dir if self.base_url else self.registry_dir

    def load_verified_snapshot(self) -> RegistrySnapshot:
        # If remote, ensure cache exists (refresh once if missing)
        d = self._local_files_dir()
        reg_path = d / "registry.json"
        sig_path = d / "registry.sig"
        pub_path = d / "registry_root_public_key.b64"

        if self.base_url and (not reg_path.exists() or not sig_path.exists() or not pub_path.exists()):
            self.refresh_cache()

        if not (reg_path.exists() and sig_path.exists() and pub_path.exists()):
            raise FileNotFoundError(f"Registry files missing in {d}")

        reg_bytes = reg_path.read_bytes()
        sig = b64d(sig_path.read_text(encoding="utf-8").strip())
        pub = b64d(pub_path.read_text(encoding="utf-8").strip())

        vk = VerifyKey(pub)
        try:
            vk.verify(reg_bytes, sig)
        except BadSignatureError as e:
            raise ValueError("Registry signature invalid") from e

        data = json.loads(reg_bytes.decode("utf-8"))
        return RegistrySnapshot(data=data)

    # ---------- Objective queries ----------

    def issuer_public_key(self, issuer_id: str) -> Optional[str]:
        snap = self.load_verified_snapshot()
        for rec in snap.data.get("records", []):
            if rec.get("type") == "issuer" and rec.get("issuer_id") == issuer_id:
                return rec.get("public_key")
        return None

    def is_issuer_present(self, issuer_id: str) -> bool:
        return self.issuer_public_key(issuer_id) is not None

    def is_key_revoked(self, issuer_id: str, public_key_b64: str) -> bool:
        snap = self.load_verified_snapshot()
        for rec in snap.data.get("records", []):
            if rec.get("type") == "revocation" and rec.get("issuer_id") == issuer_id:
                if rec.get("revoked_key") == public_key_b64:
                    return True
        return False
