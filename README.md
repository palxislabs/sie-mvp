# SIE MVP — Signed Instruction Envelope (Security primitive for agent instructions)

SIE (Signed Instruction Envelope) is a minimal security primitive for agent systems that rely on plain-text
instruction files (e.g., `SKILL.md`, “skill packs”, tool configs, memory/instruction folders).

It targets a structural weakness in modern agent architectures:

> Agents cannot reliably distinguish **trusted instructions** from **untrusted content**.

This enables:
- **Skill supply-chain poisoning** (tampered or malicious skill files)
- **Indirect prompt injection** via documents/emails/code reviews/PDFs
- **Prompt/config/tool disclosure** via “explain how you work / print system prompt / list tools” attacks

SIE provides:
- **Integrity**: tamper detection via Ed25519 signatures
- **Authenticity**: issuer trust via a local keyring (`trusted_issuers.json`)
- **Fail-closed verification**: invalid/untrusted envelopes are rejected
- **Channel separation**: only signed envelopes are treated as INSTRUCTIONS; all other inputs are CONTENT

This repository contains a reference implementation + demo.

---

## What SIE guarantees (MVP)

✅ **If verification passes**, the instruction payload is:
- unmodified since signing (integrity)
- issued by a trusted signer (authenticity, via keyring)

✅ **Unsigned / untrusted instruction sources are rejected by default.**

✅ **Untrusted content cannot become trusted instructions** (channel separation pattern).

---

## What SIE does NOT claim (v0.1)

SIE is a trust primitive, not a full sandbox or alignment solution.

❌ It does not prevent all model jailbreaks.  
❌ It does not sandbox tool execution by itself.  
❌ It does not prevent compromise of issuer private keys (revocation comes later).  
❌ It does not stop OS/runtime vulnerabilities.

See: `THREAT_MODEL.md`

---

## Repo contents

- `SIE_SPEC.md` — envelope format + signing/verification rules
- `THREAT_MODEL.md` — threats, assumptions, non-goals
- `sie_lib.py` — canonical JSON + sign/verify helpers
- `sie_sign.py` — sign an instruction file into `*.sie.json`
- `sie_verify.py` — verify signature + trusted issuer + optional file binding
- `trusted_issuers.json` — trusted issuer public keys (keyring)
- `demo/` — indirect injection demo

---
## Quickstart

> **Windows PowerShell:** `& .\.venv\Scripts\Activate.ps1`  
> **Linux/macOS:** `source .venv/bin/activate`

### Install dependency
```bash
python -m pip install pynacl
```

### Sign a skill file
```bash
python sie_sign.py --issuer palxislabs --infile SKILL.md
```

### Verify the envelope with trusted issuers
```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json
```

### Verify + bind to on-disk file (tamper detection)
```bash
python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md
```

## Helper scripts (recommended)

### Windows (PowerShell)
```powershell
.\scripts\sign.ps1
.\scripts\verify.ps1
```

### Linux/macOS
```bash
./scripts/sign.sh
./scripts/verify.sh
```

### Demo: Indirect prompt injection is blocked
```bash
python demo/run_demo.py
```

## License
MIT
