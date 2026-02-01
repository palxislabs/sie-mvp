import sys
from pathlib import Path
import json

# Ensure repo root is on PYTHONPATH
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


from pathlib import Path

from sie_lib import verify_envelope


def load_trusted_instructions(envelope_path: Path) -> dict:
    env = json.loads(envelope_path.read_text(encoding="utf-8"))

    issuer = env.get("issuer")
    if not issuer:
        raise SystemExit("Envelope missing issuer")

    keyring_path = REPO_ROOT / "trusted_issuers.json"
    if not keyring_path.exists():
        raise SystemExit("trusted_issuers.json not found")

    keyring = json.loads(keyring_path.read_text(encoding="utf-8"))

    pub = keyring.get(issuer)
    if not pub:
        raise SystemExit(f"Issuer '{issuer}' is not trusted")

    # Verify signature + basic checks
    verify_envelope(env, pub)

    # Optional: bind to external skill file if present
    skill_name = env.get("payload", {}).get("name")
    if skill_name and Path(skill_name).exists():
        disk_content = Path(skill_name).read_text(encoding="utf-8")
        import hashlib
        disk_hash = hashlib.sha256(disk_content.encode("utf-8")).hexdigest()
        env_hash = env.get("payload", {}).get("sha256")
        if env_hash and disk_hash != env_hash:
            raise SystemExit("External skill file was modified (hash mismatch).")

    return env


def is_prompt_disclosure_attempt(text: str) -> bool:
    # MVP-grade policy gate (simple pattern checks)
    needles = [
        "system prompt", "print your system", "reveal your prompt",
        "list all tool", "tool names", "routing logic", "how you work",
        "internal instructions", "show hidden policies", "developer message",
        "BANANA_CODE_ALPHA", "verification string"
    ]
    t = text.lower()
    return any(n.lower() in t for n in needles)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    envelope_path = repo_root / "SKILL.md.sie.json"
    email_path = repo_root / "demo" / "injected_email.txt"

    env = load_trusted_instructions(envelope_path)

    constraints = env.get("constraints", {})
    deny_disclosure = bool(constraints.get("deny_prompt_disclosure", False))

    trusted_instructions = env["payload"]["content"]
    untrusted_content = email_path.read_text(encoding="utf-8")

    print("=== TRUSTED INSTRUCTIONS (from verified envelope) ===")
    print(trusted_instructions.strip())
    print()

    print("=== UNTRUSTED CONTENT (email/document) ===")
    print(untrusted_content.strip())
    print()

    print("=== DEMO DECISION ===")
    if deny_disclosure and is_prompt_disclosure_attempt(untrusted_content):
        print("[BLOCKED] Untrusted content attempted prompt/tool disclosure or verification-token exfiltration.")
        print("Refusing those actions per signed constraints.")
    else:
        print("[ALLOW] No disclosure attempt detected (or policy not enabled).")
        print("Proceed to summarize content safely (not implemented in MVP).")

    print()
    print("=== KEY POINT ===")
    print("Untrusted content does NOT become new instructions. Only the signed envelope is trusted.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
