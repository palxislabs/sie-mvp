#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-SKILL.md.sie.json}"
KEYRING="${2:-trusted_issuers.json}"
TARGET="${3:-SKILL.md}"

python sie_verify.py --file "$FILE" --trusted-issuers "$KEYRING" --check-file "$TARGET"
