#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Verify envelope trust"
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json

echo "[2/4] Verify envelope + file binding"
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md

echo "[3/4] Run unit tests"
python -m unittest discover -s tests -p "test_*.py" -v

echo "[4/4] Validation complete"
