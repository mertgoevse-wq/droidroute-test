# Build & Release

## Primary path — GitHub Actions

`.github/workflows/build-apk.yml` builds a debug APK on every push to `main` and a signed release APK on every `v*` tag.

| Job | Trigger | Output |
|---|---|---|
| `verify` | every push / PR | `./gradlew lint testDebugUnitTest`, secrets preflight, markdown link check |
| `apk-debug` | push to `main` | artifact `droidroute-debug-<sha>.apk`, retained 14 days |
| `apk-release` | tag `v*` | signed APK + SHA-256 + auto-generated release notes |

Downloading on the phone: open the run page → Artifacts → install. No Android SDK needed on the device for this path.

Signing keys live in repository secrets (`SIGNING_KEYSTORE_BASE64`, `SIGNING_STORE_PASSWORD`, `SIGNING_KEY_ALIAS`, `SIGNING_KEY_PASSWORD`) and are **never** committed. Unsigned debug builds remain installable for the owner's own testing.

## Fallback path — on the phone (Termux)

`scripts/build-apk-local.sh` mirrors the CI steps inside Termux/proot-Debian:

```bash
pkg install openjdk-17 gradle git
# or inside proot-Debian:
apt-get install -y openjdk-17-jdk unzip
./gradlew :app:assembleDebug
```

Expectations to document honestly in the script's output:

- 10–30 minutes per build on the A56, with noticeable heat and battery drain.
- 4+ GB of free storage for the Gradle cache.
- Run it with the charger connected and the screen off; Gradle daemon memory is the main pressure point.
- If `assembleDebug` is killed by Android's low-memory killer, re-run with `--no-daemon -Dorg.gradle.jvmargs=-Xmx1536m`.

## Versioning

- `versionName` follows `MAJOR.MINOR.PATCH`; `versionCode` is monotonically increasing (`major*10000 + minor*100 + patch`).
- `CHANGELOG.md` is updated in the same commit as the version bump.
- The `v*` tag is created by `scripts/step-commit.sh --tag` only when the chain reaches a delivery task.

## Install instructions (for the owner, and for a future agent)

1. Enable "Install unknown apps" for the browser/file manager.
2. Install the APK.
3. First launch: grant notification permission, then open Settings → set port (default 8787) and bind mode (default local only).
4. Add at least one provider (one-click for a free gateway) and validate it.
5. In Termux: `export ANTHROPIC_BASE_URL=http://127.0.0.1:8787` and `export OPENAI_BASE_URL=http://127.0.0.1:8787/v1`, then start Claude Code / Freebuff.
6. Optional: enable the Termux integration so DroidRoute can start local models and read MCP configs.

`scripts/termux-setup.sh` performs step 5 (and can write the exports into `~/.bashrc` with `--persist`).

## Rollback

- App: keep the previous APK; Android's package installer upgrades in place, and `v*` releases keep older artifacts for 90 days.
- Data: vault and database live in app-private storage; "export configuration" writes a manifest bundle (no secrets) and "export keys" writes an encrypted, password-protected archive the owner can move to a new device.
