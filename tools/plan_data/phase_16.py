"""Phase 16 — Visual evidence and launch.

The project claims to look like an instrument panel. This phase makes that claim
visible and checkable: deterministic screenshots, automatic analysis, a visual Q&A
loop, a README gallery that cannot go stale, and a launch video.
"""

from common import Phase, Task

PHASE = Phase(
    number=16,
    slug="visual-evidence",
    title="Visual evidence & launch",
    summary="Screenshot harness, automatic visual analysis, visual Q&A loop, README gallery, launch video via brag, launch assets.",
    design="""This phase produces images of the interface, so the design rules apply to the *evidence* as much as to the app: [docs/14-design-system.md](../../docs/14-design-system.md) §11–§12.

1. **A screenshot is evidence, not marketing.** It shows the real app in a real state. No mock-up passed off as a build, no cropped-away failure, no invented number in a pixel.
2. **Deterministic or worthless.** Same locale, same font scale, same device size, same seeded data — otherwise two people comparing images compare different things.
3. **Both modes, every state.** Dark and light, and the states that are hard to reach: empty, loading, error, offline, parked key.
4. **Name what is wrong in the image.** A screenshot review that finds nothing is either a perfect screen or a shallow review; the second is far more likely. Findings get a name, a cause and an after-picture.
5. **Images live in the repository.** Committed under `design/`, referenced from the README, and checked for staleness by CI — a linked image that no longer matches the app is a false claim.""",
)

