# IMPLEMENTATION_RISKS.md — Known Risks and Mitigations

## Purpose
Track practical implementation risks while integrating SIE into real agent runtimes.

## Risk 1 — False sense of complete security

**Description**
Teams may assume signed instructions alone solve broader agent security.

**Impact**
Critical controls (sandboxing, least privilege, host hardening) may be neglected.

**Mitigation**
- Keep boundaries explicit in README/docs
- Require `SECURITY_CLAIMS.md` review before releases

---

## Risk 2 — Strict mode rollout breakage

**Description**
Turning strict mode on before signed coverage is complete can block workflows.

**Impact**
Operational disruption and rollback pressure.

**Mitigation**
- Follow warn -> strict rollout path (`ADOPTION_PATH.md`)
- Keep emergency toggle documented

---

## Risk 3 — Keyring drift / over-trust

**Description**
Trusted issuer list grows without governance.

**Impact**
Attack surface increases; trust policy weakens.

**Mitigation**
- Keep issuer set minimal
- Periodically review and prune issuers
- Document ownership for keyring updates

---

## Risk 4 — Runtime dependency fragility

**Description**
Verifier subprocess runtime missing/misconfigured in deployment env.

**Impact**
Unclear behavior, especially during strict enforcement.

**Mitigation**
- Test runtime in CI and deployment scripts
- Ensure strict/warn fallback behavior is explicit and logged

---

## Risk 5 — Incomplete logging for rejected skills

**Description**
Reject decisions without actionable logs slow incident response.

**Impact**
Operators cannot quickly triage trust failures.

**Mitigation**
- Enforce structured logging fields from enforcement docs
- Keep reason strings operator-friendly

---

## Risk 6 — Upstream integration scope creep

**Description**
First OpenClaw patch includes unrelated refactors.

**Impact**
Higher review friction, delayed merge.

**Mitigation**
- Keep first PR minimal and optional
- Separate architectural improvements into follow-up PRs
