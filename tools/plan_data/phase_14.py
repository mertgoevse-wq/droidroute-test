"""Phase 14 — Design audit and release polish (the v0.3 craft milestone).

Phase 07 builds the interface. This phase proves it is the instrument described in
docs/14-design-system.md and not a generated dashboard: token conformance, measured
contrast, complete states, the four craft tests, and a gate that is proven to bite
on the real source tree.
"""

from common import Phase, Task

PHASE = Phase(
    number=14,
    slug="design-audit",
    title="Design audit & release polish",
    summary="Token conformance, a proven gate, screen-by-screen craft review, measured contrast and accessibility, state completeness, design acceptance.",
    design="""This phase audits; it does not redesign. The direction is already decided in [docs/14-design-system.md](../../docs/14-design-system.md) and the interface already exists — your job is to find where the build drifted from the system, prove it, and correct it.

Rules for every task in this phase:

1. **A finding needs a name, a cause and an after-picture.** "Looks better now" is not a finding. `docs/14` has a name for every defect class: flat hierarchy, monotone layout, harsh border, dramatic surface jump, mixed depth strategy, decorative layer, missing state, colour-only signal, off-scale value.
2. **Fix by moving back to the system, not by inventing a second system.** A failure is repaired by correcting a token or a layout decision. A new token needs its reason written down.
3. **Do not flatten the direction.** Removing the copper accent, quieting the signal path or neutering the density is not a fix — it is a different, worse product. [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) §11.
4. **Measure instead of asserting.** Contrast ratios, hit areas, query times and counts get numbers with the method stated. An unverifiable improvement claim is a violation (handbook rule 8).
5. **Leave what works alone.** The removal test decides: name the element's job, remove it mentally, and keep it if information would be lost.
6. **Name what is still not good.** Each task ends with residual weaknesses, stated plainly, rather than a claim of a clean finish.

The gate `python3 tools/check_design_slop.py` must pass at the end of every task here, and `--self-test` must pass in each task that touches the gate itself.""",
)

