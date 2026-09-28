# T-107 — Termux bridge (RUN_COMMAND intent with HTTP fallback)

> Phase 08 · Local models · **Depends on:** T-103, T-022 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Give the app one way to run things inside Termux/Debian: the documented RUN_COMMAND intent, usable for llama.cpp and for reading MCP configuration.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-platform` | permission handling, intent construction, exit-code propagation through TermuxService |
| `security-audit` | an intent that runs shell commands deserves a strict command allow-list |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `bridge/TermuxBridge.kt` with `run(command, args)`, availability probe and a typed result
- A command allow-list so the bridge cannot become a remote shell
- `scripts/termux-bridge-helper.sh` as the receiving side, installed by the owner

## Steps

1. Implement the intent call, including the background flag and the result callback.
2. Allow-list the commands the app may run (llama-server, whisper, cat of specific config paths).
3. Return a typed result: success with stdout, failure with stderr and exit code.
4. Test on the device; when Termux is absent, fail with a clear message instead of an exception.

## Acceptance criteria

- [ ] A command runs and its output returns to the app
- [ ] A command outside the allow-list is refused with a specific message
- [ ] Without Termux installed, the caller receives `unavailable`, not a crash

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*TermuxBridge*'
bash scripts/termux-bridge-helper.sh --selftest
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-107 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-107 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-107: Termux bridge (RUN_COMMAND intent with HTTP fallback)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The app can drive the Linux environment it lives next to, within a narrow allow-list.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-107.log`.
