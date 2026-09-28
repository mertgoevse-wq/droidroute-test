"""Phase 10 — Logging & handover: make the promise that any other model can continue provable."""

from common import Phase, Task

PHASE = Phase(
    number=10,
    slug="logging-handover",
    title="Logging & handover",
    summary="Retention, status automation, evidence bundles and adversarial resume drills.",
)

TASKS = [
    Task(
        id=127,
        slug="log-retention-in-app",
        title="Log retention and rotation inside the app",
        goal="Apply the documented retention (14 daily, 60 task logs, chain log forever) to app-written logs as well as script-written ones.",
        deps=[8, 104],
        est="50-100 min",
        skills=[
            ("kotlin-core", "rotation under concurrent writers without losing records"),
            ("testing", "rotation boundary tests and an interrupted-rotation test"),
        ],
        deliverables=[
            "`logging/LogRotator.kt` implementing the same policy as scripts/weekly-cleanup.sh",
            "A test proving both implementations agree on the boundary cases",
        ],
        steps=[
            "Implement the same counts and the same archive destination as the shell script.",
            "Rotate atomically: move complete files, never truncate a file being written.",
            "Run rotation on a weekly schedule and on demand.",
            "Assert parity with the shell script on the same fixture directory.",
        ],
        accept=[
            "The app and the script produce the same file set for the same fixture input",
            "An interrupted rotation leaves no lost records (asserted)",
            "`chain.log` is never rotated by either implementation",
        ],
        verify=[
            "./gradlew :app:testDebugUnitTest --tests '*LogRotator*'",
            "scripts/weekly-cleanup.sh --dry-run",
        ],
        state="Retention is one policy with two implementations that agree.",
    ),
    Task(
        id=128,
        slug="status-automation",
        title="Status file automation",
        goal="Make `status/PROGRESS.md` and `status/NEXT.md` update themselves from the plan and the logs, so they cannot go stale through forgetfulness.",
        deps=[17, 9],
        est="90-180 min",
        skills=[
            ("kotlin-core", "deterministic generation with a stable diff (no timestamp churn)"),
            ("technical-writing", "status content that answers the three questions an arriving agent has"),
        ],
        deliverables=[
            "`tools/update_status.py` — reads plan/, logs/ and git to regenerate the two files",
            "A CI check that fails when the generated status disagrees with reality",
        ],
        steps=[
            "Derive completed tasks from the commit subjects (`T-0xx:`) and log records, not from a hand-kept list.",
            "Regenerate PROGRESS and NEXT with a stable ordering and no volatile fields.",
            "Add `--check` mode and wire it into repo-hygiene.",
            "Document the flow in docs/08-workflow.md, replacing any manual instruction that contradicts it.",
        ],
        accept=[
            "Running the tool twice produces no diff",
            "`--check` fails when a completed task is missing from the status files (proven once, then reverted)",
            "CI runs the check",
        ],
        verify=[
            "python3 tools/update_status.py && git diff --exit-code status/",
            "python3 tools/update_status.py --check",
        ],
        state="The status files are always true, because they are derived.",
    ),
    Task(
        id=129,
        slug="daily-summary-generation",
        title="Daily summary generation",
        goal="Produce the daily summary files from the logs so the owner can read a day in fifteen lines.",
        deps=[128],
        est="50-100 min",
        skills=[
            ("kotlin-core", "aggregation from log records into the documented template"),
            ("technical-writing", "summaries that state facts, not narration"),
        ],
        deliverables=[
            "`tools/gen_daily_summary.py` writing `status/daily/YYYY-MM-DD.md`",
            "Template kept in sync with status/daily/README.md",
        ],
        steps=[
            "Aggregate completed tasks, started tasks, commits, blockers and the next task from the log records.",
            "Refuse to invent content: a day with no records produces a file that says so.",
            "Keep the output under the documented length.",
        ],
        accept=[
            "A generated summary matches the template exactly",
            "An empty day produces an honest empty summary",
            "Running it twice produces identical output",
        ],
        verify=[
            "python3 tools/gen_daily_summary.py --date 2026-09-28 && cat status/daily/2026-09-28.md",
        ],
        state="The owner can read a day of autonomous work in one screen.",
    ),
    Task(
        id=130,
        slug="chain-log-integrity",
        title="Chain log integrity verification",
        goal="Guarantee the handover spine is complete: every completed task has a commit, a log file and a status entry.",
        deps=[128],
        est="60-120 min",
        skills=[
            ("testing", "cross-source consistency check across git, logs and status"),
            ("technical-writing", "a report that names exactly what is missing"),
        ],
        deliverables=[
            "`tools/verify_chain.py` comparing plan, git log, logs/tasks and status/PROGRESS.md",
            "CI integration and a documented manual run",
        ],
        steps=[
            "For each task marked complete: assert a commit with the right subject exists, a task log exists, and the status lists it.",
            "Report discrepancies with the task id and the missing artefact.",
            "Allow a documented exemption list for tasks completed before this check existed, and mark it as such.",
        ],
        accept=[
            "The tool exits 0 on a consistent repository",
            "Deleting one task log makes it fail with a precise message (proven once, then reverted)",
            "Any exemption is explicit and dated",
        ],
        verify=[
            "python3 tools/verify_chain.py",
        ],
        state="The evidence trail is verifiable, which is what makes the handover real.",
    ),
    Task(
        id=131,
        slug="handover-bundle",
        title="Handover evidence bundle",
        goal="Produce one file an arriving agent reads first: current state, next task, open errors, last decisions and where the evidence lives.",
        deps=[130, 129],
        est="60-120 min",
        skills=[
            ("kotlin-core", "deterministic bundle generation with redaction applied"),
            ("technical-writing", "content chosen for a reader with no context"),
        ],
        deliverables=[
            "`tools/handover_bundle.py` writing `status/HANDOVER.md`",
            "A check that the bundle is regenerated whenever a task completes",
        ],
        steps=[
            "Compose from PROGRESS, NEXT, ERRORS, the tail of chain.log and the recent decisions.",
            "Apply the redactor; the bundle is committed, so it must be safe.",
            "Keep it short enough to read in two minutes, with links for depth.",
            "Regenerate it in `scripts/step-commit.sh` so it is never stale.",
        ],
        accept=[
            "`status/HANDOVER.md` is regenerated and committed with every task commit",
            "The bundle contains no secret-shaped value (canary)",
            "A reader can state the next action after reading only the bundle",
        ],
        verify=[
            "python3 tools/handover_bundle.py && scripts/preflight-secrets.sh",
        ],
        state="Arriving at this project cold takes two minutes instead of twenty.",
    ),
    Task(
        id=132,
        slug="resume-drill-clean",
        title="Resume drill: clean handover",
        goal="Prove the handover works by continuing the plan in a fresh session using only the repository.",
        deps=[131],
        est="60-120 min",
        skills=[
            ("testing", "design the drill so it cannot cheat by using session memory"),
            ("technical-writing", "record the drill result as evidence, including friction found"),
        ],
        deliverables=[
            "A recorded drill: start a fresh session, read only `status/` and the target task, complete one real task",
            "A list of frictions found and the documentation fixes they produced",
        ],
        steps=[
            "Start a fresh session with no chat history, following handbooks/06-resume-protocol.md literally.",
            "Complete the next task in the plan end to end.",
            "Record every point where the documentation was insufficient, and fix the documentation.",
            "Store the drill transcript summary in `status/daily/`.",
        ],
        accept=[
            "The task was completed using only repository content",
            "Every friction found produced a documentation change in the same commit",
            "The drill is recorded with the task id it completed",
        ],
        verify=[
            "python3 tools/verify_chain.py",
        ],
        state="The resume protocol is proven, not assumed.",
    ),
    Task(
        id=133,
        slug="resume-drill-interrupted",
        title="Resume drill: interrupted mid-task",
        goal="Prove the harder case: a task killed halfway leaves enough evidence for a different agent to finish it without guesswork.",
        deps=[132],
        est="60-120 min",
        skills=[
            ("testing", "an adversarial drill: kill the session at an awkward step, uncommitted"),
            ("technical-writing", "verify the STOPPED note template is sufficient and improve it if not"),
        ],
        deliverables=[
            "A recorded drill with a deliberately interrupted task and a successful takeover",
            "Any improvement to handbooks/06-resume-protocol.md that the drill proved necessary",
        ],
        steps=[
            "Begin a task, complete two or three steps, then stop without committing.",
            "Append the STOPPED note exactly as the template prescribes.",
            "In a fresh session, follow only the status files and finish the task.",
            "Log whether the takeover was unambiguous; if not, fix the protocol.",
        ],
        accept=[
            "The takeover completed the task without inspecting session history",
            "The working tree state was recoverable exactly as the note described",
            "The protocol documentation changed if the drill exposed a gap",
        ],
        verify=[
            "cat status/ERRORS.md | tail -20",
            "python3 tools/verify_chain.py",
        ],
        state="The worst realistic interruption is survivable with the documented artefacts alone.",
    ),
    Task(
        id=134,
        slug="request-task-trace-correlation",
        title="Correlate runtime requests with build tasks",
        goal="Make it possible to join a runtime log line to the build task that produced the code path, for debugging after a handover.",
        deps=[17, 131],
        est="50-100 min",
        skills=[
            ("kotlin-core", "inject the build revision and task id into runtime records without churn"),
            ("testing", "assert the correlation fields exist and stay redacted"),
        ],
        deliverables=[
            "Build metadata (git sha, build time) available at runtime and included in log records",
            "A documented way to go from a runtime record to the task that introduced the code",
        ],
        steps=[
            "Generate the git sha into the build at compile time.",
            "Include it in every runtime log record and in `/health`.",
            "Document the lookup: sha → commit → task id.",
        ],
        accept=[
            "A runtime record contains the build sha",
            "`/health` reports the same sha as the installed build",
            "The lookup procedure is documented and was performed once as evidence",
        ],
        verify=[
            "curl -fsS http://127.0.0.1:8787/health | grep -i sha",
            "git log --oneline -1",
        ],
        state="Runtime behaviour can be traced back to the build that introduced it.",
    ),
    Task(
        id=135,
        slug="handover-docs-verification",
        title="Handover documentation verification",
        goal="Final check of the whole handover chain: an agent with no context can find, understand and act on every artefact.",
        deps=[132, 133, 134],
        est="50-100 min",
        skills=[
            ("technical-writing", "walk the documentation as a stranger would, not as its author"),
            ("testing", "convert each documented claim into a checkable assertion"),
        ],
        deliverables=[
            "A verified handover chain: README → AGENTS/CLAUDE → status → plan → handbooks",
            "Corrections committed for anything that failed the walkthrough",
        ],
        steps=[
            "Follow the documented entry path from README to a completed action.",
            "Check that every link resolves and every named file exists.",
            "Confirm the German glossary covers the terms a German-speaking owner will meet.",
        ],
        accept=[
            "The walkthrough completes without consulting any undocumented source",
            "All links resolve (checked by tooling)",
            "Corrections are committed, not merely noted",
        ],
        verify=[
            "python3 tools/check_links.py",
            "python3 tools/verify_chain.py",
        ],
        state="The handover chain is verified end to end rather than believed.",
    ),
]
