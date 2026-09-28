# T-003 — Gradle project skeleton

> Phase 00 · Foundation · **Depends on:** T-002 · **Parallel-safe:** yes · **Est. agent time:** 40-80 min

## Goal

Create the compilable Android project: settings script, version catalog, app module, manifest, and an empty-but-real `MainActivity` that `assembleDebug` accepts.

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

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-003 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-003 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-003: Gradle project skeleton"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

A compilable Android app exists; CI's scaffold gate now executes the Gradle steps for real.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-003.log`.
