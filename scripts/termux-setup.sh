#!/usr/bin/env bash
# termux-setup.sh — point the agents running in Termux / proot-Debian at DroidRoute.
#
#   scripts/termux-setup.sh                 # exports for this shell + health check
#   scripts/termux-setup.sh --persist       # also append to ~/.bashrc
#   scripts/termux-setup.sh --port 8787
set -euo pipefail

PORT="8787"
PERSIST=0
HOST="127.0.0.1"

while [ $# -gt 0 ]; do
  case "$1" in
    --persist) PERSIST=1; shift ;;
    --port)    PORT="$2"; shift 2 ;;
    --host)    HOST="$2"; shift 2 ;;
    -h|--help) sed -n '2,10p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

BASE="http://${HOST}:${PORT}"

cat <<EOF
# DroidRoute — add these to your shell (or re-run with --persist)

export ANTHROPIC_BASE_URL="$BASE"
export ANTHROPIC_API_KEY="\${ANTHROPIC_API_KEY:-droidroute}"
export OPENAI_BASE_URL="$BASE/v1"
export OPENAI_API_KEY="\${OPENAI_API_KEY:-droidroute}"
export DROIDROUTE_PORT="$PORT"

# Claude Code picks up ANTHROPIC_BASE_URL automatically.
# Freebuff / other OpenAI-compatible agents use OPENAI_BASE_URL.
EOF

if [ "$PERSIST" -eq 1 ]; then
  RC="${HOME}/.bashrc"
  touch "$RC"
  if ! grep -q 'ANTHROPIC_BASE_URL="http://127.0.0.1' "$RC" 2>/dev/null; then
    {
      echo ""
      echo "# --- DroidRoute (added $(date -Iseconds)) ---"
      echo "export ANTHROPIC_BASE_URL=\"$BASE\""
      echo "export ANTHROPIC_API_KEY=\"\${ANTHROPIC_API_KEY:-droidroute}\""
      echo "export OPENAI_BASE_URL=\"$BASE/v1\""
      echo "export OPENAI_API_KEY=\"\${OPENAI_API_KEY:-droidroute}\""
    } >> "$RC"
    echo "persisted to $RC"
  else
    echo "$RC already configured — left untouched"
  fi
fi

echo ""
echo "health check:"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS --max-time 5 "$BASE/health" 2>/dev/null; then
    echo ""
    echo "OK: DroidRoute is reachable on $BASE"
  else
    echo "NOT REACHABLE: is the app running and the port $PORT?"
    echo "  start DroidRoute on the phone, then re-run this script."
    exit 1
  fi
else
  echo "curl not installed (pkg install curl) — skipping the health check."
fi
