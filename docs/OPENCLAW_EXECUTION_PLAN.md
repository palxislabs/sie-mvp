# OPENCLAW_EXECUTION_PLAN.md — From Docs to Core Patch

## Objective
Turn the integration design into a sequence of implementation tasks that can be executed in OpenClaw core with minimal risk.

## Phase 1 — Design freeze (low risk)

- [ ] Confirm config field names and defaults (`agents.security.sie.*`).
- [ ] Confirm envelope naming convention (`SKILL.md.sie.json`).
- [ ] Confirm strict/warn behavior table as canonical.

Deliverable:
- Finalized design ticket approved for implementation.

---

## Phase 2 — MVP implementation patch

### 2.1 Config + validation
- [ ] Add SIE config schema entries.
- [ ] Add clear validation errors for missing required fields when enabled.

### 2.2 Loader hook
- [ ] Resolve envelope path per `SKILL.md`.
- [ ] Call verifier subprocess with:
  - `--file`
  - `--trusted-issuers`
  - `--check-file`

### 2.3 Decision branch
- [ ] Strict: reject unsigned skills.
- [ ] Warn: allow unsigned with warning.
- [ ] Always reject invalid signed envelope.

Deliverable:
- Small, reviewable patch with deterministic behavior.

---

## Phase 3 — Observability + tests

- [ ] Add structured logs for allow/reject decisions.
- [ ] Add test matrix covering strict/warn + verifier/keyring failures.
- [ ] Ensure behavior is stable when SIE feature is disabled (backward compatibility).

Deliverable:
- CI green with explicit branch coverage.

---

## Phase 4 — Operator rollout

- [ ] Publish migration guidance: warn mode first, strict mode second.
- [ ] Link incident and failure docs for operators.
- [ ] Add rollback instructions (`enabled=false` emergency path).

Deliverable:
- Release notes + migration section.

---

## Definition of Done

- Configurable SIE loader enforcement lands behind feature flag.
- Strict/warn modes behave exactly as documented.
- Unsigned/tampered/untrusted instructions are not silently trusted.
- Operator docs and rollback path are shipped with the feature.

---

## Risk controls

- Keep first patch minimal and optional.
- Avoid coupling to unrelated security changes.
- Preserve default behavior when feature not enabled.
- Prefer explicit failures over silent fallback.
