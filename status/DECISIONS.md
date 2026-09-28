# Decisions

Design decisions that are **settled**. Do not re-open one without a new entry that supersedes it and names the reason. Runtime data does not belong here — this is the "why" record.

## Format

```
### D-0xx — <decision>
- date: YYYY-MM-DD
- context: what forced a choice
- decision: what was chosen
- alternatives: what was rejected, and why
- consequences: what this makes easy or hard later
```

---

### D-001 — Android-native in Kotlin + Jetpack Compose
- **date:** 2026-09-28
- **context:** The owner wants an OmniRoute-equivalent gateway that runs as a real app on a Galaxy A56, not a Node service in Termux.
- **decision:** Kotlin 2.0 + Jetpack Compose, Material 3, single-module app in v1 with clean package boundaries.
- **alternatives:** Flutter and React Native (rejected: a reliable long-running background server needs a platform-level foreground service, and Flutter/RN would still need a Kotlin plugin layer); a Termux-only shell service (rejected: no UI, no Keystore, no app lifecycle).
- **consequences:** Best battery and background behaviour; slower to build than a cross-platform UI. All UI work must be Compose-native.

### D-002 — Foreground service with a persistent notification
- **date:** 2026-09-28
- **context:** Android kills background processes aggressively; the gateway must survive while the owner uses other apps.
- **decision:** `startForeground` with a `dataSync` service type and an ongoing notification showing port, bind mode and request count.
- **alternatives:** Battery-optimisation exemption as a requirement (rejected as a hard requirement — fragile across OEMs); WorkManager (rejected: not for long-lived listeners).
- **consequences:** No hidden settings the owner must find. `POST_NOTIFICATIONS` becomes a first-run permission request.

### D-003 — Default port 8787, user-configurable
- **date:** 2026-09-28
- **context:** OmniRoute's default is 20128; the owner wants both usable during migration and wants to choose the port himself.
- **decision:** Default 8787, editable in Settings, persisted in DataStore, validated against the 1024–65535 range and against collisions.
- **alternatives:** Reusing 20128 (rejected: needless collision with a running OmniRoute).
- **consequences:** `scripts/termux-setup.sh --port` must be re-run after a port change; the app shows the exact commands to copy.

### D-004 — Key vault in Android Keystore, mask 5/5, reveal once
- **date:** 2026-09-28
- **context:** The phone will hold many provider credentials for a long-running unattended agent.
- **decision:** AES-256-GCM with a Keystore-wrapped key; plaintext shown once at entry; afterwards `first5••••last5`; a second reveal requires device-credential confirmation; clipboard clears after 60 s.
- **alternatives:** `EncryptedSharedPreferences` (rejected: deprecated API surface); plaintext files (rejected outright).
- **consequences:** A key cannot be recovered from the phone without the device credential; the owner needs the export feature for device migration.

### D-005 — Secrets never enter the repository
- **date:** 2026-09-28
- **context:** Logs and status files are pushed continuously by an autonomous agent.
- **decision:** Manifest examples carry placeholders only; a redactor runs on every log line and API response; `scripts/preflight-secrets.sh` blocks any commit matching known key shapes.
- **alternatives:** Encrypted key backup committed to the repo (rejected by the owner — a private repo can still leak).
- **consequences:** Device migration uses a local encrypted export, not the repository.

### D-006 — One task file = one commit on `main`
- **date:** 2026-09-28
- **context:** The chain must be resumable by a different model at any point.
- **decision:** Subject `T-0xx: <task title>`, one commit per task, checkpoint tags before risky tasks, no branches, no force-push.
- **alternatives:** Feature branches with PRs (rejected: the agent would review its own work; more ceremony per task with no review value).
- **consequences:** `git log` maps 1:1 to the plan and is the primary resume index.

### D-007 — Four protocol surfaces on one port
- **date:** 2026-09-28
- **context:** Agents speak different dialects; the owner wants Google software to connect directly too.
- **decision:** OpenAI (`/v1/*`), Anthropic (`/v1/messages`), Gemini (`/v1beta/*`), plus DroidRoute-native helper endpoints, all on one port with one auth gate.
- **alternatives:** Separate ports per format (rejected: more configuration for the owner, more listeners to keep alive).
- **consequences:** One router engine must normalise three shapes; the protocol layer is the biggest single module.

### D-008 — Local models out-of-process via Termux in v1
- **date:** 2026-09-28
- **context:** An embedded llama.cpp (JNI) build is weeks of work and bloats the APK; the owner already runs Termux.
- **decision:** Resolve llama.cpp in Termux/Debian, manage it as an external process, register it as a normal provider. Embedded runtime is a post-v1 spike with a recorded go/no-go.
- **alternatives:** Embedded-only (rejected for v1); skip local models (rejected — the owner asked for them as a feature).
- **consequences:** The app and Termux must both run for local inference; the Termux bridge (RUN_COMMAND intent) becomes a hard dependency for that feature only.

<!-- Append new decisions above this line, newest last. -->
