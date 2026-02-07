# Changelog

All notable changes to this project will be documented in this file.

---

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