TASKS = [
    Task(
        id=197,
        slug="screenshot-harness",
        title="Deterministic screenshot harness",
        goal=(
            "Take screenshots that are worth comparing: fixed device sizes, fixed locale and font scale, seeded data, both "
            "modes, and every state that is hard to reach by hand."
        ),
        deps=[106, 190],
        est="150-300 min",
        skills=[
            ("visual-qa", "what a screenshot must contain to be evidence, and which states matter"),
            ("android-platform", "device control: screen capture, density, locale and font scale without hand-editing the device"),
        ],
        deliverables=[
            "`scripts/shots.sh` — captures the matrix (screens × modes × sizes × states) into `design/screenshots/`",
            "A fixture mode that seeds deterministic data so numbers and timestamps do not change between runs",
            "A documented device matrix and the exact commands used",
        ],
        steps=[
            "Define the matrix: the five destinations plus onboarding and the explain sheet; dark and light; a phone width and a tablet width; the states each screen can be in.",
            "Seed fixed data (a fixed provider list, fixed token counts, a fixed timestamp) so two runs are comparable.",
            "Capture through the platform: `adb exec-out screencap` for real-device shots, and Compose screenshot tests where they are cheaper.",
            "Pin locale, font scale and animation scale for the run, and restore them afterwards — the device is the owner's, not the harness's.",
            "Name files predictably: `<screen>-<mode>-<state>-<width>.png`, and fail the script if a matrix entry produced no file.",
        ],
        accept=[
            "A single command reproduces the whole matrix, and a second run produces identical images for the same state",
            "Every hard-to-reach state (empty, loading, error, offline, parked) has a capture",
            "The device is left in its original configuration after the run (asserted by the script)",
            "A missing matrix entry fails the script instead of silently omitting an image",
        ],
        verify=[
            "bash scripts/shots.sh",
            "ls design/screenshots | wc -l",
        ],
        state="The interface can be looked at on demand, comparably, without touching the app by hand.",
    ),
    Task(
        id=198,
        slug="automatic-visual-analysis",
        title="Automatic visual analysis of every screenshot",
        goal=(
            "Analyse the captured images instead of eyeballing them: clipped or overlapping text, off-token colours, contrast "
            "at real text positions, blank or broken screens, and golden-image drift — plus an advisory craft pass."
        ),
        deps=[197],
        est="180-360 min",
        skills=[
            ("visual-qa", "which defects a machine can decide and which need judgement"),
            ("droidroute-verification", "deterministic checks with thresholds, and a report that states its own limits"),
        ],
        deliverables=[
            "`tools/analyse_shots.py` — deterministic checks over `design/screenshots/`, writing `design/analysis/<date>.md`",
            "Golden images with a documented tolerance, so unrelated rendering noise does not cry wolf",
            "An advisory craft pass per screen, scored against docs/14 §11, clearly separated from the deterministic gate",
        ],
        steps=[
            "Detect clipped or overlapping text from the accessibility tree and the layout bounds rather than from pixels.",
            "Sample the actual pixels at each text region and compute the contrast ratio against the measured background (docs/14 §12).",
            "Build a histogram of the image's colours and report any colour that is not in the token palette — the honest way to catch a hardcoded value at runtime.",
            "Detect a blank screen, a screen with no focus element, and an unreachable touch target below the minimum size.",
            "Diff against golden images with a stated tolerance; report the changed region, not just a percentage.",
            "Run the advisory craft pass and label it as advisory in the report — a machine's score is not a design review.",
        ],
        accept=[
            "Every deterministic check produces a pass/fail line with the measured value, not just a verdict",
            "A deliberately off-token colour and a deliberately unreadable text pair are both caught (proven once, then reverted)",
            "The report separates deterministic findings from advisory ones",
            "The tool's limitations are stated in its own output (what it cannot see: hierarchy, intent, which element should lead)",
        ],
        verify=[
            "python3 tools/analyse_shots.py",
            "python3 tools/check_design_slop.py --self-test",
        ],
        state="Visual defects are found by a machine with numbers attached, and judgement is asked for only where it is needed.",
    ),
    Task(
        id=199,
        slug="visual-qa-loop",
        title="Visual Q&A loop with findings and fixes",
        goal=(
            "Look at the evidence and answer for it: for each screen, name what is wrong, why, fix it, and re-shoot. A finding "
            "is only closed by an after-picture — this is the visual question-and-answer the owner asked for."
        ),
        deps=[197, 198],
        est="180-360 min",
        skills=[
            ("design-craft", "reading a screenshot for hierarchy, rhythm and the focal element — not for taste"),
            ("visual-qa", "turning an image into a named defect and a testable correction"),
        ],
        deliverables=[
            "`design/review/<date>.md` — per screen: focal element, findings (test, defect, cause), fix, after-picture",
            "The applied fixes, in the same commits as their findings",
            "A residual list of what was seen and deliberately not changed, with the reason",
        ],
        steps=[
            "For each screen, state the focal element first (docs/14 §8) and whether the image agrees with it.",
            "Run the four craft tests (swap, squint, signature, token) against the actual image and write the specific defect.",
            "Answer for every element that was added \"because it looked empty\" — name its job or remove it (docs/14 §4.2 removal test).",
            "Fix, re-shoot, and replace the finding with the after-picture. Never close a finding with prose.",
            "Keep a residual list: things seen, judged, and left alone with a reason — silence reads as \"not noticed\".",
        ],
        accept=[
            "Every screen has a named focal element and at least one reviewed finding",
            "Every closed finding has an after-picture in the same document",
            "At least one finding per pass is a *removal*, not an addition — or the reason none was possible is stated",
            "The residual list exists and is specific",
        ],
        verify=[
            "python3 tools/analyse_shots.py",
            "python3 tools/check_design_slop.py",
        ],
        state="The interface was looked at, answered for, and corrected — with images proving both the problem and the fix.",
    ),
    Task(
        id=200,
        slug="readme-gallery",
        title="README gallery that cannot go stale",
        goal=(
            "Put the real screenshots in the README, generated from the files on disk, with a check that fails when an image "
            "no longer matches what the app produces."
        ),
        deps=[197, 199],
        est="120-240 min",
        skills=[
            ("visual-qa", "choosing images that show the product honestly, including one that is not flattering"),
            ("ci-cd-github-actions", "generated sections and the staleness check that keeps them true"),
        ],
        deliverables=[
            "A gallery section in `README.md` with committed screenshots (dark and light), the signal path, and one honest state",
            "`scripts/gallery.sh` regenerating the section, and a CI check that the committed section matches the images",
        ],
        steps=[
            "Pick images by what they show, not by how impressive they look. Include one state that is not success.",
            "Generate the section from `design/screenshots/` so it cannot list an image that does not exist.",
            "Keep the images small enough to keep the repository pleasant (compress, fixed width, one format).",
            "Add the staleness check to CI: if the gallery and the files disagree, the build fails with the regeneration command.",
        ],
        accept=[
            "Every image referenced in the gallery exists in the repository",
            "The gallery shows both modes and at least one non-success state",
            "CI fails when the gallery is out of date (proven once, then reverted)",
            "Total image weight stays within the budget stated in the section",
        ],
        verify=[
            "bash scripts/gallery.sh --check",
            "python3 tools/check_links.py",
        ],
        state="Anyone opening the repository sees the real app — and the images cannot quietly become fiction.",
    ),
    Task(
        id=201,
        slug="launch-video-brag",
        title="Launch video with the brag plugin",
        goal=(
            "Produce the 15–25 second launch video with the installed `brag` plugin, from the real product and the real "
            "screenshots, with its poster frame in the README and the share copy in the release notes."
        ),
        deps=[200],
        est="150-300 min",
        skills=[
            ("launch-video", "the brag workflow: hook, reveal, highlights, punchline, and the creative laws it enforces"),
            ("visual-qa", "making the video show the product truthfully rather than invent a product"),
        ],
        deliverables=[
            "`brag-output/brag.mp4`, its poster `brag.jpg`, `share-copy.txt` and `brag-plan.md`",
            "The poster embedded in the README, and the video attached to a GitHub release",
        ],
        steps=[
            "Check the prerequisites and record their versions: Node 22+, FFmpeg on PATH, `npx hyperframes doctor`.",
            "Run brag with a tone that matches this product (a serious, instrument-panel tone — not a parody), and let it read the real project code.",
            "Verify the result against the creative laws: at least one scene shows the real interface, no generic SaaS claims, every readable line holds long enough to read.",
            "Bake the poster as frame 0, embed it in the README, and attach the video to the release.",
            "If the device cannot run the toolchain, run it in CI or on another machine, and say in the task log where it ran — do not describe a video that does not exist.",
        ],
        accept=[
            "The video exists, is 15–25 seconds, and shows the real interface at least once",
            "Its claims match the repository (no invented numbers, no feature that is not built)",
            "The poster is in the README and the video is attached to a release",
            "If it could not be produced here, the reason and the alternative location are recorded — and the README makes no video claim",
        ],
        verify=[
            "npx hyperframes doctor",
            "ls -la brag-output/brag.mp4 brag-output/brag.jpg brag-output/share-copy.txt",
        ],
        state="There is a shareable launch video made from the actual product, not from a description of it.",
    ),
    Task(
        id=202,
        slug="launch-assets-and-visual-acceptance",
        title="Launch assets and visual acceptance",
        goal=(
            "Finish the visual identity: the app icon at every density, the adaptive icon, the store-style graphics and the own "
            "icon set — then close the visual claim with acceptance criterion A18 and an honest residual list."
        ),
        deps=[201],
        est="180-360 min",
        skills=[
            ("visual-qa", "producing assets that match the app instead of a template"),
            ("design-craft", "the identity: one mark, one accent, and the discipline not to add a second idea"),
        ],
        deliverables=[
            "The launcher icon in every density plus an adaptive icon (foreground, background, monochrome)",
            "An own icon set for the app's own concepts, aligned to the token grid and legible at 20dp",
            "Store-style graphics and the design section of the owner documentation",
            "A18 evidence: gallery, analysis reports, review documents, video, residual list",
        ],
        steps=[
            "Draw the mark from the chosen direction; test it at 48dp, 24dp and in monochrome before committing to it.",
            "Export every density and the adaptive layers; verify the icon masks correctly on a round-mask launcher.",
            "Build the own icon set for the product's concepts (signal path, provider, key, quota, local model, MCP) and check each at its smallest size.",
            "Produce the store-style graphics from real screenshots, never from mock-ups.",
            "Write the owner-facing design page and the residual list, then close A18 with links to every piece of evidence.",
        ],
        accept=[
            "The launcher icon renders correctly in normal, round and monochrome masks on a real launcher",
            "Every own icon is legible at its smallest rendered size (checked on the device, not in the editor)",
            "Store graphics use real screenshots and real numbers",
            "A18 is met with linked evidence, or the gap is recorded as an open item in `status/ERRORS.md`",
        ],
        verify=[
            "./gradlew :app:assembleDebug",
            "python3 tools/analyse_shots.py",
        ],
        state="The product has its own visual identity and a documented, checkable evidence trail for it.",
    ),
]
