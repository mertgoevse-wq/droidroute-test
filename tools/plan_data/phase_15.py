"""Phase 15 — Security and privacy audit.

The app holds credentials for other services on a phone that travels. This phase
turns "it is probably safe" into a threat model, measured controls and tests — and
states plainly what is *not* protected.
"""

from common import Phase, Task

PHASE = Phase(
    number=15,
    slug="security-audit",
    title="Security & privacy audit",
    summary="Threat model and test mapping, static analysis and licences, vault crypto review, network exposure, component and data-at-rest review, signing and audit trail.",
)

TASKS = [
    Task(
        id=191,
        slug="threat-model",
        title="Threat model and test mapping",
        goal=(
            "Write the threat model against what was actually built — assets, entry points, trust boundaries, attacker "
            "capabilities — and map every threat to an existing test, a missing test, or an explicitly accepted risk."
        ),
        deps=[14, 21, 165],
        est="150-300 min",
        skills=[
            ("security-audit", "assets, boundaries, attacker capability and the honest classification of residual risk"),
            ("technical-writing", "a model a reader can act on, not a taxonomy exercise"),
        ],
        deliverables=[
            "`docs/16-threat-model.md`: assets, entry points, trust boundaries, attacker profiles, threat table",
            "A mapping table: threat → control → test (or → accepted risk with the reason and the owner's decision)",
        ],
        steps=[
            "Enumerate assets: provider keys, subscription tokens, client keys, request content, logs, local model files, the vault itself.",
            "Enumerate entry points: the four protocol surfaces, the admin API, the share sheet, deep links, the MCP bridge, notifications.",
            "Enumerate boundaries: app ↔ internet, app ↔ other apps, agent ↔ gateway, device ↔ LAN/tunnel.",
            "For each threat, name the control that exists and the test that proves it. Where a test does not exist, record it as a task — do not imply coverage.",
            "State accepted risks explicitly with the reason (for example: a rooted device, memory while running, a malicious accessibility service).",
        ],
        accept=[
            "Every asset has a control or an explicitly accepted risk",
            "Every entry point has an authentication and an input-validation decision",
            "Every threat row names a test, a new task id, or an accepted risk — no empty cells",
            "The model names what is *not* protected, in the same document",
        ],
        verify=[
            "python3 tools/check_plan_consistency.py",
            "grep -rn 'TBD\\|TODO\\|to be decided' docs/16-threat-model.md || echo 'no unresolved markers'",
        ],
        state="Security claims are checkable: every threat points at a test or at a decision the owner made.",
    ),
    Task(
        id=192,
        slug="static-analysis-and-dependencies",
        title="Static analysis, dependencies and licences",
        goal=(
            "Know the supply chain: enable the platform's security analysis, pin every dependency, and give every one a "
            "version, a licence, a reason and a maintenance signal."
        ),
        deps=[9, 136, 144],
        est="120-240 min",
        skills=[
            ("gradle-android", "lint configuration, dependency verification, publishing checksums"),
            ("security-audit", "distinguishing a real advisory from a version-CVE false positive"),
        ],
        deliverables=[
            "`docs/17-security-audit.md` — the static-analysis and dependency section",
            "A dependency table: coordinate, version, licence, purpose, last release date, maintenance signal",
            "Dependency verification (checksums) enabled, or a written reason why it cannot be",
        ],
        steps=[
            "Turn on the platform security lint checks and make new findings fail the build rather than warn.",
            "Replace every dynamic version range with an exact version, and verify the dependency checksum set.",
            "List each dependency's licence and purpose; flag anything unmaintained or licence-incompatible and decide it explicitly.",
            "Check whether any dependency is used for one small thing while the platform already provides it — remove it or justify it.",
        ],
        accept=[
            "No dynamic version specifier (`+`, `latest`, ranges) remains in the build files",
            "Every dependency has a licence and a stated purpose in the table",
            "Security lint checks are enabled and fail the build on a new finding (proven once, then reverted)",
            "The audit section names the tooling used and its limitations (an offline device cannot query an advisory database live)",
        ],
        verify=[
            "./gradlew :app:lintDebug",
            "grep -rn '+\\\"\\|latest.release\\|versionRange' gradle/ app/build.gradle.kts build.gradle.kts | grep -v '^\\s*//' || echo 'no dynamic versions'",
        ],
        state="The supply chain is pinned, licensed and documented, with the limits of the audit stated.",
    ),
    Task(
        id=193,
        slug="vault-crypto-review",
        title="Secret storage and vault crypto review",
        goal=(
            "Review the vault as an attacker would: key derivation and binding, IV uniqueness, tamper detection, revocation, "
            "memory and log hygiene — and write down what the design cannot defend against."
        ),
        deps=[6, 159, 165],
        est="150-300 min",
        skills=[
            ("security-audit", "crypto usage review: mode, nonce, AAD, key lifetime, failure behaviour"),
            ("droidroute-verification", "tests that prove nonce uniqueness, tamper detection and revocation"),
        ],
        deliverables=[
            "A crypto review section in `docs/17-security-audit.md` with each parameter justified",
            "Tests: nonce uniqueness over N encryptions, tamper → distinct failure, revoked key unrecoverable, wrong credential refused",
            "A written statement of the unprotected cases (rooted device, running memory, device-unlocked attacker)",
        ],
        steps=[
            "Verify the key comes from the platform keystore and never leaves it in plaintext; state the binding used.",
            "Prove a fresh nonce per encryption (a counter test over many operations), and that altering any ciphertext byte fails closed.",
            "Verify revocation actually destroys recoverability, not just the reference.",
            "Audit every path a secret could escape through: logs, export, clipboard beyond its timer, notifications, intents, crash reports, backups.",
        ],
        accept=[
            "A nonce uniqueness test runs over at least 10 000 encryptions without a collision",
            "Tampering with ciphertext fails with a distinct error, never with partial data",
            "A redaction canary in the log path and in the export path is caught",
            "The unprotected list exists and names the residual risk without softening it",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Vault*'",
            "scripts/preflight-secrets.sh",
        ],
        state="Secret storage is reviewed with evidence, and its limits are written down instead of implied.",
    ),
    Task(
        id=194,
        slug="network-exposure-audit",
        title="Network surface and exposure audit",
        goal=(
            "Prove the exposure model: every combination of bind mode and auth mode has a test, upstream calls verify TLS, and "
            "nothing leaks version or configuration in an error."
        ),
        deps=[14, 21, 165],
        est="120-240 min",
        skills=[
            ("security-audit", "the exposure matrix and what a reachable port actually exposes"),
            ("ktor-server", "server hardening: timeouts, body limits, error shapes, no banner"),
        ],
        deliverables=[
            "An exposure matrix (bind × auth × reachability) with a test per row",
            "Proof that TLS verification is on for every upstream provider and that cleartext to a non-local host is refused",
        ],
        steps=[
            "Test that a non-loopback bind without a key is refused, and that the refusal is the same whether or not the port answers.",
            "Verify certificate verification for all upstream calls and that no trust-all setting exists anywhere.",
            "Refuse plaintext `http://` to a non-loopback provider unless the owner explicitly opted in for a local address.",
            "Set bounded request sizes and timeouts; confirm an oversized body is rejected rather than buffered.",
            "Check that error bodies and headers leak no version, build id, provider key fragment or internal path.",
        ],
        accept=[
            "Every matrix row has a passing test",
            "A non-local bind without a key is refused (asserted)",
            "Cleartext to a public host is refused (asserted)",
            "No error body contains a version string, an internal path or a credential fragment",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*Exposure*'",
            "curl -fsS http://127.0.0.1:8787/health",
        ],
        state="Exposure is a table with tests behind it, not an assumption about the default.",
    ),
    Task(
        id=195,
        slug="component-intent-and-at-rest-review",
        title="Components, intents and data at rest",
        goal=(
            "Review the app's surface to other apps and to the filesystem: exported components, intent handling, pending "
            "intents, backup rules, screenshot protection and shared content treated as untrusted input."
        ),
        deps=[98, 99, 103, 104],
        est="150-300 min",
        skills=[
            ("android-intent-security", "exposure review, intent redirection, pending-intent mutability, provider scope"),
            ("security-audit", "data at rest and what a backup would carry off the device"),
        ],
        deliverables=[
            "A manifest review table: component, exported, permission, reason",
            "Backup rules that exclude the vault, proven by a test",
            "Validation for every inbound intent extra and for share-sheet content",
        ],
        steps=[
            "List every component and justify each `exported=true`; remove the rest of the exposure.",
            "Validate and type-check every extra read from an intent, and never act on a value that arrives as a generic string.",
            "Set pending intents to immutable unless mutability is required, and check for intent redirection paths.",
            "Exclude the vault from backup and device transfer, and prove it with a test rather than a comment.",
            "Route shared content through the prompt-injection guard (T-158) and the size limits from T-194.",
        ],
        accept=[
            "No component is exported without a stated reason",
            "Every inbound extra is validated, with a test for a hostile value",
            "The vault is excluded from backup and transfer (asserted)",
            "Secret-bearing screens are screenshot-protected, verified on the device",
        ],
        verify=[
            "./gradlew :app:lintDebug",
            "./gradlew :app:testDebugUnitTest --tests '*Intent*' --tests '*Backup*'",
        ],
        state="The app's surface to other apps is small, justified and validated against hostile input.",
    ),
    Task(
        id=196,
        slug="signing-supply-chain-audit-trail",
        title="Signing, CI permissions and the audit trail",
        goal=(
            "Make releases attributable and the build chain auditable: pinned actions, least-privilege workflow permissions, "
            "published checksums, and a signed record of which task, commit and verifier produced each change."
        ),
        deps=[144, 165, 180],
        est="120-240 min",
        skills=[
            ("ci-cd-github-actions", "workflow permissions, pinned actions, provenance and artifact handling"),
            ("security-audit", "the difference between a signature that proves origin and one that proves nothing"),
        ],
        deliverables=[
            "Workflows with least-privilege permissions and every third-party action pinned by commit SHA",
            "Published SHA-256 checksums per artifact, verified by the updater (T-180)",
            "An append-only audit record: task, commit, verifier, and the acceptance criteria each verified",
        ],
        steps=[
            "Reduce each workflow's permission block to the minimum that still works, and record what was removed.",
            "Pin every third-party action to a full commit SHA, with the version in a comment.",
            "Publish a checksum file with each release and make the in-app updater verify it (not only the APK signature).",
            "Confirm no secret reaches a pull-request build, and that forks cannot read release secrets.",
            "Generate the audit record from the task logs and commits, so it cannot drift from what actually happened.",
        ],
        accept=[
            "Every third-party action is pinned by SHA",
            "Workflow permissions are minimal and the reduction is documented",
            "A tampered artifact fails signature and checksum verification, proven once",
            "The audit record covers every completed task and names the verifier",
        ],
        verify=[
            "gh api repos/{owner}/{repo}/actions/permissions --jq .",
            "python3 tools/check_plan_consistency.py",
        ],
        state="A stranger can check who built what, from which commit, verified by which workstream.",
    ),
]
