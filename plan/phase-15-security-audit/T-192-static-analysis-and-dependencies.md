# T-192 — Static analysis, dependencies and licences

> Phase 15 · Security & privacy audit · **Depends on:** T-009, T-136, T-144 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Know the supply chain: enable the platform's security analysis, pin every dependency, and give every one a version, a licence, a reason and a maintenance signal.

## Read first (context budget)

- [`status/NEXT.md`](../../status/NEXT.md) — the next task and the pre-flight commands
- [`status/ERRORS.md`](../../status/ERRORS.md) — must have no open entry for this task
- [`handbooks/09-skill-resolution.md`](../../handbooks/09-skill-resolution.md) — what each skill label below means on this machine
- [`docs/11-tbc-resolutions.md`](../../docs/11-tbc-resolutions.md) — decisions already settled; not re-opened
- this file, top to bottom, plus the *Acceptance criteria* of every `Depends on` task

Do not read the rest of the plan to "get oriented" — the entry point is this file plus the documents linked here. If the work genuinely needs another document, read that one and nothing more.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `gradle-android` | lint configuration, dependency verification, publishing checksums |
| `security-audit` | distinguishing a real advisory from a version-CVE false positive |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `docs/17-security-audit.md` — the static-analysis and dependency section
- A dependency table: coordinate, version, licence, purpose, last release date, maintenance signal
- Dependency verification (checksums) enabled, or a written reason why it cannot be

## Steps

1. Turn on the platform security lint checks and make new findings fail the build rather than warn.
2. Replace every dynamic version range with an exact version, and verify the dependency checksum set.
3. List each dependency's licence and purpose; flag anything unmaintained or licence-incompatible and decide it explicitly.
4. Check whether any dependency is used for one small thing while the platform already provides it — remove it or justify it.

## Acceptance criteria

- [ ] No dynamic version specifier (`+`, `latest`, ranges) remains in the build files
- [ ] Every dependency has a licence and a stated purpose in the table
- [ ] Security lint checks are enabled and fail the build on a new finding (proven once, then reverted)
- [ ] The audit section names the tooling used and its limitations (an offline device cannot query an advisory database live)

## Verification

```bash
./gradlew :app:lintDebug
grep -rn '+\"\|latest.release\|versionRange' gradle/ app/build.gradle.kts build.gradle.kts | grep -v '^\s*//' || echo 'no dynamic versions'
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-192.log`)
- [ ] No placeholder, no invented endpoint/URL/model/field, no edit outside the files this task names
- [ ] Nothing was weakened to make a check pass (no deleted test, no raised threshold, no disabled rule)
- [ ] `status/PROGRESS.md` and `status/NEXT.md` updated in the same commit as the work
- [ ] `scripts/preflight-secrets.sh` clean
- [ ] UI work only: `python3 tools/check_design_slop.py` passes and the four craft tests ran ([docs/14-design-system.md](../../docs/14-design-system.md) §11)

## Rules that always apply

- Prohibitions and the quality bar: [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) (placeholders, invented endpoints, unrequested scope, weakened checks)
- At least two skills **in parallel** as subagents, one of them verification: [AGENTS.md](../../AGENTS.md) §4
- Log every meaningful step, commit and push exactly once for this task: [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md) · [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md)
- No secret in the repository, ever: `scripts/preflight-secrets.sh` must pass
- A new dependency, a deviation, or a settled decision goes into [status/DECISIONS.md](../../status/DECISIONS.md) in the same commit
- Missing tool for the job? Search before improvising: [handbooks/08-tooling-discovery.md](../../handbooks/08-tooling-discovery.md)

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-192 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-192 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-192: Static analysis, dependencies and licences"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The supply chain is pinned, licensed and documented, with the limits of the audit stated.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-192.log`.
