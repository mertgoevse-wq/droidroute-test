#!/usr/bin/env bash
# preflight-secrets.sh — block a commit that would leak a credential.
#
# Scans staged content inside a git repository, or every text file when run
# outside one. Exits non-zero when a likely secret is found, naming the file
# and the pattern. Values clearly marked as examples/placeholders are allowed.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PATTERNS=(
  'sk-[A-Za-z0-9_-]{20,}'
  'ghp_[A-Za-z0-9]{20,}'
  'gho_[A-Za-z0-9]{20,}'
  'github_pat_[A-Za-z0-9_]{20,}'
  'AIza[A-Za-z0-9_-]{30,}'
  'pplx-[A-Za-z0-9]{30,}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  'AKIA[0-9A-Z]{16}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}'
)

ALLOWLIST_REGEX='example|placeholder|your[-_]?key|<redacted>|redacted|xxxx|\.example\.json'
SKIP_EXT_REGEX='\.(gguf|onnx|apk|aab|png|jpe?g|webp|gif|ico|jar|zip|so)$'

# One combined scan per file, then classify hits per pattern only when a file
# actually matched. Semantics are identical to per-pattern scanning; this only
# removes ~10 fork/exec calls per file on the common (clean) path.
COMBINED_PATTERN="$(IFS='|'; echo "${PATTERNS[*]}")"

fail=0
LIST="$(mktemp)"
trap 'rm -f "$LIST"' EXIT

if git rev-parse --git-dir >/dev/null 2>&1; then
  git diff --cached --name-only --diff-filter=ACMR >"$LIST" 2>/dev/null || true
  if [ ! -s "$LIST" ]; then
    git ls-files --cached --others --exclude-standard >"$LIST" 2>/dev/null || true
  fi
else
  find . -type f -not -path './.git/*' | sed 's|^\./||' >"$LIST" 2>/dev/null || true
fi

scanned=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  [ -f "$f" ] || continue
  printf '%s' "$f" | grep -Eq "$SKIP_EXT_REGEX" && continue
  case "$f" in scripts/preflight-secrets.sh) continue ;; esac

  # Silently skip binary files (grep hints "binary file matches" otherwise).
  if grep -qI . "$f" 2>/dev/null; then :; else continue; fi

  scanned=$((scanned + 1))
  any_hit="$(grep -Eo "$COMBINED_PATTERN" "$f" 2>/dev/null | head -1)"
  [ -n "$any_hit" ] || continue
  for p in "${PATTERNS[@]}"; do
    if grep -Eq "$p" "$f" 2>/dev/null; then
      hits="$(grep -Eo "$p" "$f" 2>/dev/null | sort -u | head -3)"
      allowed=0
      while IFS= read -r hit; do
        [ -n "$hit" ] || continue
        if printf '%s' "$hit" | grep -Eqi "$ALLOWLIST_REGEX"; then
          allowed=1
        else
          echo "  FAIL  $f  matches /$p/  (value starts: $(printf '%s' "$hit" | cut -c1-10)…)" >&2
          fail=1
        fi
      done <<EOF
$hits
EOF
      :
    fi
  done
done <"$LIST"

echo "preflight: scanned $scanned file(s)."
if [ "$fail" -ne 0 ]; then
  echo "" >&2
  echo "preflight: refusing to continue — a credential-looking value was found." >&2
  echo "  fix: replace it with a placeholder, and rotate the key if it was real." >&2
  exit 1
fi

echo "preflight: no secrets detected."
