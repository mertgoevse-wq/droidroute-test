# Toolchain — build prerequisites

Exactly what a builder needs before the first compile. Versions are pinned by
[TBC-3](11-tbc-resolutions.md) and mirrored one-to-one in
[`gradle/libs.versions.toml`](../gradle/libs.versions.toml) — that catalog is
the single source of truth; this document explains how to get there.

## Pinned versions (TBC-3)

| Component | Version | Where pinned |
|---|---|---|
| JDK | 17 (Temurin) | this page |
| Gradle wrapper | 8.10.2 | `gradle/wrapper/gradle-wrapper.properties` |
| AGP | 8.7.3 | `libs.versions.toml` |
| Kotlin | 2.0.21 | `libs.versions.toml` |
| Compose BOM | 2024.09.03, Material 3 | `libs.versions.toml` |
| Ktor | 3.0.3, CIO engine | `libs.versions.toml` |
| Room / DataStore | 2.6.1 / 1.1.1 | `libs.versions.toml` |
| kotlinx.serialization | 1.7.3 | `libs.versions.toml` |

## JDK

The build needs **JDK 17**. AGP 8.7 does not accept JDK 21 for `lintDebug` in
all setups; 17 is the safe pin.

| Environment | Command |
|---|---|
| Debian / proot-Debian | `sudo apt-get install -y openjdk-17-jdk-headless` |
| Termux | `pkg install openjdk-17` |
| CI (GitHub Actions) | `actions/setup-java` with `distribution: temurin`, `java-version: 17` |

Check: `java -version` must report `17.x`. If a machine has several JDKs, set
`org.gradle.java.home` in `gradle.properties` or `JAVA_HOME` — do not rely on PATH order.

## Android SDK packages

`sdkmanager` package names, exactly as the build references them:

| Package | Used for |
|---|---|
| `platform-tools` | adb, fastboot |
| `platforms;android-35` | `compileSdk 35` / `targetSdk 35` |
| `build-tools;35.0.0` | aapt2, d8, apksigner |

One-shot install (Debian/CI):

```bash
yes | sdkmanager --sdk_root="$ANDROID_HOME" \
  "platform-tools" "platforms;android-35" "build-tools;35.0.0"
```

`ANDROID_HOME` must point at the SDK root; Gradle reads it via `local.properties`
(`sdk.dir=`) or the environment variable. `local.properties` is machine-local and
git-ignored — never commit it.

## Disk and RAM needs

| Item | Realistic size |
|---|---|
| Android SDK (platform 35 + build-tools + platform-tools) | ~1.5 GB |
| Gradle caches (~/.gradle) after a full build | ~2–3 GB |
| One `assembleDebug` output + intermediates | ~300 MB |
| Plan **at least 8 GB free** on the device before the first build. | |

First `assembleDebug` downloads the Gradle distribution (~130 MB) plus all
Maven dependencies — expect several minutes on the A56, and **thermal
throttling** on long repeated builds. Build with the device on a flat surface,
screen off; prefer `--offline` for rebuilds once dependencies are cached.

## Termux notes

Building directly in Termux is possible but slow; the plan's canonical path is
proot-Debian (see `scripts/termux-setup.sh`). Inside proot-Debian use the
Debian commands above. Direct Termux builds need `openjdk-17`, the Android
SDK via `sdkmanager` with `--sdk_root` set under Termux's home, and ~4 GB of
RAM headroom or the Kotlin daemon will be OOM-killed.

## Verification

```bash
java -version            # 17.x
grep -c '=' gradle/libs.versions.toml   # > 0 — catalog present
python3 -c "import tomllib,pathlib;tomllib.loads(pathlib.Path('gradle/libs.versions.toml').read_text())"  # parses
```
