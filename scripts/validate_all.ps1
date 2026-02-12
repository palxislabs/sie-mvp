Write-Host "[1/4] Verify envelope trust"
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json

Write-Host "[2/4] Verify envelope + file binding"
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md

Write-Host "[3/4] Run unit tests"
python -m unittest discover -s tests -p "test_*.py" -v

Write-Host "[4/4] Validation complete"
