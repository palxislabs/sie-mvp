from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from sie_lib import verify_envelope
from sie_policy import require_instruction_channel
from sie_registry_client import RegistryClient

@dataclass(frozen=True)
class LoadedInstruction:
    issuer: str
    envelope_id: str
    constraints: Dict[str, Any]
    scope: list[str]
    content: str


def load_keyring(keyring_path: Path) -> Dict[str, str]:
    if not keyring_path.exists():
        raise FileNotFoundError(f"Trusted issuer keyring not found: {keyring_path}")
    return json.loads(keyring_path.read_text(encoding="utf-8"))


def load_verified_instructions(
    envelope_path: Path,
    *,
    keyring_path: Path = Path("trusted_issuers.json"),
    check_file_path: Optional[Path] = None,
) -> LoadedInstruction:
    """
    Framework-agnostic instruction loader:
    - reads SIE envelope
    - enforces channel separation
    - verifies signature using trusted issuer keyring
    - optional file binding check (tamper detection)

    Intended usage:
    - frameworks call this BEFORE loading skills/policies
    - if it raises, treat instructions as untrusted and fail closed
    """
    env = json.loads(envelope_path.read_text(encoding="utf-8"))
    require_instruction_channel(env)

    issuer = env.get("issuer")
    if not issuer:
        raise ValueError("Envelope missing issuer")

    # 1) Registry presence check (objective)
    reg = RegistryClient(
        base_url="https://palxis-labs.github.io/sie-mvp",
    )
    if not reg.is_issuer_present(issuer):
        raise ValueError(f"Issuer '{issuer}' not present in registry snapshot")

    # 2) Local keyring lookup
    keyring = load_keyring(keyring_path)
    pub = keyring.get(issuer)
    if not pub:
        raise ValueError(f"Issuer '{issuer}' missing from local keyring")

    # 3) Revocation check
    if reg.is_key_revoked(issuer, pub):
        raise ValueError(f"Issuer '{issuer}' key revoked in registry")


    verify_envelope(env, pub)

    # Optional bind-to-file check
    if check_file_path:
        if not check_file_path.exists():
            raise FileNotFoundError(f"Check file not found: {check_file_path}")
        disk_content = check_file_path.read_text(encoding="utf-8")
        import hashlib
        disk_hash = hashlib.sha256(disk_content.encode("utf-8")).hexdigest()
        env_hash = env.get("payload", {}).get("sha256")
        if env_hash and disk_hash != env_hash:
            raise ValueError("External instruction file hash mismatch (tampered)")

    payload = env.get("payload", {})
    content = payload.get("content")
    if not isinstance(content, str):
        raise ValueError("Envelope payload.content missing or invalid")

    return LoadedInstruction(
        issuer=issuer,
        envelope_id=env.get("id", ""),
        constraints=env.get("constraints", {}),
        scope=env.get("scope", []),
        content=content,
    )
