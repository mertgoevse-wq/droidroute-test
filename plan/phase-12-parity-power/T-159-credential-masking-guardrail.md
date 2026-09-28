# T-159 — Credential-masking guardrail

> Phase 12 · OmniRoute parity & power features · **Depends on:** T-008, T-066 · **Parallel-safe:** yes · **Est. agent time:** 90-180 min

## Goal

Redact secrets that would otherwise flow outwards in prompts or back in responses, using the same rules as the repository's own redactor.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `android-intent-security` | treat every outbound path as hostile until proven filtered |
| `droidroute-verification` | canary tests in both directions plus a false-positive check on ordinary code |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `protocol/guard/CredentialMasker.kt` shared with the logging redactor's pattern set
- A documented note about false positives and how to see what was masked

## Steps

1. Reuse one pattern source for log redaction and outbound masking so the two cannot drift.
2. Mask in both directions and log the occurrence by type only, never the value.
3. Test false positives against real code samples: masking must not mangle ordinary identifiers.
4. Document the feature's off switch and its default.

## Acceptance criteria

- [ ] A canary key is masked in outbound content and in inbound content (asserted)
- [ ] Ordinary code samples pass through unchanged (asserted)
- [ ] The masking event is logged by type, never by value

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*CredentialMasker*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-159 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-159 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-159: Credential-masking guardrail"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A leaked key in a prompt does not become a leaked key in a response, and the rule has one source.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-159.log`.
