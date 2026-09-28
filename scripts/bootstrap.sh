#!/usr/bin/env bash
# DroidRoute — bootstrap a fresh clone.
#
#   bash scripts/bootstrap.sh
#
# Checks the tools this repository needs, refreshes the agent tooling inventory,
# and runs every checker. Idempotent: running it twice changes nothing.
#
# It does not install anything, does not touch the network, and does not write
# outside this repository. If a check fails, nothing else runs and the reason is
# printed — fix that, then run it again.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

pass() { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }
fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; }
step() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# --- 1. Are we where we think we are? ---------------------------------------
step "1. Repository"
for marker in AGENTS.md plan/INDEX.md tools/generate_plan.py scripts/preflight-secrets.sh; do
  if [[ -e "$marker" ]]; then
    pass "$marker"
  else
    fail "$marker is missing — this does not look like the DroidRoute repository"
    exit 1
  fi
done
printf '     root: %s\n' "$ROOT"

# --- 2. Are the tools present? ---------------------------------------------
step "2. Tools"
if command -v git >/dev/null 2>&1; then
  pass "git $(git --version | awk '{print $3}')"
else
  fail "git is not on PATH"
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  py_ok="$(python3 -c 'import sys; print(1 if sys.version_info >= (3, 9) else 0)')"
  if [[ "$py_ok" == "1" ]]; then
    pass "python3 $(python3 -c 'import platform; print(platform.python_version())')"
  else
    fail "python3 is older than 3.9 — the checkers need 3.9 or newer"
    exit 1
  fi
else
  fail "python3 is not on PATH (Termux: pkg install python)"
  exit 1
fi

if command -v gh >/dev/null 2>&1; then
  pass "gh $(gh --version 2>/dev/null | head -1 | awk '{print $3}')"
else
  warn "gh is not installed — local checks work, but pushing and release tasks will not"
fi

if command -v node >/dev/null 2>&1; then
  pass "node $(node --version)"
else
  warn "node is not installed — the launch video (T-201) needs Node 22+ and FFmpeg"
fi

# --- 3. Working tree --------------------------------------------------------
step "3. Working tree"
if [[ -n "$(git status --porcelain 2>/dev/null || true)" ]]; then
  warn "uncommitted changes present:"
  git status --short | sed 's/^/     /'
  warn "that is fine locally, but commit before starting a task"
else
  pass "clean"
fi

# --- 4. Tooling inventory ---------------------------------------------------
step "4. Agent tooling inventory"
if python3 scripts/discover_tooling.py --check-fresh >/dev/null 2>&1; then
  pass "status/TOOLING.md matches this machine"
else
  if python3 scripts/discover_tooling.py --check >/dev/null 2>&1; then
    echo "     refreshing the inventory for this machine:"
    python3 scripts/discover_tooling.py | sed 's/^/     /'
    pass "regenerated — commit the change if it differs"
  else
    fail "the inventory is malformed — run: python3 scripts/discover_tooling.py"
    exit 1
  fi
fi

# --- 5. Every checker -------------------------------------------------------
step "5. Checks"
if python3 tools/check_plan_consistency.py --quiet; then
  pass "plan, links, skill labels, design, secrets and counts"
else
  fail "a check failed — see the output above"
  exit 1
fi

if bash scripts/preflight-secrets.sh >/dev/null 2>&1; then
  pass "secrets preflight clean"
else
  fail "the secrets preflight failed — do not commit until it is clean"
  exit 1
fi

for script in scripts/*.sh; do
  bash -n "$script" || { fail "syntax error in $script"; exit 1; }
done
pass "all shell scripts parse"

# --- 6. Where to go next ----------------------------------------------------
step "6. Next"
tasks="$(find plan -name 'T-*.md' | wc -l | tr -d ' ')"
phases="$(find plan -maxdepth 1 -type d -name 'phase-*' | wc -l | tr -d ' ')"
printf '     plan: %s tasks in %s phases\n' "$tasks" "$phases"
if [[ -f status/NEXT.md ]]; then
  next_line="$(grep -m1 -o 'T-[0-9]\{3,4\}' status/NEXT.md || true)"
  [[ -n "${next_line:-}" ]] && printf '     next task: %s (see status/NEXT.md)\n' "$next_line"
fi
printf '     code word: %s (see KICKOFF.md)\n' "$(grep -m1 -o '`[A-Za-z]*-[0-9]*`' KICKOFF.md | tr -d '`' || echo '(see KICKOFF.md)')"

step "Ready"
echo "     Start your agent in this directory and give it the code word from KICKOFF.md."
