# OPENCLAW_PATCH_SKELETON.md — Minimal Loader Patch Outline

## Goal
Provide a concrete patch skeleton maintainers can adapt quickly in OpenClaw core.

## Suggested target area
- skill loader path (where `SKILL.md` entries are discovered and loaded)
- add optional verification gate before skill is accepted

## Config read helper (pseudo)

```ts
const sie = config.agents?.security?.sie;
const sieEnabled = !!sie?.enabled;
const sieStrict = !!sie?.strict;
const verifierBin = sie?.verifier ?? "python";
const verifyScript = sie?.verifyScript;
const trustedIssuers = sie?.trustedIssuers;
const suffix = sie?.envelopeSuffix ?? ".sie.json";
```

## Envelope resolver (pseudo)

```ts
function envelopePathFor(skillMdPath: string, suffix = ".sie.json") {
  return `${skillMdPath}${suffix}`;
}
```

## Verifier adapter (pseudo)

```ts
import { spawnSync } from "child_process";

function verifyEnvelope(opts: {
  verifierBin: string;
  verifyScript: string;
  envelopePath: string;
  trustedIssuers: string;
  checkFile: string;
}) {
  const r = spawnSync(
    opts.verifierBin,
    [
      opts.verifyScript,
      "--file", opts.envelopePath,
      "--trusted-issuers", opts.trustedIssuers,
      "--check-file", opts.checkFile,
    ],
    { encoding: "utf-8" }
  );

  return {
    ok: r.status === 0,
    code: r.status ?? -1,
    stdout: r.stdout ?? "",
    stderr: r.stderr ?? "",
  };
}
```

## Loader decision branch (pseudo)

```ts
const envelopePath = envelopePathFor(skillMdPath, suffix);
const envelopeExists = fs.existsSync(envelopePath);

if (!sieEnabled) {
  allowSkill();
  return;
}

if (!envelopeExists) {
  if (sieStrict) rejectSkill("unsigned skill rejected (strict mode)");
  else {
    warn("unsigned skill allowed (warn mode)");
    allowSkill();
  }
  return;
}

if (!verifyScript || !trustedIssuers) {
  if (sieStrict) rejectSkill("SIE config incomplete in strict mode");
  else {
    warn("SIE config incomplete; allowing in warn mode");
    allowSkill();
  }
  return;
}

const result = verifyEnvelope({
  verifierBin,
  verifyScript,
  envelopePath,
  trustedIssuers,
  checkFile: skillMdPath,
});

if (!result.ok) {
  rejectSkill(`SIE verify failed (code=${result.code})`);
  return;
}

allowSkill();
```

## Structured logging fields

- `skillPath`
- `sieEnabled`
- `sieStrict`
- `envelopePath`
- `envelopeExists`
- `verifyAttempted`
- `verifyOk`
- `action` (`allow|reject`)
- `reason`

## Minimal test checklist for patch

- [ ] unsigned+warn => allow+warn
- [ ] unsigned+strict => reject
- [ ] signed valid => allow
- [ ] signed invalid => reject
- [ ] missing verifier runtime => strict reject, warn allow+warn
- [ ] missing trusted issuers path => strict reject, warn allow+warn

## Notes

- Keep patch small and optional.
- Preserve current default behavior when SIE disabled.
- Avoid coupling to unrelated security changes in first PR.
