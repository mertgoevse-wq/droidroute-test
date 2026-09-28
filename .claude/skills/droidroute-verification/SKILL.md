---
name: droidroute-verification
description: Run the verification workstream for a DroidRoute task - try to falsify the implementation, cover the error paths the task names, and produce raw evidence for the log. Use as the second (mandatory) parallel workstream in every task, or when asked to verify, prove, or check a claim in this repository.
---

# Verification workstream

Your job is **not** to confirm the implementation. It is to break it, and only then to report.

## 1. Read the acceptance criteria as test cases

Each `- [ ]` line in the task file becomes at least one check. If a line cannot be turned into a check, say so and propose a rewording — vague criteria are as much a defect as failing code.

## 2. Cover the error paths the task names

Typical set for this project:

| Area | What to force |
|---|---|
| Provider adapters | 401, 429, 500, timeout, truncated stream, malformed JSON, HTML error page |
| Routing | quota exhausted, parked key, breaker open, mid-stream failure, alias cycle |
| Server/auth | missing key, wrong key, non-local bind, admin route without auth |
| Keys | masking, reveal-once, canary (no key value in any log line) |
| Local models | oversized model warning, crashed process, port release on unload |
| MCP | dead server, hung stdio server, malformed config file |

## 3. Never weaken the check

If a test fails: fix the cause. Do not delete the test, add `@Ignore`, lower a threshold, or disable the secrets preflight. If the check itself is wrong, change it in its own task and record why in `status/DECISIONS.md`.

## 4. Produce evidence, not summaries

```bash
scripts/log-step.sh T-0xx "test" "./gradlew :app:testDebugUnitTest --tests '*QuotaLedger*'" "pass" --actor verify --dur 4210
```

The log line is the evidence. A claim without a command and its raw result is not verification.

## 5. Report in this shape

```
workstream: verify
status: pass | fail | blocked
files: <tests written>
evidence: <command> -> <result>
notes: <what is still untested and why>
```

## 6. Two things that are always part of verification here

- `scripts/preflight-secrets.sh` — a canary must never reach a commit.
- `python3 tools/check_links.py` and `python3 tools/generate_plan.py --check` when documents or the plan changed.
