# T-002 — Android toolchain and build prerequisites

> Phase 00 · Foundation · **Depends on:** T-001 · **Parallel-safe:** yes · **Est. agent time:** 30-60 min

## Goal

Establish exactly which JDK, Android SDK components and Gradle wrapper the project needs, and document how to satisfy them both on the phone (Termux/proot-Debian) and in CI.

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

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-002 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-002 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-002: Android toolchain and build prerequisites"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Toolchain documented and pinned; a builder knows exactly what to install before the first compile.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-002.log`.
