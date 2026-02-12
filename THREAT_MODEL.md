# Threat Model (v0.1) — Signed Instruction Envelope (SIE)

_Last updated to include indirect injection and prompt disclosure risks observed in OpenClaw-style agent frameworks._


## Goal
Prevent agents and humans from executing or trusting modified or untrusted instruction artifacts (e.g., SKILL.md),
by requiring cryptographic integrity + publisher authentication and enforcing fail-closed verification.

## Assets to Protect
- Instruction integrity (no silent modification)
- Instruction provenance (who issued it)
- Trust boundary between "instructions" and "content"
- Agent tool permissions (prevent overbroad execution triggered by untrusted instructions)
- User safety (prevent malicious actions initiated via injected instructions)

## Assumptions
- The verifier runs locally and is not bypassed (or bypassing is considered a user choice).
- Public keys for trusted issuers can be obtained securely (pinned, bundled, or via trusted registry).
- Attackers may control instruction content, transport channel, and surrounding context files.

## In-Scope Threats (We Defend Against)

### T1 — Tampered instruction files
An attacker modifies SKILL.md (or equivalent instruction pack) at rest or in transit.
Outcome without SIE: agent follows malicious instructions.
SIE mitigation: signature verification fails; execution blocked.

### T2 — Untrusted publishers / supply-chain skills
User downloads a skill pack from an unknown source or compromised repository.
Outcome without SIE: agent trusts it.
SIE mitigation: unsigned or unknown-signer skills are rejected by default.

### T3 — Instruction/content confusion (prompt injection via files)
Untrusted content is treated as trusted instruction because it's in the same channel.
Outcome without SIE: agent is "confused deputy".
SIE mitigation: only signed instruction envelopes are treated as trusted instructions; other content is treated as untrusted input.

### T4 — Skill registry poisoning
Popular skill registries or shared folders contain one malicious skill.
Outcome without SIE: mass compromise.
SIE mitigation: verifier blocks unsigned/tampered skills; allows only explicitly trusted issuers.

### T5 — Indirect prompt injection via untrusted content (documents, emails, code)
An attacker places instructions inside content that the agent is asked to read/summarize/review (e.g., an email,
PDF, README, code review text), causing the agent to treat content as instructions and change behavior or exfiltrate
information.
Outcome without channel separation: agent follows attacker instructions (e.g., prints verification tokens, reveals config).
SIE mitigation (MVP): enforce channel separation — only signed instruction envelopes may modify behavior/policy. Untrusted
content is treated as data and cannot introduce new directives.

### T6 — System prompt / configuration disclosure
An attacker tricks the agent into revealing internal instructions, routing logic, tool names, secrets, or configuration
by asking it to "explain how you work", "print your system prompt", or perform structured "conversion" of system text.
Outcome: leakage of internal control instructions; improved attacker success and repeated exploitation.
SIE mitigation (MVP): reduce plaintext sensitive instruction distribution; require signed instruction artifacts for trusted
control-plane data; add a policy gate that refuses requests to reveal internal instructions/configuration.

## Concrete Supply-Chain Scenarios (Operator-Facing)

### S1 — Namespace/frontmatter squatting in community skill repos
Attacker publishes a malicious skill variant that resolves before the intended one due to discovery/order logic
(e.g., name collision in metadata).
Outcome without strong trust checks: wrong skill is installed as if legitimate.
SIE mitigation: envelope verification ties trust to issuer key, not to display name or discovery order.

### S2 — Malicious skill substitution after install
A legitimate `SKILL.md` is replaced or edited on disk post-install by another process/user.
Outcome without integrity check: agent executes modified instructions.
SIE mitigation: `--check-file` hash binding detects file tampering and rejects trust.

### S3 — Issuer private key compromise
Attacker steals a trusted issuer's signing key and produces valid signatures.
Outcome: cryptographic verification alone cannot distinguish attacker output.
MVP status: not fully solved. Requires key rotation, revocation, and short trust windows in later versions.
Operator mitigation now: keep trusted keyring minimal, monitor issuer behavior, and be ready to remove compromised issuers quickly.

## Out-of-Scope (Explicitly Not Solved by MVP)
- Model-level jailbreaks that ignore policies even with signed instructions
- Vulnerabilities in the agent runtime, tool implementations, OS, or sandbox escape
- Data exfiltration via allowed tools when user explicitly grants overbroad scope
- Attacks that compromise issuer private keys (handled via revocation/key rotation in later versions; MVP assumes keys remain secret)

## Security Properties Provided by MVP
- Integrity: any modification of the signed payload is detectable
- Authenticity: issuer identity is verifiable via public key
- Fail-closed: verification failure prevents trust/execution
- Least-privilege declaration: instruction scope is explicit (enforced by adapters)

## MVP Success Criteria
- A signed SKILL.md verifies successfully and loads
- A single-byte modification causes verification failure
- Unknown signer causes rejection by default
- Demo clearly shows prompt-injection/supply-chain modification being blocked
