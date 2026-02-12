# Changelog

All notable changes to this project will be documented in this file.

---

## Unreleased

### Added
- Verifier CLI support for configurable trusted issuer keyring path: `--trusted-issuers`.
- CLI test coverage for trusted-issuer verification and key failure cases:
  - untrusted issuer rejection
  - hash mismatch rejection (`--check-file`)
  - missing issuer rejection
  - malformed envelope rejection
- Cross-platform helper scripts:
  - `scripts/sign.ps1`, `scripts/verify.ps1`
  - `scripts/sign.sh`, `scripts/verify.sh`
- Operator-focused documentation:
  - `docs/SECURITY_QUICKSTART.md`
  - `docs/OPERATOR_CHECKLIST.md`
  - `docs/FAILURE_MODES.md`
  - `docs/VALIDATION.md`
  - `docs/ENFORCEMENT_BEHAVIOR.md`
- OpenClaw integration planning update with PR-ready implementation checklist:
  - `docs/OPENCLAW_INTEGRATION.md`
- Project planning docs:
  - `NEXT_STEPS.md`
  - `ROADMAP.md`

### Changed
- `README.md` quickstart now uses trusted-issuer verification flow and references helper scripts + operator docs.
- Public planning docs were sanitized to avoid exposing private commercial strategy.

## v0.1.0 — Initial public release

### Added
- Signed Instruction Envelope (SIE) format and reference implementation
- Ed25519 signing and verification tools (`sie_sign.py`, `sie_verify.py`)
- Channel separation enforcement (instructions vs untrusted content)
- Policy module blocking prompt disclosure and indirect injection
- Integration loader for agent frameworks
- Signed issuer registry snapshot (neutral trust infrastructure)
- Registry client with remote fetch + local cache
- Revocation enforcement via registry
- Demonstration showing injected content is treated as data, not instructions
- Unit tests and CI workflow

### Security properties demonstrated
- Instruction authenticity verification
- Tamper detection for skill files
- Trusted issuer enforcement
- Revocation capability
- Blocking of indirect prompt injection attempts

### Notes
This is an MVP reference implementation intended to validate the architecture and enable ecosystem experimentation.
