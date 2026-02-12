# OpenClaw Integration Plan for SIE (MVP)

## Objective

Enforce signature + issuer trust verification for skill instructions at load time, so unsigned/untrusted/tampered skills cannot be silently executed as trusted instructions.

---

## Why this matters

Current agent ecosystems often trust plaintext instruction files (`SKILL.md`) by location/convention.
That creates supply-chain risk (namespace squatting, tampering, malicious skill substitution).

SIE adds:

- Integrity (signature verification)
- Authenticity (trusted issuer keyring)
- Fail-closed option (strict rejection)
- Separation between trusted instructions and untrusted content

---

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

## Field notes

- enabled: turns SIE verification on/off
- strict: reject unsigned skills when true
- verifier: executable (python, python3, full path)
- verifyScript: verifier script path
- trustedIssuers: keyring path
- envelopeSuffix: default .sie.json (for SKILL.md.sie.json)

## Loader enforcement behavior (MVP)

### For each discovered SKILL.md:

1. Resolve expected envelope path (SKILL.md + suffix)
2. If SIE disabled → current behavior
3. If SIE enabled:
- envelope exists:
- run verifier:
- --file <envelope>
- --trusted-issuers <path>
- --check-file <skillmd>
- if verify fails → reject skill
- envelope missing:
- strict=true → reject skill
- strict=false → allow + warn

## Minimal integration pseudocode (workspace loader)
```
import fs from "fs";
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

- enabled=true, strict=false
- Warn on missing envelope
- Reject invalid signed envelopes

### Phase B — Enforce mode

- enabled=true, strict=true
- Require valid signed envelope for all skills

## Failure handling

- Verifier binary missing:
- strict=true → reject + explicit error
- strict=false → allow + high-severity warning
- Keyring missing/unreadable:
- strict=true → reject all signed checks
- strict=false → allow unsigned only with warning (temporary migration mode)

## Security boundaries

This protects skill instruction authenticity/integrity.
It does not replace runtime sandboxing, tool permissioning, or OS hardening.
