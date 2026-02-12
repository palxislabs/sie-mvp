# FAILURE_MODES.md — Verifier Failures and Operator Actions

## Purpose
Map common SIE verification failures to clear operator actions.

## Failure Modes

## 1) Envelope file missing

**Example**
- `SKILL.md.sie.json` not found

**Typical cause**
- Unsinged skill
- Wrong envelope naming/path

**Action**
- In warn mode: allow temporarily, log warning
- In strict mode: reject skill
- Sign the skill and retry

---

## 2) Trusted issuer file missing/unreadable

**Example**
- `Trusted issuer file not found: trusted_issuers.json`

**Typical cause**
- Bad path or missing keyring
- Permission error

**Action**
- Fix keyring path/permissions
- Re-run verify
- Do not silently trust signed instructions without keyring

---

## 3) Issuer missing in envelope

**Example**
- `Envelope missing issuer field`

**Typical cause**
- Malformed envelope
- Older/non-compliant envelope format

**Action**
- Regenerate envelope with valid issuer
- Reject in strict contexts

---

## 4) Issuer not trusted

**Example**
- `[FAIL] Issuer 'X' is not trusted.`

**Typical cause**
- Unknown publisher
- Keyring missing intended issuer

**Action**
- Confirm whether issuer should be trusted
- If yes: add issuer public key intentionally
- If no: keep rejected

---

## 5) Signature verification failed

**Example**
- verifier returns signature mismatch / invalid signature

**Typical cause**
- Tampered envelope payload
- Wrong public key
- Corrupted file

**Action**
- Treat as suspicious
- Re-obtain skill from trusted source
- Re-sign/re-verify through trusted pipeline

---

## 6) File hash mismatch (`--check-file`)

**Example**
- `[FAIL] External file hash does not match signed payload.sha256`

**Typical cause**
- `SKILL.md` changed after signing
- Wrong target file passed to `--check-file`

**Action**
- If expected edit: re-sign file
- If unexpected edit: investigate tampering and reject

---

## 7) Verifier runtime unavailable

**Example**
- `python` executable missing
- loader cannot spawn verifier

**Typical cause**
- Missing runtime dependency
- wrong command path in integration config

**Action**
- Fix runtime path or dependency installation
- strict mode: reject signed path until fixed
- warn mode: temporary warning-only allowance (time-boxed)

---

## Operator policy recommendation

- Production default: strict mode
- Migration default: warn mode + deadline to strict mode
- Never suppress verification failures silently
- Log: skill path, mode, envelope presence, result, reason
