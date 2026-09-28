#!/usr/bin/env bash
# log-step.sh — write one structured, redacted log record.
#
#   scripts/log-step.sh T-042 "write" "QuotaLedger.kt" "created"
#   scripts/log-step.sh T-042 "test" "gradle testDebugUnitTest" "pass" --actor verify --dur 4210
#   scripts/log-step.sh T-042 "error" "provider call" "fail: timeout" --level error
#
# Records go to logs/tasks/<task>.log, logs/daily/<date>.log and (for task
# boundaries) logs/chain.log. Format: handbooks/05-logging-standard.md
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

usage() { echo "usage: log-step.sh <T-0xx|chain> <action> <target> <result> [--actor A] [--level L] [--dur MS] [--extra JSON]" >&2; exit 2; }

[ $# -ge 4 ] || usage
TASK="$1"; ACTION="$2"; TARGET="$3"; RESULT="$4"; shift 4

ACTOR="main"; LEVEL="info"; DUR=""; EXTRA="{}"
while [ $# -gt 0 ]; do
  case "$1" in
    --actor) ACTOR="$2"; shift 2 ;;
    --level) LEVEL="$2"; shift 2 ;;
    --dur)   DUR="$2";   shift 2 ;;
    --extra) EXTRA="$2"; shift 2 ;;
    *) usage ;;
  esac
done

# --- redaction ---------------------------------------------------------------
# Belt and braces: the tooling must never write a credential into a log that is
# pushed to GitHub, even if a caller passes one by mistake.
redact() {
  sed -E \
    -e 's/(sk-[A-Za-z0-9_-]{8})[A-Za-z0-9_-]+/\1<redacted>/g' \
    -e 's/(ghp_[A-Za-z0-9]{6})[A-Za-z0-9]+/\1<redacted>/g' \
    -e 's/(gho_[A-Za-z0-9]{6})[A-Za-z0-9]+/\1<redacted>/g' \
    -e 's/(AIza[A-Za-z0-9]{6})[A-Za-z0-9_-]+/\1<redacted>/g' \
    -e 's/(pplx-[A-Za-z0-9]{6})[A-Za-z0-9]+/\1<redacted>/g' \
    -e 's/((Authorization|authorization|x-api-key)[^,}]{0,20}:?[[:space:]]*)[^"]{8,}/\1<redacted>/g' \
    -e 's/"?(api[_-]?key|token|password|secret)"?[[:space:]]*[:=][[:space:]]*"[^"]{8,}"/"\1":"<redacted>"/g'
}

json_escape() {
  python3 -c 'import json,sys; sys.stdout.write(json.dumps(sys.stdin.read())[1:-1])' 2>/dev/null \
    || tr -d '"\\'
}

TERM="$(printf '%s' "$TARGET" | json_escape | redact)"
RES="$(printf '%s' "$RESULT" | json_escape | redact)"
ACT="$(printf '%s' "$ACTOR" | json_escape | redact)"
EXT="$(printf '%s' "$EXTRA" | redact)"

DUR_FIELD=""
[ -n "$DUR" ] && DUR_FIELD=",\"dur_ms\":$DUR"

RECORD="$(printf '{"ts":"%s","task":"%s","actor":"%s","level":"%s","action":"%s","target":"%s","result":"%s"%s,"extra":%s}' \
  "$(date -Iseconds)" "$TASK" "$ACT" "$LEVEL" "$ACTION" "$TERM" "$RES" "$DUR_FIELD" "$EXT" | redact)"

mkdir -p logs/tasks logs/daily
printf '%s\n' "$RECORD" >> "logs/tasks/${TASK}.log"
printf '%s\n' "$RECORD" >> "logs/daily/$(date +%F).log"

# Task boundaries also land in the chain log — that file is the handover spine.
case "$ACTION" in
  start|finish|commit|push|decide|error) printf '%s\n' "$RECORD" >> logs/chain.log ;;
esac

echo "$RECORD"
