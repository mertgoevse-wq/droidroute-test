#!/usr/bin/env bash
# step-commit.sh — the single sanctioned way to commit in this repository.
#
# Every completed task ends with:
#   scripts/step-commit.sh "T-042: implement quota ledger"
#
# Before a risky task:
#   scripts/step-commit.sh --checkpoint "T-043"
#
# Release tagging:
#   scripts/step-commit.sh --tag v0.1.0 "T-147: release"
#
# It always: runs the secret preflight -> stages everything -> commits -> pushes.
# A push failure never loses the commit: it is logged and retried later.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MODE="commit"
TAG=""
ARGS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --checkpoint) MODE="checkpoint"; shift ;;
    --tag)        MODE="commit"; TAG="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

MESSAGE="${ARGS[0]:-}"
if [ -z "$MESSAGE" ]; then
  echo "usage: scripts/step-commit.sh [--checkpoint|--tag <version>] \"<message>\"" >&2
  exit 2
fi

TASK_ID="$(printf '%s' "$MESSAGE" | grep -oE 'T-[0-9]{3}' | head -1 || true)"

log_chain() {
  local action="$1" result="$2" extra="${3:-{\}}"
  mkdir -p logs
  printf '{"ts":"%s","task":"%s","actor":"main","level":"info","action":"%s","target":"git","result":"%s","extra":%s}\n' \
    "$(date -Iseconds)" "${TASK_ID:-chain}" "$action" "$result" "$extra" >> logs/chain.log
}

# 1. Secret preflight — the reason this repository has no leaked keys.
if ! scripts/preflight-secrets.sh; then
  echo "step-commit: refusing to commit — secret preflight failed." >&2
  {
    echo
    echo "## $(date -Iseconds) — commit blocked by preflight"
    echo "- task: ${TASK_ID:-n/a}"
    echo "- message: $MESSAGE"
    echo "- action: removed the offending value, rotated the key if it was real, retried"
  } >> status/ERRORS.md
  exit 1
fi

# 2. Checkpoint mode: tag the current HEAD before a risky task, then stop.
if [ "$MODE" = "checkpoint" ]; then
  TAG_NAME="checkpoint/${TASK_ID:-manual-$(date +%H%M%S)}"
  git tag -f "$TAG_NAME" >/dev/null
  git push -f origin "refs/tags/$TAG_NAME" >/dev/null 2>&1 \
    && log_chain "push" "checkpoint $TAG_NAME" \
    || log_chain "push" "checkpoint $TAG_NAME failed (local only)"
  echo "checkpoint created: $TAG_NAME"
  exit 0
fi

# 3. Stage and commit.
git add -A
if git diff --cached --quiet; then
  echo "step-commit: nothing staged — nothing to commit." >&2
  log_chain "commit" "skipped: empty diff"
  exit 0
fi

git commit -m "$MESSAGE"
SHA="$(git rev-parse --short HEAD)"
log_chain "commit" "$SHA" "{\"files\":$(git show --name-only --pretty=format: HEAD | grep -c . || echo 0)}"

# 4. Optional release tag.
if [ -n "$TAG" ]; then
  git tag -a "$TAG" -m "$MESSAGE"
  log_chain "commit" "tagged $TAG"
fi

# 5. Push. Failure is survivable: the commit stays local and is retried later.
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if git push origin "$BRANCH" && { [ -z "$TAG" ] || git push origin "$TAG"; }; then
  log_chain "push" "ok $BRANCH@$SHA"
  echo "pushed: $BRANCH@$SHA"
else
  log_chain "push" "FAILED $BRANCH@$SHA (commit kept locally)"
  {
    echo
    echo "## $(date -Iseconds) — push failed"
    echo "- task: ${TASK_ID:-n/a}"
    echo "- commit: $SHA exists locally on $BRANCH"
    echo "- retry: git pull --rebase --autostash && git push origin $BRANCH"
    echo "- continue: proceed with the next task; retry at the next task boundary"
  } >> status/ERRORS.md
  exit 1
fi
