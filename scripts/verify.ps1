param(
  [string]$File = "SKILL.md.sie.json",
  [string]$TrustedIssuers = "trusted_issuers.json",
  [string]$CheckFile = "SKILL.md"
)

python sie_verify.py --file $File --trusted-issuers $TrustedIssuers --check-file $CheckFile
