#!/usr/bin/env bash
# build-apk-local.sh — build the APK on the phone when CI is not an option.
#
# Reality check for a Galaxy A56:
#   10-30 minutes per build, noticeable heat, 4+ GB free storage for the
#   Gradle cache. Charge the phone, expect the fan-less thermal limit.
#
#   scripts/build-apk-local.sh              # debug build
#   scripts/build-apk-local.sh --release    # release build (needs signing config)
#   scripts/build-apk-local.sh --clean
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

VARIANT="Debug"
CLEAN=0
EXTRA_ARGS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --release) VARIANT="Release"; shift ;;
    --clean)   CLEAN=1; shift ;;
    *) EXTRA_ARGS+=("$1"); shift ;;
  esac
done

echo "DroidRoute local build — variant $VARIANT"

# --- environment checks ------------------------------------------------------
missing=0
for tool in java git; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "  missing: $tool" >&2
    missing=1
  fi
done
[ "$missing" -eq 1 ] && {
  echo ""
  echo "Install the toolchain first:"
  echo "  Termux:        pkg install openjdk-17 git"
  echo "  proot-Debian:  apt-get install -y openjdk-17-jdk git"
  exit 1
}

if [ -n "${ANDROID_HOME:-}" ] || [ -n "${ANDROID_SDK_ROOT:-}" ]; then
  echo "  Android SDK: ${ANDROID_HOME:-$ANDROID_SDK_ROOT}"
else
  echo "  note: no ANDROID_HOME set — the Gradle wrapper will fetch what it needs"
  echo "        (first run downloads the SDK; make sure you are on Wi-Fi)"
fi

free_kb="$(df -Pk . | awk 'NR==2 {print $4}')"
free_gb=$((free_kb / 1024 / 1024))
echo "  free storage: ${free_gb} GB"
if [ "$free_gb" -lt 4 ]; then
  echo "  WARNING: under 4 GB free — Gradle may fail. Free space first." >&2
fi

export GRADLE_OPTS="${GRADLE_OPTS:--Xmx1536m -Dfile.encoding=UTF-8}"

if [ "$CLEAN" -eq 1 ]; then
  echo "  cleaning build output…"
  ./gradlew clean
fi

echo "  building… (this is the slow part)"
set +e
./gradlew ":app:assemble${VARIANT}" --no-daemon \
  -Dorg.gradle.jvmargs="${GRADLE_OPTS}" \
  "${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}"
status=$?
set -e

if [ "$status" -ne 0 ]; then
  cat <<'EOF'

Build failed. Common causes on this device:
  - low memory: retry with --no-daemon -Dorg.gradle.jvmargs=-Xmx1536m
  - missing SDK: install the Android SDK components or use the CI build
  - disk full: ./gradlew clean, then free space
Record the failure in status/ERRORS.md before retrying.
EOF
  exit "$status"
fi

APK="$(find app/build/outputs/apk -name "*.apk" -newermt '-30 minutes' | head -1 || true)"
echo ""
echo "build finished."
if [ -n "$APK" ]; then
  echo "  apk: $APK"
  echo "  size: $(du -h "$APK" | cut -f1)"
  echo "  install: open it in the file manager, or: adb install -r \"$APK\""
else
  echo "  no fresh APK found — check app/build/outputs/apk/"
fi
