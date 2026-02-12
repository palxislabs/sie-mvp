param(
  [string]$Issuer = "palxislabs",
  [string]$Target = "SKILL.md"
)

python sie_sign.py --issuer $Issuer --infile $Target
