# T-002 — Android toolchain and build prerequisites

> Phase 00 · Foundation · **Depends on:** T-001 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Establish exactly which JDK, Android SDK components and Gradle wrapper the project needs, and document how to satisfy them both on the phone (Termux/proot-Debian) and in CI.

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
| `gradle-android` | pin JDK 17, AGP 8.7, Kotlin 2.0 and the wrapper version |
| `technical-writing` | write docs/toolchain.md with the exact commands and their pitfalls |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `docs/toolchain.md` — required versions, Termux and Debian install commands, SDK packages, disk and RAM needs
- `gradle/wrapper/gradle-wrapper.properties` pinned to a concrete distribution
- `gradle/libs.versions.toml` version catalog seeded with the pinned versions

## Steps

1. Check the available JDK in Termux/Debian and record the exact package name that provides 17.
2. Write the version catalog with Kotlin, AGP, Compose BOM, Ktor, Room, DataStore, kotlinx.serialization.
3. Document `sdkmanager` package names: platforms;android-35, build-tools, platform-tools.
4. Record the realistic constraints: build time on the A56, storage for the Gradle cache, thermal throttling.

## Acceptance criteria

- [ ] `java -version` reports 17 (or the document names the exact command that achieves it)
- [ ] `gradle/libs.versions.toml` parses and contains every version the plan references
- [ ] `docs/toolchain.md` lists no version that contradicts `docs/11-tbc-resolutions.md` TBC-3

## Verification

```bash
java -version
grep -c '=' gradle/libs.versions.toml
python3 -c "import tomllib,pathlib;tomllib.loads(pathlib.Path('gradle/libs.versions.toml').read_text())"
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-002.log`)
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

- `scripts/log-step.sh T-002 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-002 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-002: Android toolchain and build prerequisites"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Toolchain documented and pinned; a builder knows exactly what to install before the first compile.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-002.log`.
