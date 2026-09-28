"""Phase 00 — Foundation: prove the tooling, scaffold the project, make CI honest."""

from common import Phase, Task

PHASE = Phase(
    number=0,
    slug="foundation",
    title="Foundation",
    summary="Toolchain, Gradle scaffold, storage and vault foundations, and CI that tells the truth.",
)

TASKS = [
    Task(
        id=1,
        slug="repository-hygiene",
        title="Repository hygiene and baseline checks",
        goal=(
            "Make the tooling trustworthy before any app code exists. Every script in scripts/ "
            "runs cleanly, the secrets preflight blocks a planted key, the step logger writes a "
            "well-formed record, and the CI workflows are green on the current tree."
        ),
        deps=[],
        est="20-40 min",
        skills=[
            ("git-workflow", "exercise the commit/tag/push path and the ignore rules"),
            ("testing", "plant a fake key and prove the preflight rejects it"),
        ],
        deliverables=[
            "`logs/chain.log` seeded with a genesis record explaining the scaffold",
            "`status/ERRORS.md` and `status/DECISIONS.md` verified writable by the tooling",
        ],
        steps=[
            "Run `scripts/preflight-secrets.sh`; confirm it scans every tracked and untracked file.",
            "Temporarily add a file containing a `sk-` shaped value, confirm the preflight fails, then remove it.",
            "Run `scripts/log-step.sh T-001 \"verify\" \"preflight\" \"pass\"` and inspect the JSON record.",
            "Run `scripts/weekly-cleanup.sh --dry-run` and confirm it reports without moving anything.",
            "Confirm `.gitignore` keeps build output, keystores, model files and `logs/archive/` out of the tree.",
        ],
        accept=[
            "`scripts/preflight-secrets.sh` exits 0 on the clean tree and 1 on the planted key",
            "`logs/chain.log` contains a well-formed record with `ts`, `task`, `actor`, `action`, `result`",
            "`git status --short` is clean after the commit",
            "Both workflows show a completed run for the pushed commit (or a documented reason why not)",
        ],
        verify=[
            "scripts/preflight-secrets.sh",
            "scripts/weekly-cleanup.sh --dry-run",
            "tail -n 3 logs/chain.log",
        ],
        state="Tooling proven: preflight blocks secrets, logging writes valid JSON records, cleanup is safe, CI is green.",
    ),
    Task(
        id=2,
        slug="android-toolchain",
        title="Android toolchain and build prerequisites",
        goal=(
            "Establish exactly which JDK, Android SDK components and Gradle wrapper the project needs, "
            "and document how to satisfy them both on the phone (Termux/proot-Debian) and in CI."
        ),
        deps=[1],
        est="30-60 min",
        skills=[
            ("gradle-android", "pin JDK 17, AGP 8.7, Kotlin 2.0 and the wrapper version"),
            ("technical-writing", "write docs/toolchain.md with the exact commands and their pitfalls"),
        ],
        deliverables=[
            "`docs/toolchain.md` — required versions, Termux and Debian install commands, SDK packages, disk and RAM needs",
            "`gradle/wrapper/gradle-wrapper.properties` pinned to a concrete distribution",
            "`gradle/libs.versions.toml` version catalog seeded with the pinned versions",
        ],
        steps=[
            "Check the available JDK in Termux/Debian and record the exact package name that provides 17.",
            "Write the version catalog with Kotlin, AGP, Compose BOM, Ktor, Room, DataStore, kotlinx.serialization.",
            "Document `sdkmanager` package names: platforms;android-35, build-tools, platform-tools.",
            "Record the realistic constraints: build time on the A56, storage for the Gradle cache, thermal throttling.",
        ],
        accept=[
            "`java -version` reports 17 (or the document names the exact command that achieves it)",
            "`gradle/libs.versions.toml` parses and contains every version the plan references",
            "`docs/toolchain.md` lists no version that contradicts `docs/11-tbc-resolutions.md` TBC-3",
        ],
        verify=[
            "java -version",
            "grep -c '=' gradle/libs.versions.toml",
            "python3 -c \"import tomllib,pathlib;tomllib.loads(pathlib.Path('gradle/libs.versions.toml').read_text())\"",
        ],
        state="Toolchain documented and pinned; a builder knows exactly what to install before the first compile.",
    ),
    Task(
        id=3,
        slug="gradle-project-skeleton",
        title="Gradle project skeleton",
        goal=(
            "Create the compilable Android project: settings script, version catalog, app module, "
            "manifest, and an empty-but-real `MainActivity` that `assembleDebug` accepts."
        ),
        deps=[2],
        est="40-80 min",
        skills=[
            ("gradle-android", "author settings.gradle.kts, build.gradle.kts, the app manifest and signing config seams"),
            ("android-compose-ui", "wire a minimal MainActivity with a Material 3 theme"),
        ],
        deliverables=[
            "`settings.gradle.kts`, root and app `build.gradle.kts`",
            "`app/src/main/AndroidManifest.xml` with applicationId, minSdk 26, target/compile 35",
            "`app/src/main/kotlin/com/droidroute/app/MainActivity.kt` + theme package",
            "`gradlew`, `gradlew.bat`, wrapper jar",
        ],
        steps=[
            "Create the Gradle files referencing the version catalog, no hard-coded versions.",
            "Declare the app manifest: INTERNET, FOREGROUND_SERVICE, FOREGROUND_SERVICE_DATA_SYNC, POST_NOTIFICATIONS.",
            "Add a minimal Compose entry point that renders an honest 'not configured yet' state — no lorem text.",
            "Set `applicationId com.droidroute.app`, `versionCode 1`, `versionName 0.1.0`.",
            "Run `./gradlew :app:assembleDebug` and fix every warning that indicates a real misconfiguration.",
        ],
        accept=[
            "`./gradlew :app:assembleDebug` succeeds",
            "`./gradlew :app:lintDebug` reports no errors",
            "APK exists under `app/build/outputs/apk/debug/`",
            "No version string is hard-coded outside the version catalog",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "./gradlew :app:lintDebug",
            "ls app/build/outputs/apk/debug/",
        ],
        state="A compilable Android app exists; CI's scaffold gate now executes the Gradle steps for real.",
    ),
    Task(
        id=4,
        slug="package-structure",
        title="Package structure and module boundaries",
        goal=(
            "Lay down the package layout the rest of the plan assumes, with each package owning one "
            "responsibility and a single public entry point, so later tasks never guess where code goes."
        ),
        deps=[3],
        est="30-60 min",
        skills=[
            ("kotlin-core", "create the packages with minimal, honest seams (no empty placeholder classes)"),
            ("technical-writing", "record the layout in docs/01-architecture.md's layer table"),
        ],
        deliverables=[
            "Packages under `com.droidroute`: `server`, `protocol`, `provider`, `routing`, `vault`, `store`, `mcp`, `local`, `bridge`, `ui`, `logging`",
            "One `README.md`-level note per package is not required — the architecture table is the single source",
        ],
        steps=[
            "Create the packages with their first real type only where the task needs it — do not add empty files.",
            "Define shared value types that multiple layers need (RequestId, ProviderId, ModelId, Capability) in their owning package.",
            "Confirm `docs/01-architecture.md` lists exactly these packages and no others.",
        ],
        accept=[
            "Every package named in `docs/01-architecture.md` exists in the source tree",
            "No package contains an empty or placeholder class",
            "`./gradlew :app:assembleDebug` still succeeds",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "find app/src/main/kotlin/com/droidroute -maxdepth 1 -type d | sort",
        ],
        state="The layer boundaries from the architecture doc exist in code and are stable for later tasks.",
    ),
    Task(
        id=5,
        slug="storage-foundation",
        title="Storage foundation (Room + DataStore)",
        goal=(
            "Provide the persistence seams: DataStore for preferences (port, bind mode, language, strategy) "
            "and Room for structured data (providers, keys metadata, quota ledgers, usage records, logs index)."
        ),
        deps=[4],
        est="45-90 min",
        skills=[
            ("persistence-room", "entities, DAOs, migrations strategy, transaction boundaries"),
            ("testing", "in-memory database tests for each DAO"),
        ],
        deliverables=[
            "`store/AppDatabase.kt` with entities: Provider, ProviderKey, QuotaLedger, UsageRecord, RoutingAlias",
            "`store/SettingsStore.kt` backed by DataStore for scalar preferences",
            "DAO tests using an in-memory database",
        ],
        steps=[
            "Define entities with explicit column names and indexes on the fields the router queries (provider id, key id, window start).",
            "Write DAOs with suspend functions and `@Transaction` where two tables must change together.",
            "Add a migration policy note: schema version 1 ships with no migration, and every later change needs one.",
            "Test insert/read/update for each DAO and the cascade delete of a provider's keys.",
        ],
        accept=[
            "`./gradlew :app:testDebugUnitTest` passes, including the new DAO tests",
            "Deleting a provider deletes its keys and quota ledgers (asserted in a test)",
            "No preference is stored in Room that belongs in DataStore, and vice versa",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest",
            "grep -rn 'Entity(' app/src/main/kotlin/com/droidroute/store/ | wc -l",
        ],
        state="Persistence seams exist and are tested; later tasks store data instead of inventing their own storage.",
    ),
    Task(
        id=6,
        slug="key-vault",
        title="Key vault (Keystore, AES-256-GCM)",
        goal=(
            "Implement the secret store described in docs/05-security.md: AES-256-GCM with a "
            "Keystore-wrapped key, per-record IV, one-time reveal, and the fixed mask format."
        ),
        deps=[5],
        est="60-120 min",
        skills=[
            ("security-audit", "review the crypto usage: key wrapping, IV uniqueness, no plaintext fallback path"),
            ("testing", "round-trip, tamper detection, mask format and canary tests"),
        ],
        deliverables=[
            "`vault/KeyVault.kt` — put/get/delete/revealOnce, ciphertext persisted in app-private storage",
            "`vault/Masking.kt` — `first5••••last5` with the documented short-key rule",
            "Unit tests including a corrupted-ciphertext case and a canary that must never appear in output",
        ],
        steps=[
            "Generate or unwrap the AES key via Android Keystore with GCM and no user-authentication requirement.",
            "Store ciphertext + IV + version per record; never a plaintext copy, never a deterministic IV.",
            "Implement masking exactly as documented (5 visible at each end, `••••` for anything over 12 characters).",
            "Implement `revealOnce` state tracking so the plaintext is surfaced once at entry time.",
            "Write the canary test: a known key value must not appear in any log record the vault produces.",
        ],
        accept=[
            "Round-trip test passes; a modified ciphertext byte causes a decryption failure rather than silent garbage",
            "Masking never exposes more than 5 characters from either end",
            "Canary test passes (key value absent from all log output)",
            "No plaintext secret is written anywhere outside the in-memory result of `revealOnce`",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*KeyVault*'",
            "./gradlew :app:testDebugUnitTest --tests '*Masking*'",
        ],
        state="Secrets can be stored and retrieved safely; every later storage of a credential goes through this API.",
    ),
    Task(
        id=7,
        slug="foreground-service-skeleton",
        title="Foreground service skeleton",
        goal=(
            "Create the service that will host the server: startForeground with the dataSync type, a "
            "persistent notification, START_STICKY, and a clean stop path — with no server logic yet."
        ),
        deps=[3],
        est="40-80 min",
        skills=[
            ("android-platform", "service type declaration, notification channel, START_STICKY semantics"),
            ("testing", "instrumented check that the service starts, notifies and stops"),
        ],
        deliverables=[
            "`server/DroidRouteService.kt` with start/stop/state callbacks",
            "Notification channel + ongoing notification showing port, bind mode and request count placeholders",
            "`POST_NOTIFICATIONS` runtime permission request on first start",
        ],
        steps=[
            "Declare the service in the manifest with `foregroundServiceType=\"dataSync\"`.",
            "Create the notification channel and an ongoing, low-importance notification.",
            "Implement START_STICKY with an explicit stop action in the notification.",
            "Expose a `StateFlow<ServiceState>` for the UI to observe.",
        ],
        accept=[
            "Starting the service from a debug action keeps it alive with the screen off for at least 10 minutes",
            "Stopping it removes the notification and releases resources",
            "No `IllegalStateException` about foreground service types on Android 14+",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "adb shell dumpsys activity services com.droidroute.app | head -40",
        ],
        state="A correctly typed foreground service exists; the server can be mounted into it by the next phase.",
    ),
    Task(
        id=8,
        slug="app-logging-writer",
        title="App-side log writer",
        goal=(
            "Implement the Kotlin logger that emits the same JSON-lines records as scripts/log-step.sh, "
            "through the same redactor, so runtime logs and agent logs are indistinguishable in shape."
        ),
        deps=[4],
        est="40-80 min",
        skills=[
            ("kotlin-core", "coroutine-safe appender, non-blocking writes, rotation hooks"),
            ("testing", "format conformance against a golden record produced by the shell script"),
        ],
        deliverables=[
            "`logging/LogWriter.kt` and `logging/LogRecord.kt`",
            "`logging/Redactor.kt` shared by app and bridge",
            "A test comparing an app-written record's shape with a shell-written one",
        ],
        steps=[
            "Model the record exactly as documented in handbooks/05-logging-standard.md.",
            "Write appends with a single writer coroutine to keep ordering without blocking callers.",
            "Apply the redactor to every field before serialisation, not after.",
            "Mirror records into `logs/tasks/` when the Termux integration is enabled and the path is writable.",
        ],
        accept=[
            "App record and shell record have identical keys and value shapes (asserted by a test)",
            "The redactor strips a planted key from a message field",
            "Writes do not block the caller (verified by a timing assertion in a test)",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LogWriter*'",
            "./gradlew :app:testDebugUnitTest --tests '*Redactor*'",
        ],
        state="App and agent logs share one format and one redactor; log evidence is now comparable across the two worlds.",
    ),
    Task(
        id=9,
        slug="ci-pipeline-hardening",
        title="CI pipeline hardening",
        goal=(
            "Make the workflows dependable: Gradle caching, artifact retention, scaffold gating that "
            "disappears automatically once the project exists, and documented signing secrets."
        ),
        deps=[3],
        est="30-60 min",
        skills=[
            ("ci-cd-github-actions", "workflow logic, caching, artifact and release steps"),
            ("security-audit", "confirm no secret is echoed and signing inputs come only from secrets"),
        ],
        deliverables=[
            "Updated `.github/workflows/build-apk.yml` with caching and honest gating",
            "`docs/signing.md` — which repository secrets must exist before the first `v*` tag",
        ],
        steps=[
            "Enable Gradle caching and pin action versions.",
            "Verify the release job fails loudly when signing secrets are absent (it must not produce an unsigned release).",
            "Confirm the workflow never prints an environment variable that could contain a secret.",
            "Record the required secret names in docs/signing.md, including how to generate the keystore base64.",
        ],
        accept=[
            "A push produces a green `verify` job and an `apk-debug` artifact",
            "Removing a signing secret makes the release job fail with an explicit message",
            "`docs/signing.md` names every required secret",
        ],
        verify=[
            "gh run list --workflow=build-apk.yml --limit 3",
            "gh secret list",
        ],
        state="CI is trustworthy: it fails when it should and never publishes an unsigned release.",
    ),
    Task(
        id=10,
        slug="docs-baseline-and-linkcheck",
        title="Documentation baseline and link integrity",
        goal=(
            "Guarantee that the documentation set is self-consistent: every relative link resolves, "
            "every doc referenced from README/AGENTS.md exists, and the German glossary covers every "
            "term a reader will meet in the docs."
        ),
        deps=[1],
        est="30-60 min",
        skills=[
            ("technical-writing", "check accuracy and remove any remaining filler"),
            ("testing", "extend the link checker to cover the glossary coverage rule"),
        ],
        deliverables=[
            "Link checker extended to report broken relative links with file and target",
            "`docs/glossary-de.md` updated with any term introduced since the scaffold",
        ],
        steps=[
            "Run the link checker locally over the whole tree and fix every report.",
            "Cross-read docs/ against status/components/ for stale statements about task ranges.",
            "Add missing glossary entries for any new term (do not invent terms the docs do not use).",
        ],
        accept=[
            "Link checker reports zero broken relative links",
            "Every doc listed in AGENTS.md §10 exists",
            "No doc claims a task range that disagrees with plan/INDEX.md",
        ],
        verify=[
            "python3 tools/generate_plan.py --check",
            "python3 tools/check_links.py",
        ],
        state="Documentation is internally consistent and machine-checked; drift now fails CI instead of confusing the next agent.",
    ),
]
