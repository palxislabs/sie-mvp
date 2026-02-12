# NEXT_STEPS.md — 7-Day Execution Plan

## Goal (This Week)
Ship practical, adoptable SIE improvements that reduce real skill supply-chain risk now.

## Day 1 — Stabilize Core
- [ ] Confirm verifier CLI behavior matrix (valid / invalid / untrusted / missing issuer / hash mismatch).
- [ ] Add quick smoke commands section to README.
- [ ] Define v0.2 acceptance criteria (max 5 bullets).

## Day 2 — Enforcement Semantics
- [ ] Create `docs/ENFORCEMENT_BEHAVIOR.md` with strict vs warn mode table.
- [ ] Define canonical envelope naming policy (`SKILL.md.sie.json`).
- [ ] Document fail-closed defaults and migration path.

## Day 3 — Developer UX
- [ ] Add helper scripts (`scripts/verify.ps1`, `scripts/verify.sh`, `scripts/sign.ps1`, `scripts/sign.sh`).
- [ ] Add one command examples in README for Win/Linux/macOS.
- [ ] Ensure all examples are copy-paste safe.

## Day 4 — Threat Model Hardening
- [ ] Add explicit attack trees for: namespace squatting, malicious skill substitution, issuer key compromise.
- [ ] Add non-goals section to prevent over-claiming.
- [ ] Add operational mitigations list (pin author/path/commit, review diffs, least privilege).

## Day 5 — Integration Readiness
- [ ] Refine `docs/OPENCLAW_INTEGRATION.md` into PR-ready checklist.
- [ ] Add a loader decision matrix (inputs -> outcomes).
- [ ] Add logging expectations for rejected skills.

## Day 6 — Evidence + Communication
- [ ] Publish a technical note with reproducible demo and limitations.
- [ ] Add "How to validate this claim" section (commands + expected outputs).
- [ ] Prepare short social summary + long technical version.

## Day 7 — Revenue Alignment Checkpoint
- [ ] Choose first monetization experiment (hosted trust registry / enterprise policy pack / integration support).
- [ ] Define 2-week MVP scope and success metrics.
- [ ] Commit to one distribution channel for discovery.

---

## Non-Negotiables
- Daily shipping > perfect architecture.
- Security claims must be precise and testable.
- Keep defaults safe for beginners.
- Every change should improve either trust, adoption, or speed-to-deploy.
