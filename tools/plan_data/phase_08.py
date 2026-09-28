"""Phase 08 — Local models: llama.cpp through Termux, with honest memory accounting."""

from common import Phase, Task

PHASE = Phase(
    number=8,
    slug="local-models",
    title="Local models",
    summary="Termux bridge, runtime resolution, model catalog, memory guard, and special-purpose models.",
)

TASKS = [
    Task(
        id=107,
        slug="termux-bridge",
        title="Termux bridge (RUN_COMMAND intent with HTTP fallback)",
        goal="Give the app one way to run things inside Termux/Debian: the documented RUN_COMMAND intent, usable for llama.cpp and for reading MCP configuration.",
        deps=[103, 22],
        est="90-180 min",
        skills=[
            ("android-platform", "permission handling, intent construction, exit-code propagation through TermuxService"),
            ("security-audit", "an intent that runs shell commands deserves a strict command allow-list"),
        ],
        deliverables=[
            "`bridge/TermuxBridge.kt` with `run(command, args)`, availability probe and a typed result",
            "A command allow-list so the bridge cannot become a remote shell",
            "`scripts/termux-bridge-helper.sh` as the receiving side, installed by the owner",
        ],
        steps=[
            "Implement the intent call, including the background flag and the result callback.",
            "Allow-list the commands the app may run (llama-server, whisper, cat of specific config paths).",
            "Return a typed result: success with stdout, failure with stderr and exit code.",
            "Test on the device; when Termux is absent, fail with a clear message instead of an exception.",
        ],
        accept=[
            "A command runs and its output returns to the app",
            "A command outside the allow-list is refused with a specific message",
            "Without Termux installed, the caller receives `unavailable`, not a crash",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*TermuxBridge*'",
            "bash scripts/termux-bridge-helper.sh --selftest",
        ],
        state="The app can drive the Linux environment it lives next to, within a narrow allow-list.",
    ),
    Task(
        id=108,
        slug="llama-runtime-resolution",
        title="llama.cpp runtime resolution",
        goal="Resolve a working llama.cpp runtime in the documented order and record which path won.",
        deps=[107],
        est="90-180 min",
        skills=[
            ("local-inference", "the three resolution paths and their real failure modes"),
            ("technical-writing", "an honest statement of what each path costs in download and time"),
        ],
        deliverables=[
            "`local/RuntimeResolver.kt` — package, build-from-source, prebuilt, each with a probe",
            "A UI-facing explanation when none resolves, naming which step failed",
        ],
        steps=[
            "Probe `llama-server --version` for each candidate path in order and record the version.",
            "For the build path, generate a script in the Debian environment and capture its output.",
            "For the prebuilt path, download and verify before offering it.",
            "Persist the winning path and re-probe on demand, never on every request.",
        ],
        accept=[
            "A working runtime is found or the failure names the exact missing prerequisite",
            "The resolved version and path are visible in the UI and in `/health`",
            "No binary is bundled in the APK",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*RuntimeResolver*'",
        ],
        state="Local inference has a real runtime with a recorded provenance.",
    ),
    Task(
        id=109,
        slug="llama-process-lifecycle",
        title="llama-server process lifecycle",
        goal="Start, monitor and stop llama-server per model, with idle unload, and prove the port is released on stop.",
        deps=[108],
        est="90-180 min",
        skills=[
            ("local-inference", "process supervision, port allocation, log capture"),
            ("testing", "start/stop/restart tests, including a crashed-process recovery test"),
        ],
        deliverables=[
            "`local/LlamaProcess.kt` — load, unload, status, log tail; idle unload after N minutes",
            "Port allocation from a reserved local range, one per loaded model",
        ],
        steps=[
            "Start the process with the documented flags (context, threads, no mlock) and capture its output.",
            "Detect readiness by polling `/health` on the model port, not by sleeping.",
            "Unload cleanly; if the process died, report the reason and its stderr tail.",
            "Unload on idle and on memory-pressure callbacks.",
        ],
        accept=[
            "A loaded model answers a completion through its local port",
            "Stopping releases the port within a second",
            "A crashed process is detected and reported rather than silently leaving a dead provider",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LlamaProcess*'",
        ],
        state="Local models have a managed lifecycle with observable state.",
    ),
    Task(
        id=110,
        slug="model-catalog",
        title="Model catalog and curated list",
        goal="Show what models exist locally and offer a curated set that is known to work on 8 GB.",
        deps=[109, 5],
        est="60-120 min",
        skills=[
            ("local-inference", "sane model choices for an 8 GB phone, with sizes and licences"),
            ("android-platform", "scanning owner-chosen folders through the storage access framework"),
        ],
        deliverables=[
            "`local/ModelCatalog.kt` — scan `.gguf` files plus a bundled curated list with sizes and licences",
            "Compatibility badge per entry: comfortable, tight, risky",
        ],
        steps=[
            "Scan the owner's chosen folder and `~/.droidroute/models/` for `.gguf` files, reading metadata where possible.",
            "Compose the curated list from models with published sizes and licences; no unattributed entries.",
            "Compute the badge from the device's real available memory at scan time.",
            "Persist the catalog with content hashes to detect file changes.",
        ],
        accept=[
            "Local files appear with their real sizes and quants",
            "Every curated entry names its source and licence",
            "Badges change when memory pressure changes",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ModelCatalog*'",
        ],
        state="The owner can pick a model that fits the device without guessing.",
    ),
    Task(
        id=111,
        slug="model-download",
        title="Model download with resume and checksum",
        goal="Download a curated model reliably on a phone connection: resumable, checksum-verified, with progress in the foreground service.",
        deps=[110, 7],
        est="80-150 min",
        skills=[
            ("kotlin-core", "resumable HTTP with range requests and a bounded retry policy"),
            ("security-audit", "verify the checksum before the file is offered as usable"),
        ],
        deliverables=[
            "`local/ModelDownloader.kt` with pause/resume/cancel and progress in the notification",
            "Checksum verification with a clear failure that deletes the partial file",
        ],
        steps=[
            "Implement range-based resume so an interrupted download continues instead of restarting.",
            "Verify size and checksum before marking the model usable.",
            "Report progress through the existing foreground notification.",
            "Handle storage-exhaustion by stopping cleanly and reporting remaining space.",
        ],
        accept=[
            "An interrupted download resumes and completes with a verified checksum",
            "A corrupted download is rejected and does not appear as usable",
            "Progress is visible in the notification while the app is backgrounded",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*ModelDownloader*'",
        ],
        state="Model acquisition survives a flaky phone connection.",
    ),
    Task(
        id=112,
        slug="memory-guard",
        title="Memory estimation, warnings and trim handling",
        goal="Implement the no-limit-but-no-surprises policy: estimate RAM need, warn with numbers, and unload under memory pressure.",
        deps=[109, 110],
        est="60-120 min",
        skills=[
            ("local-inference", "KV cache estimation from context, layers and head dimension"),
            ("android-platform", "onTrimMemory handling and what to unload first"),
        ],
        deliverables=[
            "`local/MemoryGuard.kt` — estimate, colour-coded warning, unload ranking",
            "Warning screen with the concrete numbers and the recommended smaller context",
        ],
        steps=[
            "Estimate need = file size + KV cache + overhead, and compare with available memory.",
            "Warn at the documented thresholds with actual numbers and a 'load anyway' action.",
            "On memory pressure, unload idle models first, then the least recently used, and only then the active one.",
            "Never kill a model mid-request without logging why.",
        ],
        accept=[
            "A too-large model produces the documented warning with real numbers, and loading anyway is possible",
            "Under simulated memory pressure the idle model is unloaded first",
            "No unload happens without a log record naming the reason",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*MemoryGuard*'",
        ],
        state="The owner can run any model size and always knows the risk before starting.",
    ),
    Task(
        id=113,
        slug="local-provider-registration",
        title="Register local models as ordinary providers",
        goal="Make a loaded local model indistinguishable from a hosted provider to routing, logging, usage and MCP.",
        deps=[109, 27],
        est="60-120 min",
        skills=[
            ("llm-routing", "registration semantics: availability follows the process lifecycle"),
            ("testing", "routing test proving a local model is preferred under a suitable strategy"),
        ],
        deliverables=[
            "Provider id `local/llamacpp/<model>` registered on load and removed on unload",
            "Capability declarations so local models are excluded from requests they cannot serve",
        ],
        steps=[
            "Register the running model with its real context window and capabilities.",
            "Mark it available only while the process is healthy.",
            "Ensure usage records mark local calls with zero cost and a `local` tag.",
            "Test that a request can be routed to the local model and that it disappears from candidates on unload.",
        ],
        accept=[
            "A loaded model appears in `/v1/models` and answers through the normal routes",
            "Unloading removes it from the candidate list immediately",
            "Usage records are tagged `local` with cost 0",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LocalProvider*'",
            "curl -fsS http://127.0.0.1:8787/v1/models | grep local",
        ],
        state="Local inference is a first-class route rather than a separate subsystem.",
    ),
    Task(
        id=114,
        slug="local-embeddings",
        title="Local embedding models",
        goal="Expose local embedding models through `/v1/embeddings` using the same runtime.",
        deps=[113, 76],
        est="60-120 min",
        skills=[
            ("local-inference", "embedding mode flags and batching for the local runtime"),
            ("testing", "dimension and determinism assertions"),
        ],
        deliverables=[
            "Embedding mode registration with the `embeddings` capability tag",
            "A test asserting deterministic vectors for identical input",
        ],
        steps=[
            "Start the runtime in embedding mode for models that support it.",
            "Tag them so chat routing never selects them (reusing the Phase 5 rule).",
            "Verify batching behaviour and vector dimensions.",
        ],
        accept=[
            "Local embeddings return vectors of the expected dimension",
            "Identical input yields identical output (determinism asserted)",
            "Embedding models never appear as chat candidates",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LocalEmbeddings*'",
        ],
        state="Local embedding models are usable for search and indexing work.",
    ),
    Task(
        id=115,
        slug="local-speech",
        title="Speech models (STT and TTS)",
        goal="Add whisper.cpp transcription and a speech synthesis path, with a clear `not_supported` when only one side is available.",
        deps=[108, 75],
        est="90-180 min",
        skills=[
            ("local-inference", "whisper.cpp usage, model sizes and their accuracy trade-off"),
            ("testing", "transcription test with a bundled short sample, plus the unsupported path"),
        ],
        deliverables=[
            "`local/SpeechRuntime.kt` for whisper.cpp resolution and invocation",
            "`/v1/audio/transcriptions` served locally; TTS either implemented or explicitly not_supported",
        ],
        steps=[
            "Resolve whisper.cpp following the same three-path strategy as llama.cpp.",
            "Invoke it for uploaded audio and return the documented response shape.",
            "For TTS, assess what is realistic on-device and either implement it or record the decision.",
            "Ensure a sample audio file exists for tests and contains no personal data.",
        ],
        accept=[
            "A short audio sample transcribes correctly",
            "Missing TTS support returns `not_supported` naming the missing runtime",
            "No test asset contains personal audio",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Speech*'",
        ],
        state="Speech in and out works locally, or its absence is stated precisely.",
    ),
    Task(
        id=116,
        slug="local-vision",
        title="Local vision models",
        goal="Support small multimodal models so image requests can be answered offline, with adjusted memory warnings.",
        deps=[113, 112],
        est="80-150 min",
        skills=[
            ("local-inference", "multimodal gguf handling and its extra memory cost"),
            ("testing", "image part round trip through the normalised model"),
        ],
        deliverables=[
            "Vision capability declaration for local multimodal models",
            "Memory estimate adjusted for the vision encoder",
        ],
        steps=[
            "Detect multimodal capability from the model metadata or the owner's declaration.",
            "Route image content parts to the local model when it is the chosen candidate.",
            "Adjust the memory estimate and warnings accordingly.",
        ],
        accept=[
            "An image request can be answered by a local multimodal model",
            "Non-vision local models reject image content with a capability error",
            "Memory warnings reflect the higher need",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LocalVision*'",
        ],
        state="Offline image questions are possible, with honest resource expectations.",
    ),
    Task(
        id=117,
        slug="embedded-runtime-spike",
        title="Embedded (JNI) runtime spike and decision",
        goal="Answer whether an embedded llama.cpp is worth building, with evidence, and record the decision rather than the intention.",
        deps=[113],
        est="120-240 min",
        skills=[
            ("local-inference", "JNI integration shape, build complexity, ABI constraints"),
            ("performance-android", "measure the difference in start time and memory against the Termux path"),
        ],
        deliverables=[
            "A spike branch or a documented experiment (not merged code, if the answer is no)",
            "A decision entry in status/DECISIONS.md with go or no-go and the evidence",
        ],
        steps=[
            "Assess build complexity honestly: toolchain, binary size, licence obligations.",
            "Measure the two paths' start latency and memory if a prototype is feasible within the spike budget.",
            "Write the decision with numbers and constraints, including what would change the answer.",
        ],
        accept=[
            "A decision exists in status/DECISIONS.md with evidence or an explicit statement of what could not be measured",
            "No half-integrated JNI code is left on main",
            "The task states clearly whether a future agent should revisit it",
        ],
        verify=[
            "grep -n 'embedded' status/DECISIONS.md",
            "./gradlew :app:assembleDebug",
        ],
        state="The embedded runtime question is settled with evidence instead of being forgotten.",
    ),
]
