# ENFORCEMENT_BEHAVIOR.md — SIE Loader Modes

## Purpose
Define deterministic loader outcomes for signed skill instruction enforcement.

## Terms
- **Skill file**: `SKILL.md`
- **Envelope**: `SKILL.md.sie.json` (default convention)
- **Verifier**: `sie_verify.py` (or compatible verifier)
- **Strict mode**: reject unsigned skills
- **Warn mode**: allow unsigned skills but warn loudly

## Inputs
- `sie.enabled` (bool)
- `sie.strict` (bool)
- Envelope exists? (yes/no)
- Verify result (pass/fail)
- Verifier runtime available? (yes/no)
- Trusted issuer keyring readable? (yes/no)

## Decision Matrix

| Case | enabled | strict | envelope | verifier/keyring state | verify result | Loader action |
|---|---:|---:|---|---|---|---|
| 1 | false | any | any | any | any | Allow (current behavior) |
| 2 | true | false | missing | n/a | n/a | Allow + warn `unsigned skill allowed (warn mode)` |
| 3 | true | true | missing | n/a | n/a | Reject `unsigned skill rejected (strict mode)` |
| 4 | true | any | present | verifier unavailable | n/a | strict: Reject, warn: Allow + high-severity warning |
| 5 | true | any | present | keyring unreadable | n/a | strict: Reject, warn: Allow + high-severity warning |
| 6 | true | any | present | runtime OK | pass | Allow |
| 7 | true | any | present | runtime OK | fail | Reject `signature/issuer/hash verification failed` |

## Expected Verifier Invocation

```bash
python sie_verify.py \
  --file SKILL.md.sie.json \
  --trusted-issuers trusted_issuers.json \
  --check-file SKILL.md
```

## Logging Expectations

Minimum structured fields for each skill load decision:
- `skillPath`
- `enforcementEnabled`
- `strictMode`
- `envelopeFound`
- `verificationAttempted`
- `verificationPassed`
- `action` (`allow` | `reject`)
- `reason`

## Operator Guidance

### Recommended rollout
1. Start with `enabled=true`, `strict=false` for migration visibility.
2. Monitor warnings and sign trusted skills.
3. Move to `strict=true` after inventory is signed and verified.

### Safe defaults for production
- `enabled=true`
- `strict=true`
- explicit trusted issuer keyring path
- explicit envelope naming policy

## Non-goals
This document does not define runtime tool sandboxing, host hardening, or model-level prompt attack defenses. It only defines instruction authenticity/integrity decisions at skill load time.
