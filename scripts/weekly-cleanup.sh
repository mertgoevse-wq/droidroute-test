#!/usr/bin/env bash
# weekly-cleanup.sh — keep the repository lean without destroying the audit trail.
#
# Retention:
#   logs/daily/  -> keep the newest 14 files
#   logs/tasks/  -> keep the newest 60 files
#   logs/chain.log -> never pruned
# Pruned files move to logs/archive/ (git-ignored) instead of being deleted.
#
# Runs from the repo-hygiene workflow weekly, or by hand:
#   scripts/weekly-cleanup.sh [--dry-run]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

DAILY_KEEP=14
TASK_KEEP=60

mkdir -p logs/archive/daily logs/archive/tasks logs/daily logs/tasks

prune() {
  local dir="$1" keep="$2" archive="$3" label="$4"
  local list moved=0
  # shellcheck disable=SC2012
  list="$(ls -1t "$dir" 2>/dev/null | tail -n +$((keep + 1)))" || list=""
  if [ -z "$list" ]; then
    echo "  $label: nothing to prune (keep $keep)"
    return 0
  fi
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "  [dry-run] $dir/$f -> $archive/$f"
    else
      mv "$dir/$f" "$archive/$f"
    fi
    moved=$((moved + 1))
  done <<EOF
$list
EOF
  echo "  $label: pruned $moved (keeping $keep)"
}

echo "weekly-cleanup $(date -Iseconds)"
prune logs/daily  "$DAILY_KEEP" logs/archive/daily "daily logs"
prune logs/tasks  "$TASK_KEEP"  logs/archive/tasks "task logs"

if [ "$DRY_RUN" -eq 0 ]; then
  {
    echo ""
    echo "## Log rotation $(date -Iseconds)"
    echo "- daily: keep $DAILY_KEEP, tasks: keep $TASK_KEEP"
    echo "- archived to \`logs/archive/\` (local only, not committed)"
    echo "- chain.log untouched"
  } >> logs/daily/"$(date +%F).log"
else
  echo "(dry run — nothing was moved)"
fi
