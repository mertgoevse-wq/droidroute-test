# T-168 — Migration importers from other routers

> Phase 13 · Competitive absorption & Android edge · **Depends on:** T-024, T-033 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Import an existing router configuration so switching is a paste: OmniRoute, 9Router, LiteLLM, one-api/new-api and CLIProxyAPI formats, with secrets flagged rather than imported silently.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `droidroute-provider-manifest` | the real config shapes of each tool, and what maps cleanly to a manifest |
| `droidroute-verification` | fixtures per format, including a file with embedded secrets |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `provider/import/Importer.kt` with one parser per supported tool
- An import report: what was recognised, what was skipped, and what needs the owner's key

## Steps

1. Parse each format into the internal model without inventing fields that the source did not contain.
2. Detect embedded credentials and move them to the vault instead of copying them into an importable manifest file.
3. Report unmapped settings explicitly rather than dropping them silently.
4. Test with fixtures for each format, including a partially broken file.

## Acceptance criteria

- [ ] Each supported format imports its providers with correct base URLs (asserted per fixture)
- [ ] A credential found in the source is stored in the vault and never written to disk
- [ ] Unrecognised entries are listed in the report, not dropped

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Importer*'
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-168 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-168 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-168: Migration importers from other routers"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Moving from a competitor is a paste with a report, not a weekend of retyping.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-168.log`.
