# T-003 — Gradle project skeleton

> Phase 00 · Foundation · **Depends on:** T-002 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Create the compilable Android project: settings script, version catalog, app module, manifest, and an empty-but-real `MainActivity` that `assembleDebug` accepts.

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
| `gradle-android` | author settings.gradle.kts, build.gradle.kts, the app manifest and signing config seams |
| `android-compose-ui` | wire a minimal MainActivity with a Material 3 theme |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `settings.gradle.kts`, root and app `build.gradle.kts`
- `app/src/main/AndroidManifest.xml` with applicationId, minSdk 26, target/compile 35
- `app/src/main/kotlin/com/droidroute/app/MainActivity.kt` + theme package
- `gradlew`, `gradlew.bat`, wrapper jar

## Steps

1. Create the Gradle files referencing the version catalog, no hard-coded versions.
2. Declare the app manifest: INTERNET, FOREGROUND_SERVICE, FOREGROUND_SERVICE_DATA_SYNC, POST_NOTIFICATIONS.
3. Add a minimal Compose entry point that renders an honest 'not configured yet' state — no lorem text.
4. Set `applicationId com.droidroute.app`, `versionCode 1`, `versionName 0.1.0`.
5. Run `./gradlew :app:assembleDebug` and fix every warning that indicates a real misconfiguration.

## Acceptance criteria

- [ ] `./gradlew :app:assembleDebug` succeeds
- [ ] `./gradlew :app:lintDebug` reports no errors
- [ ] APK exists under `app/build/outputs/apk/debug/`
- [ ] No version string is hard-coded outside the version catalog

## Verification

```bash
./gradlew :app:assembleDebug
./gradlew :app:lintDebug
ls app/build/outputs/apk/debug/
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-003.log`)
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

- `scripts/log-step.sh T-003 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-003 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-003: Gradle project skeleton"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A compilable Android app exists; CI's scaffold gate now executes the Gradle steps for real.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-003.log`.
