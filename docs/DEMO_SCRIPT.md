# DEMO_SCRIPT.md — 5-Minute Live Demo

## Goal
Show, in one short run, that trusted signed instructions pass and tampered/untrusted inputs fail.

## Setup
- Use a clean terminal in repo root
- Ensure Python deps installed (`pynacl`)

## Demo flow

### Step 1 — Baseline success
```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```
Expected: `[OK] Signature verified and basic checks passed.`

### Step 2 — Simulate tamper
```bash
cp SKILL.md SKILL.md.bak
printf "\n# tamper\n" >> SKILL.md
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```
Expected: non-zero exit and hash mismatch failure.

### Step 3 — Restore and recover
```bash
mv SKILL.md.bak SKILL.md
python sie_sign.py --issuer palxislabs --infile SKILL.md
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```
Expected: verification succeeds again.

### Step 4 — Simulate untrusted issuer
```bash
printf '{}' > tmp_issuers.json
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers tmp_issuers.json
rm -f tmp_issuers.json
```
Expected: non-zero exit and issuer-not-trusted failure.

## Talking points (non-hype)
- SIE verifies instruction authenticity and integrity before trust.
- SIE does not replace sandboxing, host hardening, or key compromise response.
- Practical value: reduce silent trust in modified/unknown skill instructions.

## Optional close
Point to:
- `docs/VALIDATION.md`
- `docs/OPERATOR_CHECKLIST.md`
- `docs/OPENCLAW_UPSTREAM_HANDOFF.md`
