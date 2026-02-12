# MAINTAINER_CHECKLIST.md — Pre-Release Checklist

Use this before publishing release notes or asking users to adopt a new SIE version.

## Core correctness
- [ ] `python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json`
- [ ] `python sie_verify.py --file SKILL.md.sie.json --trusted-issuers trusted_issuers.json --check-file SKILL.md`
- [ ] `python -m unittest discover -s tests -p "test_*.py" -v`

## Negative-path sanity
- [ ] Untrusted issuer rejection still works
- [ ] Hash mismatch rejection still works
- [ ] Missing issuer rejection still works
- [ ] Malformed envelope rejection still works

## Docs coherence
- [ ] README quickstart commands match current CLI behavior
- [ ] Operator docs linked from README are present and current
- [ ] Integration docs do not over-claim security guarantees

## Public-safety check
- [ ] No private strategy/business-sensitive notes accidentally added
- [ ] No secrets/tokens/keys in committed files
- [ ] No local absolute paths in public docs

## Release hygiene
- [ ] Changelog updated with user-relevant changes
- [ ] Commit history is understandable
- [ ] Tag/release note prepared (if publishing)
