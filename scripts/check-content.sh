#!/usr/bin/env bash
# Fail if blacklisted content appears outside allowed paths.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Exact blacklist from packaging checklist. Do not use bare "ito".
PATTERN='\bIBAN\b|BIC[: ]|hiscox|azinove|rambert|genuyt|eiermann|goldschmidt|bodein|steeve|petitnid|kairos|centralis|slean|ze rencontre|dt interim|dt-interim|kappeler|gl events|gl-events|hemmerlin|ito calorifuge|partenaire odoo|odoo partner|\bn8n\b|make\.com|no-code|nocode|ne pas diffuser|notes internes'

echo "==> 1/2 Scanning for blacklisted content patterns…"

set +e
# --exclude-dir matches directory basenames (node_modules, input, data, coverage…).
MATCHES="$(
  grep -riEn "$PATTERN" . \
    --exclude-dir=node_modules \
    --exclude-dir=input \
    --exclude-dir=data \
    --exclude-dir=coverage \
    --exclude-dir=.git \
    --exclude-dir=.wrangler \
    --exclude=check-content.sh \
    2>/dev/null
)"
GREP_STATUS=$?
set -e

if [[ "$GREP_STATUS" -eq 0 ]]; then
  echo "Blacklisted content found:"
  printf '%s\n' "$MATCHES"
  exit 1
elif [[ "$GREP_STATUS" -gt 1 ]]; then
  echo "grep failed with status $GREP_STATUS" >&2
  exit "$GREP_STATUS"
fi

echo "No blacklisted patterns found."

echo "==> 2/2 Running gitleaks (if installed)…"
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --no-git --source .
else
  echo "gitleaks not installed; skipping secret scan (success)."
fi

echo "==> check-content: OK"