TASKS = [
    Task(
        id=185,
        slug="token-conformance-audit",
        title="Token conformance audit across the whole UI",
        goal=(
            "Prove that every colour, spacing, radius and type role in the built interface traces to `ui/theme/Tokens.kt` "
            "as specified in docs/14-design-system.md, and fix the drift that always accumulates while screens get built."
        ),
        deps=[92, 106],
        est="120-240 min",
        skills=[
            ("design-craft", "judging a value against the system, and telling drift from a legitimate new token"),
            ("droidroute-verification", "an inventory that can be re-run and compared, not a reading of the code"),
        ],
        deliverables=[
            "A generated inventory of every visual value found in the UI, with its token or its exception marked",
            "A zero-drift result: every value either resolves to a token or is added to `Tokens.kt` with a written reason",
        ],
        steps=[
            "Extract every literal colour, dp value, radius and text style from the UI sources into one list.",
            "Map each to a token; classify the rest as drift (fix in the UI) or a genuine gap (add to `Tokens.kt` with a reason in the same commit).",
            "Check the inverse direction too: tokens that no screen uses are either dead weight or a screen that ignored the system.",
            "Record the count before and after in the task log — an audit that cannot state its own effect is not an audit.",
        ],
        accept=[
            "No hardcoded colour remains outside `ui/theme/Tokens.kt` (asserted by `tools/check_design_slop.py`)",
            "Every spacing and radius value is on the scale in docs/14 §7, or the exception is documented in `Tokens.kt`",
            "The inventory script is committed and re-runnable",
        ],
        verify=[
            "python3 tools/check_design_slop.py",
            "python3 tools/check_design_slop.py --self-test",
        ],
        state="The design system is real in the code, not only in the document.",
    ),
    Task(
        id=186,
        slug="prove-the-gate-bites",
        title="Prove the design gate bites on the real source tree",
        goal=(
            "Inject every rule violation once into the actual app sources, confirm the gate fails with the right message, "
            "then revert. A gate that has silently stopped matching anything is worse than no gate."
        ),
        deps=[185],
        est="90-180 min",
        skills=[
            ("droidroute-verification", "one negative test per rule, each proved and reverted"),
            ("design-craft", "the cases phase 07 revealed that the rule set still does not catch"),
        ],
        deliverables=[
            "A documented proof table: rule → injected violation → gate message → reverted",
            "Gate extensions for the real cases the exercise exposes, and the fixture in `--self-test` extended to match",
        ],
        steps=[
            "For each rule in `tools/check_design_slop.py`, make the smallest real violation in a UI file, run the gate, record the output verbatim, then revert.",
            "Do the same for the state rule on a screen that collects state.",
            "Fix any rule that failed to fire, and any rule that fired on legitimate code.",
            "Extend the bad/good fixture pair so the self-test keeps covering what this exercise added.",
        ],
        accept=[
            "Every rule has at least one recorded failure with its exact message",
            "Every injection was reverted, and `git status` is clean afterwards (shown in the log)",
            "No rule fires on the real tree once the injections are reverted",
        ],
        verify=[
            "python3 tools/check_design_slop.py --self-test",
            "python3 tools/check_design_slop.py",
            "git status --short",
        ],
        state="The gate is evidence, because it has been shown to fail when it should.",
    ),
    Task(
        id=187,
        slug="craft-review-and-fixes",
        title="Screen-by-screen craft review with the four tests",
        goal=(
            "Walk every screen in both modes with the Swap, Squint, Signature and Token tests from docs/14 §11, name the "
            "highest-impact problem on each, and fix it. Not a taste report — a list of corrections."
        ),
        deps=[185],
        est="180-300 min",
        skills=[
            ("design-craft", "the four tests, the removal test, and knowing what to leave alone"),
            ("droidroute-verification", "screenshots as evidence at the real sizes, in both modes"),
        ],
        deliverables=[
            "One screenshot per screen in dark and light mode, attached as evidence",
            "A findings table per screen: test, named defect, correction, and the state after the fix",
        ],
        steps=[
            "For each screen, name the focal element (docs/14 §8) before judging anything else.",
            "Run the four tests; write down the specific defect, not an impression.",
            "Apply the removal test to every decorative layer: state the job, remove it mentally, keep only what loses information when removed.",
            "Re-shoot after each fix; a finding without an after-picture is not closed.",
            "Stop at the highest-impact problem per screen per pass rather than redesigning; the direction is already decided.",
        ],
        accept=[
            "Every screen has both modes captured and a named focal element",
            "Every finding has a correction and a re-shot screenshot",
            "No screen fails the squint test (hierarchy readable, nothing shouting)",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "python3 tools/check_design_slop.py",
        ],
        state="The interface reads as one decided thing rather than seven screens built on different days.",
    ),
    Task(
        id=188,
        slug="contrast-and-accessibility-evidence",
        title="Measured contrast, motion and accessibility evidence",
        goal=(
            "Replace the assertion that contrast is fine with numbers: every foreground/background pair in both modes, plus "
            "TalkBack, 200 % font scale, reduced motion and touch targets, each with recorded evidence."
        ),
        deps=[106],
        est="150-300 min",
        skills=[
            ("design-a11y", "WCAG thresholds and how a failure is fixed without flattening the direction"),
            ("droidroute-verification", "measured ratios, screen-reader transcripts, font-scale captures"),
        ],
        deliverables=[
            "A contrast table: token pair → measured ratio → threshold → pass/fail, both modes",
            "Evidence for TalkBack descriptions, 200 % font scale, reduced motion and hit areas",
        ],
        steps=[
            "Compute the ratio for every pair actually used; record the measured value, not a rounded claim.",
            "Fix failures by adjusting the token, never by moving text off a surface or dropping a level of the hierarchy.",
            "Run the whole app with TalkBack: every control described, the signal path announced as words.",
            "Set the animation scale to 0 and confirm the Signalweg is static, readable and still truthful.",
            "Test at 200 % font scale; fix truncation, overlap and clipped controls.",
        ],
        accept=[
            "Every used pair meets its threshold, with the measured ratio recorded",
            "Reduced motion removes movement and keeps every piece of information",
            "No screen breaks at 200 % font scale, and every control is reachable with the screen reader",
        ],
        verify=[
            "./gradlew :app:lintDebug",
            "adb shell settings put global animator_duration_scale 0",
            "adb shell settings put global animator_duration_scale 1",
        ],
        state="Accessibility is a measurement in this repository, not an intention.",
    ),
    Task(
        id=189,
        slug="state-completeness-pass",
        title="State completeness pass (loading, empty, error, partial, offline)",
        goal=(
            "Give every data-bearing screen its missing states, because the default path is the only one that ever gets "
            "built, and a gateway with no traffic shows nothing at all."
        ),
        deps=[187],
        est="120-240 min",
        skills=[
            ("android-compose-ui", "state families in Compose without duplicating layout per branch"),
            ("droidroute-verification", "each state produced on the device, not simulated in a preview"),
        ],
        deliverables=[
            "Five states implemented per data-bearing screen, demonstrated with a capture each",
            "Empty states that name the next action, error states in the API's own vocabulary",
        ],
        steps=[
            "Enumerate the screens that load data; for each, list which of the five states exist today.",
            "Build the missing ones: skeletons in the shape of the real content, empty states that offer the action, errors that name the cause.",
            "Make failures keep the last known value visible with a marker instead of blanking the screen.",
            "Produce each state on the device (stop the server, revoke the key, cut the network) and capture it.",
        ],
        accept=[
            "Every data-bearing screen has all five states, each captured",
            "An empty Dashboard states the next action instead of showing zeros",
            "The offline state is reachable in airplane mode and still useful",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "adb shell cmd connectivity airplane-mode enable",
        ],
        state="The interface is finished for the cases that actually happen, not only the happy one.",
    ),
    Task(
        id=190,
        slug="design-acceptance",
        title="Design acceptance and the closing statement",
        goal=(
            "Close the design work with evidence a stranger can check: acceptance criterion A16 met, the sheet of before/after "
            "evidence complete, and an honest list of what is still not good."
        ),
        deps=[186, 188, 189],
        est="90-180 min",
        skills=[
            ("droidroute-verification", "A16 as a criterion with evidence, not a summary"),
            ("technical-writing", "stating residual weaknesses plainly instead of claiming a finish"),
        ],
        deliverables=[
            "A16 evidence in `docs/10-acceptance.md`'s format, with the screenshots and measurements referenced",
            "A short design section in the owner documentation: direction, tokens, and how to keep the system when adding a screen",
            "A residual-weakness list — what is honestly still rough, and why it was accepted",
        ],
        steps=[
            "Walk A16 criterion by criterion and link each to its evidence.",
            "Write the owner-facing page: what the app looks like, why, and the three rules to follow when adding a screen.",
            "List what is still not good, without softening it.",
            "Confirm the gate, the four tests and the screenshots are all committed before declaring the phase done.",
        ],
        accept=[
            "A16 is met with linked evidence, or the gap is named as an open item in `status/ERRORS.md`",
            "The owner documentation explains the system well enough to add a screen without reading the source",
            "The residual-weakness list exists and is specific",
        ],
        verify=[
            "python3 tools/check_design_slop.py",
            "python3 tools/generate_plan.py --check",
        ],
        state="The design work is closed with evidence and without a claim it cannot support.",
    ),
]
