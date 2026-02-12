# OpenClaw Integration Plan for SIE (MVP)

## Objective
Enforce signature + issuer trust verification for skill instructions at load time, so unsigned/untrusted/tampered skills cannot be silently executed as trusted instructions.

## Why this matters
Agent runtimes that trust plaintext instruction files (`SKILL.md`) by location/convention are exposed to supply-chain substitution and tampering risks.

SIE contributes:
- Integrity (signature verification)
- Authenticity (trusted issuer keyring)
- Fail-closed capability (strict rejection)
- Clear separation between trusted instructions and untrusted content

## Proposed OpenClaw config surface

```jsonc
{
  "agents": {
    "security": {
      "sie": {
        "enabled": true,
        "strict": true,
        "verifier": "python",
        "verifyScript": "/path/to/sie_verify.py",
        "trustedIssuers": "/path/to/trusted_issuers.json",
        "envelopeSuffix": ".sie.json"
      }
    }
  }
}
```

### Field notes
- `enabled`: turns SIE verification on/off
- `strict`: reject unsigned skills when true
- `verifier`: executable (`python`, `python3`, full path)
- `verifyScript`: verifier script path
- `trustedIssuers`: keyring path
- `envelopeSuffix`: default `.sie.json` (for `SKILL.md.sie.json`)

## Loader enforcement behavior (MVP)
For each discovered `SKILL.md`:

1. Resolve expected envelope path (`SKILL.md` + suffix)
2. If SIE disabled → current behavior
3. If SIE enabled:
   - Envelope exists:
     - run verifier with `--file`, `--trusted-issuers`, `--check-file`
     - if verify fails → reject skill
   - Envelope missing:
     - `strict=true` → reject skill
     - `strict=false` → allow + warn

## Minimal integration pseudocode (workspace loader)

```ts
import { spawnSync } from "child_process";

function verifySkillEnvelope(opts: {
  verifierBin: string;
  verifyScript: string;
  envelopePath: string;
  trustedIssuersPath: string;
  checkFilePath: string;
}): boolean {
  const r = spawnSync(
    opts.verifierBin,
    [
      opts.verifyScript,
      "--file", opts.envelopePath,
      "--trusted-issuers", opts.trustedIssuersPath,
      "--check-file", opts.checkFilePath,
    ],
    { encoding: "utf-8" }
  );
  return r.status === 0;
}
```

## Rollout plan

### Phase A — Observe mode
- `enabled=true`, `strict=false`
- Warn on missing envelope
- Reject invalid signed envelopes

### Phase B — Enforce mode
- `enabled=true`, `strict=true`
- Require valid signed envelope for all skills

## Failure handling
- Verifier binary missing:
  - `strict=true` → reject + explicit error
  - `strict=false` → allow + high-severity warning
- Keyring missing/unreadable:
  - `strict=true` → reject signed checks
  - `strict=false` → allow unsigned temporarily + high-severity warning

## PR-ready implementation checklist

### A) Config plumbing
- [ ] Add `agents.security.sie.*` schema fields
- [ ] Add defaults and validation errors
- [ ] Add docs entry under gateway/agent config

### B) Loader hook
- [ ] Add envelope path resolver in skill loader
- [ ] Add verifier subprocess adapter
- [ ] Add strict/warn decision branch using documented matrix

### C) Logging + observability
- [ ] Emit structured decision logs (`allow`/`reject` + reason)
- [ ] Include envelope presence + verify status in diagnostics

### D) Test plan
- [ ] Unsigned skill allowed in warn mode
- [ ] Unsigned skill rejected in strict mode
- [ ] Signed valid skill allowed
- [ ] Signed invalid/tampered skill rejected
- [ ] Missing verifier runtime behavior matches strict/warn policy

### E) Rollback plan
- [ ] Emergency toggle: `enabled=false`
- [ ] Migration toggle: `strict=false`
- [ ] Operator runbook reference for incident handling

## Security boundaries
This protects skill instruction authenticity/integrity at load time.
It does **not** replace runtime sandboxing, tool permissioning, OS hardening, or key compromise response controls.
