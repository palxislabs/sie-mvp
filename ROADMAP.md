# ROADMAP.md — SIE

## Vision
Make trusted agent instructions practical by default: signed, verifiable, fail-closed when desired, and easy to integrate.

## Now (v0.1.x)
- ✅ Signing + verification primitives
- ✅ Trusted issuer keyring support (`--trusted-issuers`)
- ✅ File hash binding (`--check-file`)
- ✅ Basic test coverage for verifier CLI
- ✅ OpenClaw loader integration design doc

## Next (v0.2)
- [ ] Enforced loader integration (warn mode + strict mode)
- [ ] Explicit failure-mode tests (missing issuer, malformed envelope, hash mismatch edge cases)
- [ ] OS-friendly helper scripts and examples
- [ ] Improved threat model with supply-chain scenarios
- [ ] Better operator docs for rollout/migration

## Later (v0.3)
- [ ] Native TypeScript verifier path (remove runtime Python dependency in core integrations)
- [ ] Issuer key rotation + revocation flow
- [ ] Optional transparency/audit logs for trust decisions
- [ ] Signed policy bundles for channel separation controls

## Business Track (parallel)
- [ ] Publish OSS core with adoption-first docs
- [ ] Validate demand via integration support and trust hardening help
- [ ] Test enterprise offerings (registry, compliance logs, policy management)

## Principles
- Minimize trust assumptions
- Fail closed where security-sensitive
- Keep implementation composable
- Prefer boring, testable security over cleverness
