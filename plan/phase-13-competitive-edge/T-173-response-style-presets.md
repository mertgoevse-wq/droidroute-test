# T-173 — Response-style presets (terse and minimal-code), opt-in

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-153, T-066 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Offer the brevity modes competitors inject by default — terse answers, minimal YAGNI-first code — as explicit, opt-in presets with a hard carve-out for safety, validation and anything the owner asked for.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-verification` | prove the preset never overrides an explicit instruction and never strips safety guidance |
| `ai-governors` | a style mode that changes answers without consent is a defect; make the boundary visible |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Presets `off` (default), `concise`, `minimal-code` with documented injected text
- Per-alias and per-request selection; the preset used is reported in the response headers

## Steps

1. Write each preset's injected instruction as a file, reviewed like code, with the carve-outs stated inline.
2. Default to `off` and require an explicit selection per alias or per request.
3. Guarantee that an explicit owner instruction wins over the preset (asserted with a fixture).
4. Report the active preset so the owner can see why an answer came back terse.

## Acceptance criteria

- [ ] Default is `off` and no request gets a preset it did not ask for (asserted)
- [ ] An explicit instruction in the request is not overridden by the preset (asserted)
- [ ] The active preset is visible in the response headers and the log

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*StylePreset*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-173 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-173 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-173: Response-style presets (terse and minimal-code), opt-in"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Token-saving answer styles exist without silently rewriting the owner's instructions.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-173.log`.
