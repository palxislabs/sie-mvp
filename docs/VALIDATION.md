# VALIDATION.md — Reproducible Verification Checklist

## Purpose
Provide a deterministic command sequence to validate core SIE claims.

## Prerequisites
- Python environment available
- `pynacl` installed
- Files present: `SKILL.md`, `SKILL.md.sie.json`, `trusted_issuers.json`

## 1) Baseline verify should pass

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json
```

Expected:
- Exit code `0`
- Output contains `[OK] Signature verified and basic checks passed.`

---

## 2) File binding verify should pass

```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected:
- Exit code `0`
- Output contains `[OK] Signature verified and basic checks passed.`

---

## 3) Tamper test should fail

### 3a) Backup
```bash
cp SKILL.md SKILL.md.bak
```

### 3b) Modify file
```bash
echo "# tamper" >> SKILL.md
```

### 3c) Verify with file check
```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected:
- Non-zero exit code
- Output contains hash mismatch failure

### 3d) Restore file
```bash
mv SKILL.md.bak SKILL.md
```

---

## 4) Untrusted issuer should fail

Create temporary empty issuer map and verify:

```bash
printf '{}' > tmp_issuers.json
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers tmp_issuers.json
```

Expected:
- Non-zero exit code
- Output contains issuer-not-trusted failure

Cleanup:

```bash
rm -f tmp_issuers.json
```

---

## 5) Re-sign after legitimate edit

If `SKILL.md` changed intentionally:

```bash
python sie_sign.py --issuer palxislabs --infile SKILL.md
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

Expected:
- Verify returns `[OK]`

---

## Windows notes
- Activate env: `& .\.venv\Scripts\Activate.ps1`
- Use helper scripts:
  - `.\scripts\sign.ps1`
  - `.\scripts\verify.ps1`

## Linux/macOS notes
- Activate env: `source .venv/bin/activate`
- Use helper scripts:
  - `./scripts/sign.sh`
  - `./scripts/verify.sh`
