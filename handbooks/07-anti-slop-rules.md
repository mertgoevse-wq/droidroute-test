# Anti-Slop Rules

Binding for every agent, every task, every commit. Each rule names the violation and the correct behaviour.

## 1. No placeholder implementations

**Violation:** `// TODO: implement later`, `throw NotImplementedError()`, a function returning hard-coded fake data so a test passes.
**Correct:** implement it, or — if the task explicitly says to create a seam — create a documented adapter with a single `not_supported` error path and register it in `status/DECISIONS.md`.

## 2. No invented endpoints, URLs, model names or fields

**Violation:** writing `https://api.someprovider.com/v1` because it looks plausible; guessing a request field name.
**Correct:** the task says to read the provider's documentation; if it is unreachable, stop the task and record it. A wrong URL produces a provider that silently never works — worse than a missing one.

## 3. No unrequested scope

**Violation:** reformatting a file you did not have to touch, renaming someone else's identifiers, "while I was here" refactors, mass dependency upgrades.
**Correct:** change exactly what the task names. If you find a genuine defect outside scope, write it into `status/ERRORS.md` and leave the code alone.

## 4. No unverified completion

**Violation:** ticking acceptance boxes because the code compiles; writing "tests pass" without running them.
**Correct:** run the verification command, paste the raw result into the task log, then tick.

## 5. No silent failures

**Violation:** `catch (e: Exception) { /* ignore */ }`, `|| true` on a check.
**Correct:** handle it or log it with a reason. Every swallowed exception appears in the log with `level: warn` and a `result` explaining why it is safe to continue.

## 6. No duplicated truth

**Violation:** the same rule stated in `README.md`, `CLAUDE.md`, `AGENTS.md` and three handbooks, drifting apart.
**Correct:** state it once, link to it. The canonical homes are: architecture → `docs/01`, protocols → `docs/02`, routing → `docs/04`, security → `docs/05`, process → `docs/08` + `handbooks/`.

## 7. No filler prose

**Violation:** "In today's fast-paced world of AI…", restating the task title as a sentence, adjectives like *seamless*, *robust*, *powerful*, *cutting-edge*.
**Correct:** facts, decisions, rules, numbers. If a sentence does not change what the reader does, delete it.

## 8. No unverifiable claims

**Violation:** "This is 10× faster", "widely compatible", "production-ready".
**Correct:** a measured number with the measurement described, or nothing.

## 9. No test or check weakening

**Violation:** deleting a failing test, adding `@Ignore`, lowering a threshold, disabling lint or the secrets preflight to make a commit pass.
**Correct:** fix the cause. If the check itself is wrong, change it in its own task with the reasoning recorded in `status/DECISIONS.md`.

## 10. No template residue

**Violation:** files that still contain `<YOUR NAME>`, example text clearly not adapted, tables with rows nobody filled in.
**Correct:** every emitted file is fully resolved. A generator (if used) must produce complete files, not stubs.

## 11. No borrowed aesthetics (visual)

**Violation:** glassmorphism, Liquid Glass, frosted or blurred shells, neumorphism, brutalism, skeuomorphic controls, generic AI gradients (violet→blue and friends), glow or coloured drop shadows, a 3D-style button, emoji standing in for an icon, an underlined "interchangeable buzzword" headline.
**Correct:** the direction in [`docs/14-design-system.md`](../docs/14-design-system.md) §4 — flat graphite surfaces, hairline borders, one copper accent, real status lamps. A technique is not banned in isolation: it is banned when its only job is to look designed.

**The test that decides it:** replace our type and layout with a stock template — does anything change? If nothing changes, nothing was decided. Full gates in `docs/14` §11.

## 12. No unmanaged visual values

**Violation:** `Color(0xFF7C3AED)` inline, `Modifier.padding(13.dp)`, `RoundedCornerShape(10.dp)`, a second `fontSize` nobody chose, a raw `TextStyle` in a screen.
**Correct:** every colour, spacing, radius, type role and border comes from `ui/theme/Tokens.kt` as defined in [`docs/14-design-system.md`](../docs/14-design-system.md) §5–§7. A value that genuinely does not exist yet is **added to the token file first**, with its reason, in the same commit. `tools/check_design_slop.py` enforces the mechanical part of this.

## 13. No missing states

**Violation:** a screen that shows live data and has no empty state, no loading skeleton and no error state; a disabled control with no reason; a failed value rendered as `0`.
**Correct:** default, hover, focused, pressed, disabled for every control; loading, empty, error, partial, offline for every data area; unknown rendered as *unknown*, estimates labelled as *estimates*. See `docs/14` §9–§10.

## 14. No unearned motion, no decoration without a job

**Violation:** an entrance animation on the fifth launch of the same screen, a moving element that encodes nothing, a spinner where a skeleton belongs, animating layout properties instead of transform/opacity, ignoring reduced-motion.
**Correct:** motion explains state, causality, continuity or spatial change and nothing else; under 300 ms; custom ease-out; honours reduced motion. Decoration is admitted only when removing it loses information — the removal test in `docs/14` §4.2 and §11 decides.

## Self-check before committing

1. Does the diff contain only what the task named?
2. Are there any `TODO`, placeholder strings, or fake returns?
3. Did every acceptance criterion actually run?
4. Does every log line that should exist exist, and is it redacted?
5. Would a strict reviewer call any of this filler?

For any diff that touches UI:

6. Does `python3 tools/check_design_slop.py` pass, and did the four craft tests from `docs/14` §11 actually get run?
7. Is every colour, spacing, radius and type role from the token file — or did a new value get added with a reason?
8. Are the empty, loading, error and disabled states present, or does the screen only work when everything succeeds?

If any answer is uncomfortable, fix it before `scripts/step-commit.sh` runs.
