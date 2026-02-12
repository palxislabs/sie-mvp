# SECURITY_CLAIMS.md — What SIE Claims (and Does Not)

## Purpose
Keep security messaging accurate, testable, and non-hype.

## Claims we can make now (v0.1)

1. **Integrity verification**
   - If signed payload bytes change, verification fails.

2. **Issuer trust enforcement**
   - If issuer is not in trusted keyring, verification fails.

3. **Optional on-disk file binding**
   - `--check-file` detects mismatch between signed hash and local file content.

4. **Fail-closed compatibility**
   - Integrations can reject untrusted/invalid envelopes deterministically.

## Claims we should avoid (for now)

- “Prevents all prompt injection.”
- “Solves AI alignment/safety broadly.”
- “Eliminates need for sandboxing or least privilege.”
- “Protects against compromised signer private keys.”

## Correct phrasing examples

✅ "SIE helps enforce instruction authenticity and integrity before trust."

✅ "SIE reduces skill supply-chain risk when integrated into a fail-closed loader path."

✅ "SIE is one control layer and should be combined with sandboxing and host hardening."

## Evidence mapping

- Integrity/tamper checks: `docs/VALIDATION.md`
- Failure behaviors: `docs/FAILURE_MODES.md`
- Loader semantics: `docs/ENFORCEMENT_BEHAVIOR.md`
- Integration path: `docs/OPENCLAW_INTEGRATION.md`

## Maintainer note

If a claim cannot be validated by a command/test/doc in this repo, do not publish it as a security guarantee.
