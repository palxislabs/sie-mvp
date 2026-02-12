# IMPLEMENTATION_TICKETS.md — OpenClaw Loader Enforcement (MVP)

## Ticket 1 — Config surface for SIE enforcement

### Scope
Add `agents.security.sie.*` config keys:
- `enabled` (bool)
- `strict` (bool)
- `verifier` (string)
- `verifyScript` (string)
- `trustedIssuers` (string)
- `envelopeSuffix` (string, default `.sie.json`)

### Acceptance
- Config validates
- Invalid shape yields actionable error
- Defaults documented

---

## Ticket 2 — Envelope path resolver in skill loader

### Scope
For each `SKILL.md`, resolve envelope path as `SKILL.md` + `envelopeSuffix`.

### Acceptance
- Resolver handles missing envelope deterministically
- Behavior follows strict/warn mode

---

## Ticket 3 — Verifier subprocess adapter

### Scope
Execute verifier with:
- `--file <envelope>`
- `--trusted-issuers <path>`
- `--check-file <skillmd>`

### Acceptance
- Non-zero exit -> verification failure
- stdout/stderr captured for diagnostics

---

## Ticket 4 — Strict/Warn decision branch

### Scope
Implement decision matrix from `docs/ENFORCEMENT_BEHAVIOR.md`.

### Acceptance
- Strict rejects unsigned
- Warn allows unsigned with high-severity warning
- Invalid signed envelope always rejected

---

## Ticket 5 — Structured logging

### Scope
Emit structured fields:
- `skillPath`
- `enforcementEnabled`
- `strictMode`
- `envelopeFound`
- `verificationAttempted`
- `verificationPassed`
- `action`
- `reason`

### Acceptance
- Logs available for failed and successful decisions
- Operator can explain any load outcome from logs

---

## Ticket 6 — Test matrix in OpenClaw side

### Scope
Add loader tests for:
- unsigned+warn -> allow
- unsigned+strict -> reject
- signed valid -> allow
- signed invalid -> reject
- verifier unavailable -> strict reject, warn allow+warn
- keyring missing -> strict reject, warn allow+warn

### Acceptance
- All matrix branches covered

---

## Ticket 7 — Rollout controls

### Scope
Document operational rollout:
- start warn mode
- migrate to strict after signed coverage
- emergency toggle (`enabled=false`)

### Acceptance
- Operator runbook exists and references failure docs
