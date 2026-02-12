import argparse
import sys
from pathlib import Path

# Allow running this file directly: `python integrations/openclaw_loader_sim.py ...`
# by ensuring repo root is on sys.path for `integrations.*` imports.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from integrations.sie_enforcement import evaluate_skill


def main() -> int:
    p = argparse.ArgumentParser(description="Simulate OpenClaw skill loader SIE decision branch.")
    p.add_argument("--skill", required=True, help="Path to SKILL.md")
    p.add_argument("--mode", choices=["warn", "strict"], default="warn", help="Unsigned skill behavior")
    p.add_argument("--verify-script", default="sie_verify.py", help="Path to verifier script")
    p.add_argument("--trusted-issuers", default="trusted_issuers.json", help="Path to trusted issuers keyring")
    p.add_argument("--envelope-suffix", default=".sie.json", help="Envelope suffix (default: .sie.json)")

    args = p.parse_args()

    decision = evaluate_skill(
        Path(args.skill),
        mode=args.mode,
        verify_script=Path(args.verify_script),
        trusted_issuers=Path(args.trusted_issuers),
        envelope_suffix=args.envelope_suffix,
    )

    if decision.allowed:
        print(f"ALLOW: {decision.detail}")
        return 0

    print(f"REJECT: {decision.detail}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
