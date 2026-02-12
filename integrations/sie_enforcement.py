from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EnforcementDecision:
    allowed: bool
    reason: str
    detail: str = ""


def _run_verify(verify_script: Path, envelope: Path, trusted_issuers: Path, skill_file: Path) -> tuple[bool, str]:
    cmd = [
        sys.executable,
        str(verify_script),
        "--file",
        str(envelope),
        "--trusted-issuers",
        str(trusted_issuers),
        "--check-file",
        str(skill_file),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode == 0, out


def evaluate_skill(
    skill_file: Path,
    *,
    mode: str,
    verify_script: Path,
    trusted_issuers: Path,
    envelope_suffix: str = ".sie.json",
) -> EnforcementDecision:
    if mode not in {"warn", "strict"}:
        raise ValueError("mode must be 'warn' or 'strict'")

    if not skill_file.exists():
        return EnforcementDecision(False, "skill_not_found", f"skill file not found: {skill_file}")

    envelope = Path(f"{skill_file}{envelope_suffix}")
    if not envelope.exists():
        if mode == "strict":
            return EnforcementDecision(False, "unsigned_strict", "unsigned skill rejected (strict mode)")
        return EnforcementDecision(True, "unsigned_warn", "unsigned skill allowed (warn mode)")

    ok, detail = _run_verify(verify_script, envelope, trusted_issuers, skill_file)
    if not ok:
        return EnforcementDecision(False, "verify_failed", detail)

    return EnforcementDecision(True, "verified", "signed skill verified")
