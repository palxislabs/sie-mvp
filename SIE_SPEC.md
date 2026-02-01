# Signed Instruction Envelope (SIE) — Specification v0.1 (MVP)

## Purpose
SIE defines a cryptographically signed container for agent instructions (e.g., SKILL.md). It provides:
- Integrity (tamper detection)
- Authenticity (who issued the instructions)
- Channel separation (instructions vs content)
- Declared scope/constraints for safe execution

## Core Concept: Channel Separation
SIE defines two input channels:
- INSTRUCTION (trusted control-plane): must be signed (SIE) to affect agent behavior/policy/tooling.
- CONTENT (untrusted data-plane): never treated as instructions; cannot override policies; may be summarized/processed.

MVP rule: Agents MUST ignore unsigned "instruction files" by default.

## Envelope Format (JSON)
An envelope is a UTF-8 JSON object with the fields below.

### Required Fields
- `version` (string): must be "0.1"
- `issuer` (string): issuer identifier (e.g., domain or org name)
- `issued_at` (string): ISO-8601 UTC timestamp
- `id` (string): unique identifier (UUID recommended)
- `channel` (string): must be "instruction" for this MVP
- `scope` (array of strings): declared permissions (e.g., "read_files", "call_api", "net_connect")
- `constraints` (object): policy constraints (see below)
- `payload` (object): contains the instructions and metadata
- `signature` (string): base64 signature over canonicalized signing bytes
- `public_key` (string): base64 Ed25519 public key (optional in MVP; recommended for portability)

### Payload Object
`payload` must include:
- `name` (string): e.g., "SKILL.md" or "palxis.skill.summarize.logs"
- `content_type` (string): e.g., "text/markdown"
- `content` (string): the instruction text itself

### Constraints Object (MVP)
- `no_external_urls` (boolean): if true, the agent must not fetch URLs based on this instruction
- `max_output_tokens` (integer): max tokens allowed for responses derived from this instruction
- `deny_prompt_disclosure` (boolean): if true, agent must refuse to reveal internal prompts/config/tool routing

## Signing
Algorithm: Ed25519

Signing input bytes:
- Canonical JSON serialization of the envelope with `signature` removed (and `public_key` excluded if present),
  encoded as UTF-8.

Canonicalization (MVP):
- Sort object keys lexicographically at all levels.
- No extra whitespace.
- Arrays keep original order.

## Verification Rules (Fail Closed)
Given an envelope:
1. Parse JSON; if invalid → FAIL
2. Check `version == "0.1"` → else FAIL
3. Check required fields exist → else FAIL
4. Check `channel == "instruction"` → else FAIL (MVP only)
5. Verify Ed25519 signature using:
   - `public_key` if present, else a locally configured trusted keyring mapping issuer→public_key
6. If signature invalid → FAIL
7. If issuer not trusted (not in keyring and no public_key allowed by policy) → FAIL
8. Enforce constraints locally (adapter responsibility)
9. Only on PASS may the agent load/use `payload.content` as trusted instructions

## Storage Conventions (MVP)
For a given instruction file `SKILL.md`, produce:
- `SKILL.sie.json` (the signed envelope)

## Non-Goals (v0.1)
- Confidentiality of prompt text (encryption is v0.2+)
- Key revocation lists (v0.2+)
- Blockchain identity (optional future)
- Preventing all model jailbreaks (SIE is a trust primitive, not alignment)