# T-108 — llama.cpp runtime resolution

> Phase 08 · Local models · **Depends on:** T-107 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Resolve a working llama.cpp runtime in the documented order and record which path won.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `local-inference` | the three resolution paths and their real failure modes |
| `technical-writing` | an honest statement of what each path costs in download and time |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `local/RuntimeResolver.kt` — package, build-from-source, prebuilt, each with a probe
- A UI-facing explanation when none resolves, naming which step failed

## Steps

1. Probe `llama-server --version` for each candidate path in order and record the version.
2. For the build path, generate a script in the Debian environment and capture its output.
3. For the prebuilt path, download and verify before offering it.
4. Persist the winning path and re-probe on demand, never on every request.

## Acceptance criteria

- [ ] A working runtime is found or the failure names the exact missing prerequisite
- [ ] The resolved version and path are visible in the UI and in `/health`
- [ ] No binary is bundled in the APK

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*RuntimeResolver*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-108 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-108 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-108: llama.cpp runtime resolution"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Local inference has a real runtime with a recorded provenance.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-108.log`.
