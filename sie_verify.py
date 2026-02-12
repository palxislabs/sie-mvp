import argparse
import json
from pathlib import Path

from sie_lib import verify_envelope

def load_trusted_issuers(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Trusted issuer file not found: {path}")
    import json
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    p = argparse.ArgumentParser(description="Verify a .sie.json envelope (SIE v0.1).")
    p.add_argument("--file", required=True, help="Path to .sie.json file")
    p.add_argument("--pubkey", required=False, help="Public key base64 (optional if envelope includes public_key)")
    p.add_argument("--check-file", required=False, help="Path to external file to hash-check against payload.sha256")
    p.add_argument("--trusted-issuers", required=False, default="trusted_issuers.json",
    help="Path to trusted issuer keyring JSON (default: trusted_issuers.json)")

    args = p.parse_args()

    f = Path(args.file)
    if not f.exists():
        raise SystemExit(f"File not found: {f}")

    env = json.loads(f.read_text(encoding="utf-8"))

    issuer = env.get("issuer")
    if not issuer:
        raise SystemExit("Envelope missing issuer field")

    keyring = load_trusted_issuers(Path(args.trusted_issuers))

    pub = keyring.get(issuer)
    if not pub:
        print(f"[FAIL] Issuer '{issuer}' is not trusted.")
        return 2

    try:
        verify_envelope(env, pub)
        if args.check_file:
            cf = Path(args.check_file)
            if not cf.exists():
                raise SystemExit(f"Check file not found: {cf}")

            content = cf.read_text(encoding="utf-8")
            import hashlib
            disk_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            env_hash = env.get("payload", {}).get("sha256")

            if not env_hash:
                print("[FAIL] Envelope has no payload.sha256 to compare against.")
                return 2

            if disk_hash != env_hash:
                print("[FAIL] External file hash does not match signed payload.sha256 (file was modified).")
                return 2
    except ValueError as e:
        print(f"[FAIL] {e}")
        return 2

    print("[OK] Signature verified and basic checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
