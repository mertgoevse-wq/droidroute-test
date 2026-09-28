# T-163 — A2A server for agent delegation

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-120, T-151 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Let other agents delegate to the DroidRoute fleet: advertise capabilities on an agent card and accept inbound A2A tasks.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `ai-trust-builders` | delegation is a trust boundary: what is advertised, what is accepted, what is refused |
| `ai-governors` | inbound autonomy needs limits and an audit trail the owner can inspect |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `server/a2a/AgentCard.kt` and the inbound task endpoint
- An audit record per delegated task, naming the requester and the outcome

## Steps

1. Publish an agent card listing the capabilities DroidRoute will actually perform, with no overstatement.
2. Accept inbound tasks only from configured clients and inside the budget rules from T-155.
3. Record every delegated task in the log with requester, cost and outcome.
4. Refuse anything outside the advertised capability set with a specific error.

## Acceptance criteria

- [ ] The agent card matches the implemented capabilities
- [ ] An unconfigured requester is rejected and the attempt is logged
- [ ] Every accepted delegation produces an audit record

## Verification

```bash
curl -fsS http://127.0.0.1:8787/.well-known/agent-card
./gradlew :app:testDebugUnitTest --tests '*AgentCard*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-163 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-163 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-163: A2A server for agent delegation"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

DroidRoute can act as a controlled delegate inside an agent fleet.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-163.log`.
