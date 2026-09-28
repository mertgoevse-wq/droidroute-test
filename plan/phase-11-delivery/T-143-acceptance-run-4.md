# T-143 — Acceptance run A10–A12 (handover, build, hygiene)

> Phase 11 · Delivery · **Depends on:** T-142, T-133 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Prove the last three criteria, including that a different model can take over from the repository alone.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `testing` | the takeover drill must be genuinely cold, with no session memory |
| `ci-cd-github-actions` | verify the artifact path end to end from the workflow run |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Evidence entries for A10, A11 and A12

## Steps

1. A10: in a fresh session, complete one task end to end using only repository artefacts.
2. A11: download the CI-built APK, install it on the device, and run the local build once as the fallback proof.
3. A12: run the secrets preflight, confirm the cleanup workflow ran, and check every README link.
4. Record all of it in the task log.

## Acceptance criteria

- [ ] A10, A11 and A12 are ticked with evidence
- [ ] The takeover was done without consulting any chat history
- [ ] The APK installed from CI runs the same build sha that `/health` reports

## Verification

```bash
gh run list --workflow=build-apk.yml --limit 3
python3 tools/check_links.py
scripts/preflight-secrets.sh
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-143 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-143 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-143: Acceptance run A10–A12 (handover, build, hygiene)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

All twelve acceptance criteria are satisfied with evidence.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-143.log`.
