#!/usr/bin/env bash
set -euo pipefail

ISSUER="${1:-palxislabs}"
TARGET="${2:-SKILL.md}"

python sie_sign.py --issuer "$ISSUER" --infile "$TARGET"
