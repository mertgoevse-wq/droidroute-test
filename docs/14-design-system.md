<div align="center">

# DroidRoute — Design System

**One direction, decided once, applied everywhere.**

`Direction: Graphit-Instrumententafel · Akzent: Kupfer · Marke: „Signal“ · Signatur: der Signalweg`

Rules that bind agents: [`handbooks/07-anti-slop-rules.md`](../handbooks/07-anti-slop-rules.md) §11–§14 · Drawings: [`design/README.md`](../design/README.md)
Gate: `python3 tools/check_design_slop.py` · Tasks: [`plan/phase-07-ui/`](../plan/phase-07-ui/), [`plan/phase-14-design-audit/`](../plan/phase-14-design-audit/)

</div>

---

## 1. Why this document exists

Before this file, the repository said three things about visual design: *"a coherent Material 3 theme"*, *"simple, readable charts"* and *"dynamic colour"*. Nothing else. That is the exact input that produces the default result — Material You purple, four equal KPI cards, a rainbow chart, everything the same size. The rules below replace intention-by-omission with decisions that can be checked.

This document is the **system**: direction, tokens, scales and gates. The **rules** for agents live in [`handbooks/07-anti-slop-rules.md`](../handbooks/07-anti-slop-rules.md) §11–§14 so that all prohibitions stay in one place. The **implementation** lives in the phase 07 and phase 14 tasks.

## 2. Audit findings (state before this document)

| # | Finding | Why it is a defect | Fixed by |
|---|---|---|---|
| D1 | No palette anywhere; `dynamic colour` was requested as a feature | Material You paints the app in the owner's wallpaper. The product would have no identity at all — its colour would literally be someone else's photo. | §4, §5; `dynamicColour` becomes opt-in (default **off**) |
| D2 | No type scale, spacing scale, radius scale or depth strategy | Defaults produce *flat hierarchy* and *monotone layout*: everything one size, one gap, one density. The single most common reason generated UI reads as generated. | §5–§7 |
| D3 | Charts specified only as "simple, readable" | Default output is a multi-colour series with a legend and no baseline discipline. | §9 |
| D4 | No naming of the focal element on any screen | A dashboard with four equal cards has no entry point for the eye. | §8 |
| D5 | No banned-pattern list for visual work | [`handbooks/07`](../handbooks/07-anti-slop-rules.md) covered code slop (placeholders, invented URLs) but said nothing about glass, gradients or borrowed aesthetics. | handbook §11 |
| D6 | No signature element | The interface would be interchangeable with any gateway dashboard — which fails the project's own test for craft (`§11`: *if another product could ship this unchanged, it is a default*). | §8.2 |
| D7 | No loading / empty / error / offline state requirement per screen | Missing states are the fastest tell of unfinished UI; a router with no traffic shows nothing at all. | §10 |
| D8 | Accessibility covered screen readers, font scale and touch targets, but not measured contrast, reduced motion or state coverage | Contrast was asserted (*"verify contrast ratios"*) with no method and no numbers. | §12 |
| D9 | Nothing in CI looked at the UI | Without a gate, the first twenty commits drift and nobody notices. | §13, `tools/check_design_slop.py` |
| D10 | "Document the palette in a design note inside the theme package" | A second, private source of truth that no checker reads. Canonical design truth is *this* file. | §3 |

Audit method: the design-skill library index (`~/.claude/design-skill-library`) was queried for mobile, dashboard, dark-mode, colour-system and anti-slop skills; `interface-design`, `no-ai-design-slop`, `dark-mode-design`, `color-system` and `hallmark` were read in full, and their rule catalogues are what §4–§13 apply **to this product**. Nothing here is taken from OmniRoute, 9Router or any other router: those are competitors, not references.

## 3. One source of truth

| Question | Document |
|---|---|
| What does the interface look like and why | this file |
| What is forbidden, for every agent, always | [`handbooks/07-anti-slop-rules.md`](../handbooks/07-anti-slop-rules.md) §11–§14 |
| Which skill to load for design work | [`handbooks/09-skill-resolution.md`](../handbooks/09-skill-resolution.md) → `android-compose-ui` |
| Where it is built | [`plan/phase-07-ui/`](../plan/phase-07-ui/), [`plan/phase-14-design-audit/`](../plan/phase-14-design-audit/) |
| Which drawing implements it | [`design/`](../design/README.md) — logo, own icon set, dashboard mock, living preview |
| Is it still true | `python3 tools/check_design_slop.py` (CI) |

No theme package writes its own design note. Token names and values live here and in `ui/theme/Tokens.kt`; if the two disagree, the Kotlin is wrong.

## 4. Direction

### 4.1 The world this product lives in

DroidRoute is a **switchboard**. Requests arrive, are examined, and are switched to one of many lines. That world has real objects, and the interface borrows from them instead of from "SaaS dashboard".

| Axis | Decision | Consequence |
|---|---|---|
| **Domain vocabulary** | switchboard, patch panel, line, lane, signal, relay, patch cable, circuit, toll, meter, timetable, relief (Ablösung), slot | Labels use the product's real nouns; the router's own terms (`provider`, `key`, `quota`, `breaker`) stay in English |
| **Colour world** | dark bakelite panel, engraved labels, signal lamps (green / amber / red), copper terminals, manila timetable paper, cable jackets in muted slate and olive | graphite structure + one copper accent + real lamp colours |
| **Material** | flat panel, hairline engraved lines, no glass, no glow | depth strategy = **borders only** (§7) |
| **Feel** | a working instrument panel at night: calm, legible, precise — never a consumer app and never a brochure | dense by default, generous only around the focal element |
| **One visual thesis** | *the request path is visible* | the signature element is the routing itself, not a logo |

### 4.2 The signature element — the Signalweg

One element that could not exist in any other product:

> A vertical **live signal path** on the Dashboard: the client line, the DroidRoute switch, and the provider lines, with a lamp per endpoint whose colour is the real health state and a marker that moves along the path when a request is in flight. On failure the marker stops *at the hop that failed* and the hop carries the reason string from `/v1/routing/explain`.

It is the product's identity because it is the product's function. Rules:

- It encodes **state**, never decoration: no movement without a request, no lamps without a health verdict.
- Every visual claim matches the API. A lamp may not be green because green looks good.
- With reduced motion it becomes a static path with the last hop highlighted; it is fully usable with no animation.
- If a metric is unknown, the hop shows *unknown*, not a neutral colour that hides the gap.

### 4.3 Rejected defaults

Named so they cannot sneak back in:

| Default | Replaced by |
|---|---|
| Dark SaaS dashboard: four equal KPI cards in a row | one live signal path as the focal element, with the single most important number beside it at display size and the rest demoted to a labelled list |
| Gradient or glass hero, coloured card fills | flat surfaces, hairline borders, one copper accent used only for the primary action |
| Equal bottom navigation, every screen the same shape | five destinations kept, but each screen states its own focal element and its own density (§8) |
| Rainbow multi-series chart | one accent + one comparison hue, direct labels, zero-baseline bars, unknown rendered as unknown (§9) |
| Bundled "tech" webfont for personality | platform type at a real scale, plus platform **monospace with tabular figures** for numbers — a decision with a reason (§6) |

## 5. Colour

**Dark mode is the primary mode.** The owner runs a gateway at night; light mode is the timetable-paper variant, not the other way round. Tokens are declared once in **OKLCH** (perceptual lightness, so a lightness step looks like a lightness step at every hue), then converted for Compose.

### 5.1 Surfaces — one hue, lightness only

| Token | OKLCH | Role |
|---|---|---|
| `canvas` | `oklch(0.180 0.012 250)` | page background |
| `surface-1` | `oklch(0.215 0.012 250)` | cards, list rows on canvas |
| `surface-2` | `oklch(0.245 0.012 250)` | sheets, popovers, dialogs |
| `surface-3` | `oklch(0.270 0.012 250)` | tooltips, menus above a sheet |
| `inset` | `oklch(0.150 0.012 250)` | text fields, code, log view — **darker** than its surroundings, because inputs receive content |

Steps are ~3.5 points of lightness: visible when stacked, invisible in isolation. Never a second hue for a surface — a violet sidebar on a graphite page fragments the panel into two products.

### 5.2 Borders — the only depth mechanism

| Token | Value | Role |
|---|---|---|
| `line-faint` | `rgba(255,255,255,0.07)` | separation inside a card |
| `line` | `rgba(255,255,255,0.10)` | card and row edges |
| `line-strong` | `rgba(255,255,255,0.16)` | section boundary, inset field outline |
| `line-focus` | `rgba(255,255,255,0.28)` | focus ring |

### 5.3 Text — four levels, always three levers

| Token | OKLCH | Hex (dark) | Level |
|---|---|---|---|
| `ink` | `oklch(0.930 0.005 250)` | `#E5E8EB` | primary — never pure white |
| `ink-2` | `oklch(0.780 0.008 250)` | `#B4B8BC` | secondary / supporting |
| `ink-3` | `oklch(0.660 0.010 250)` | `#8E9398` | tertiary / labels |
| `ink-muted` | `oklch(0.645 0.010 250)` | `#898E94` | metadata — the lowest level usable for real text |
| `ink-disabled` | `oklch(0.510 0.010 250)` | `#62676C` | disabled only; exempt from the contrast floor, and never used for information |

Hierarchy comes from **size + weight + colour together**. A single 14sp size holds three tiers: `value 600/ink`, `label 500/ink-3`, `meta 400/ink-muted`.

### 5.4 Accent — copper, exactly one, and never a status colour

The owner chose **copper** over brass: warmer, slightly darker, more earth than instrument-panel shine.

| Token | OKLCH | Role |
|---|---|---|
| `accent` | `oklch(0.720 0.120 055)` | copper. The one primary action per screen, the active destination, a 1dp emphasis stroke |
| `accent-ink` | `oklch(0.200 0.020 055)` | text/icons **on** a copper fill |
| `accent-quiet` | `oklch(0.290 0.040 055)` | copper-tinted container when a filled control would be too loud |

Rules: one accent per screen; ~10 % of pixels at most; never on a status chip, a lamp or a chart series.

**Copper sits near two status hues, and that is handled by material, not by hope.** Copper (`055`), warn (`075`) and err (`025`) are 20–30° apart — close enough that colour alone must never be the difference:

| | Copper is allowed to be | Copper is never |
|---|---|---|
| Form | a filled control with dark text, an underline, a 1dp stroke, the active destination | a lamp, a dot, a filled pill that carries state |
| Pairing | always with a verb ("Verbinden", "Weiter") | always without a word |
| Place | one per screen, near the primary action | inside a status list, a chart, or next to a lamp |

Status colours keep the shape-and-word rule from §5.5, so the three are distinguishable to a colour-blind reader as well. T-188 measures every copper/status pair side by side in both modes before this is considered settled, and the values above are the starting point for that measurement, not the conclusion.

### 5.5 Status — real lamps, never colour alone

| Token | OKLCH | Meaning |
|---|---|---|
| `ok` | `oklch(0.750 0.110 155)` | healthy, quota available |
| `warn` | `oklch(0.810 0.125 075)` | degraded, near a limit, breaker half-open |
| `err` | `oklch(0.680 0.150 025)` | failing, quota exhausted, breaker open |
| `info` | `oklch(0.760 0.070 240)` | neutral system fact |
| `unknown` | `ink-3` + hatch pattern | value not known — **never** rendered as a neutral ok |

Every status is carried by **colour + shape + label** together: a filled circle, a half-filled circle, a bar, a triangle — plus the word. `warn` sitting near the copper accent is safe because the accent never marks state and never appears as a lamp (§5.4), and every lamp carries a shape and a word.

Constraints: body text ≥ 4.5:1, large text and UI components ≥ 3:1, no meaning conveyed by hue alone, all pairs verified during T-188 with recorded ratios.

### 5.6 Light mode ("Timetable")

| Token | OKLCH | Hex |
|---|---|---|
| `canvas` | `oklch(0.975 0.004 250)` | `#F5F7F9` |
| `surface-1` | `oklch(1.000 0.000 000)` | `#FFFFFF` |
| `inset` | `oklch(0.960 0.004 250)` | `#F0F2F4` |
| `ink` | `oklch(0.220 0.012 250)` | `#161B20` |
| `ink-2` | `oklch(0.380 0.012 250)` | `#3E4349` |
| `ink-3` | `oklch(0.480 0.010 250)` | `#595E63` |
| `ink-muted` | `oklch(0.520 0.010 250)` | `#65696F` |
| `accent` | `oklch(0.545 0.140 055)` | `#AC5500` |
| `accent-ink` | `oklch(0.995 0.008 055)` | `#FFFCF8` |
| `ok` / `warn` / `err` / `info` | `0.545 0.135 155` / `0.600 0.150 075` / `0.560 0.190 025` / `0.520 0.120 240` | `#00864B` / `#B37000` / `#CC3336` / `#0070A6` |

Same hierarchy, inverted values, same single hue.

### 5.7 Measured contrast (this is the evidence, not a promise)

Every pair below was converted OKLCH → sRGB and measured with the WCAG relative-luminance formula on 2026-09-28, because the first version of this section *asserted* contrast and the assertion was wrong: the light-mode accent-ink pair measured 3.97:1 and light `warn` measured 2.98:1. Both were fixed by moving the token, not by moving the text — which is the rule in §12.

| Foreground | Backgrounds | Measured (dark) | Measured (light) | Floor |
|---|---|---|---|---|
| `ink` | canvas / surface-1 / surface-2 / surface-3 / inset | 12.24 – 15.95 | 16.14 | 4.5 |
| `ink-2` | same | 7.55 – 9.83 | 9.29 | 4.5 |
| `ink-3` | same | 4.86 – 6.33 | 6.10 | 4.5 |
| `ink-muted` | same | 4.56 – 5.94 | 5.14 | 4.5 |
| `accent` | canvas / surface-1 / surface-2 | 6.31 – 7.31 | 4.82 – 5.18 | 3.0 |
| `accent-ink` | accent | 7.06 | 5.07 | 4.5 |
| `ok` / `warn` / `err` / `info` | canvas / surface-2 | 5.25 – 10.27 | 3.74 – 5.43 | 3.0 |

Zero failures. Two consequences that are now rules:

- `ink-muted` was raised to `0.645` in dark mode so that metadata text passes **on every surface**, not only on the canvas. A level that only works on one background is a trap.
- `ink-disabled` was split out of it. Disabled controls are exempt from the contrast floor; information is not. Conflating the two is how a hint becomes unreadable.

T-188 re-measures on the rendered app, at the real text positions, in both modes and at 200 % font scale. This table is the starting point it checks against.

### 5.8 Dynamic colour

**Off by default.** `dynamicColour` becomes an opt-in setting for the owner, documented as "use my wallpaper colours". The designed scheme is always the shipped default, because an app whose identity is the wallpaper has no identity to verify.

## 6. Typography

Base 14sp, ratio **1.25** (product UI), rounded to the spacing grid:

| Role | Size | Weight | Colour | Notes |
|---|---|---|---|---|
| `display` | 34sp | 600 | `ink` | onboarding hero, one per screen at most |
| `h1` | 28sp | 600 | `ink` | screen title |
| `h2` | 22sp | 600 | `ink` | section title |
| `h3` | 18sp | 500 | `ink-2` | card title |
| `body` | 14sp | 400 | `ink-2` | prose, list rows |
| `label` | 14sp | 500 | `ink-3` | field and row labels |
| `meta` | 12sp | 400 | `ink-muted` | timestamps, ids, counts |
| `micro` | 11sp | 500 | `ink-3` | uppercase, tracked +0.06em — used sparingly |

Rules:

- **Numbers are monospace, tabular, one decision.** Every dynamic number (tokens, cost, latency, quota, countdown, request id) uses the platform monospace with `FontFeatureSetting "tnum"`. Reason: an instrument panel's numbers must not jitter while counting, and alignment in a column is legibility, not decoration. This is the one place where type deviates from the platform default — a decision, not a default.
- Headings get slightly negative tracking; body text stays at default with line height ~1.5.
- Never more than one `display` and one `h1` on a screen. If two elements are the same size and weight, one of them has no job.
- Text never scales below 11sp, and everything survives 200 % font scale (T-106, T-188).

## 7. Space, shape, depth

| Scale | Values | Use |
|---|---|---|
| micro | 4, 8 | icon ↔ label, chip padding |
| component | 12, 16 | inside a card, row padding |
| section | 24, 32 | between groups on a screen |
| major | 48 | between a focal element and everything else |

4dp base, multiples only. **Uneven rhythm on purpose:** tight groups, wide gaps between groups — equal gaps everywhere is the reference sound of nothing being decided.

| Shape | Value |
|---|---|
| inputs, chips, small controls | 4dp |
| cards, list-row containers | 8dp |
| sheets, dialogs | 12dp |
| nested rounded elements | `outer = inner + padding` (concentric) |

**Depth strategy: borders only. Committed.** No elevation shadows, no glow, no blur, no layered shadows. Hierarchy comes from the surface step + border opacity. One strategy, everywhere, always — mixing a border card next to a shadow card is the most visible inconsistency an interface can have.

## 8. Screens: one focal point each

| Screen | Focal element | Everything else |
|---|---|---|
| Dashboard | the **Signalweg** (§4.2) | one hero number beside it; the rest is a labelled list, demoted |
| Providers | the list's *first actionable row* (needs-key or failing providers sort up) | filters collapse into a sheet |
| Routing | the **live explanation** of the current strategy for the selected model | the editor below it, never a wall of inputs |
| Local | the **loaded model** and its memory headroom, as one gauge | catalogue below |
| Settings | the **access state** (local-only vs. reachable) with its consequence | sections below, one decision per block |

Layout rules:

- **Name the focal element before writing the composable.** If it cannot be named, the screen is a list and should look like one.
- The eye must find the focal element in under a second; the *squint test* (§12.4) decides.
- Five destinations stay as they are (bottom navigation, `T-091`). No restructure: the tasks, the onboarding flow and the status files already reference these five screens.
- **Centering — decided.** Centered is allowed for exactly three things: the onboarding hero (one line, one action), empty-state content, and a single large metric. Running text, list rows, settings labels, log lines, table cells and error details stay **left-aligned**, because centered prose is measurably slower to read and ragged on a phone. Centering is a deliberate accent, not a layout default.

## 9. Data: numbers, charts, logs

- **Honest numbers only.** Unknown is rendered as *unknown* (hatched bar + the word). Estimated cost carries an *estimate* marker. No fabricated zero, no filled-in guess — this is the visual form of the repository's own rule against inventing values.
- **One comparison at a time.** A chart has one accent series plus at most one comparison hue; more than two series becomes a small multiple or a list, never a rainbow.
- Zero-baseline bars; no truncated axes; no 3D; no gradient fills; no drop shadows under the plot.
- Direct labels on the series beat a legend; a legend is the fallback when labels would collide.
- Tabular monospace figures (§6) so a counting number does not shift its neighbours.
- Log output is monospace, one line per record, level carried by a shape + word, long lines wrap rather than truncate silently, and every export is re-redacted ([`T-104`](../plan/phase-07-ui/T-104-logs-viewer.md)).
- Charts are hand-sized Compose, not a charting dependency ([`T-095`](../plan/phase-07-ui/T-095-usage-charts.md)); a canvas draws the bars, the tokens colour them.

## 10. States: the screen is not finished without them

Every interactive element: **default · hover (mouse/foldable) · focused · pressed · disabled**.
Every data-bearing area: **loading · empty · error · partial · offline**.

- Loading is a skeleton in the shape of the real content, not a spinner in the middle of an empty screen.
- Empty states say what to do next and offer the action (Dashboard's empty state is the onboarding's first step, not four zeros).
- Errors state the cause and the next action, in the vocabulary of the API (`parked until 00:00`, not `unavailable`).
- Failed values keep their last known value visible with a marker, rather than blanking the card.
- Disabled controls say *why* they are disabled, inline, not in a toast.

## 11. The craft tests

Run before showing any UI work. A screen that fails one is not finished, whatever the tests say.

| Test | Question | Fail looks like |
|---|---|---|
| **Swap** | Replace our type/layout with a stock template — does anything feel different? | everything, i.e. nothing was decided |
| **Squint** | Blur it: is the hierarchy still readable and is nothing shouting? | flat hierarchy, or one harsh border winning |
| **Signature** | Point at five places where the Signalweg idea appears. | "the overall feel" — that is not a place |
| **Token** | Read the token names aloud: do they belong to this product? | `gray-700`, `surface-2`, `#7C3AED` |

## 12. Accessibility floor (not optional, measured)

1. **Contrast**, measured and recorded: body ≥ 4.5:1, large text ≥ 3:1, UI component boundaries ≥ 3:1. Every foreground/background pair in both modes, with the ratio written down in the T-188 log.
2. **Not by colour alone:** shape + word alongside every status, chart series and error.
3. **Touch targets** ≥ 48dp (Android), never below 44dp, never overlapping.
4. **Reduced motion** (`Settings.Global.ANIMATOR_DURATION_SCALE == 0`): all movement replaced by opacity/colour change; the Signalweg becomes static and remains readable.
5. **Font scale 200 %:** no truncation, no overlap, no clipped controls.
6. **TalkBack:** every control has a meaningful description; the signal path announces its state in words, not as "image".
7. **Focus order** follows reading order; focus is always visible (`line-focus`).

## 13. The gate

```bash
python3 tools/check_design_slop.py          # scan the UI sources and the drawings in design/
python3 tools/check_design_slop.py --self-test   # prove the gate itself still bites
```

It fails on: a banned aesthetic (glass, blur, neumorphism, skeuomorphic gradients), decorative shadow/elevation, gradient brushes, hardcoded `Color(0x…)` outside `ui/theme/Tokens.kt`, spacing or radius values off the scales in §7, user-facing string literals in composables, and a missing state family for a screen that loads data. It is wired into CI (`.github/workflows/repo-hygiene.yml`), and it runs against a fixture in `--self-test` so a gate that has stopped working is itself a failure.

**The drawings are checked too.** The same run parses every `design/**/*.svg` as XML and applies the banned-aesthetic rules to the SVGs and to `design/preview.html` — gradient, filter, shadow and blur are refused there exactly as in a composable. Rationale: the mock-ups are what an agent copies when it implements the next screen, so a preview allowed to use a gradient would teach the wrong thing faster than a document could forbid it. `design/README.md` §2 states the rule; this is the enforcement.

Design work is not "done" because the gate passes. The gate catches what a machine can catch; §11 catches the rest.

---

<div align="center">

## 15. Mark, assets and motion

### 15.1 The mark: Signal

Chosen by the owner from four proposals (Signal, Weiche, Klinke, D als Schaltweg). An **open ring with one line through it** - a point passing through a gate. It is the smallest possible statement of what the product does, and it survives every size the platform demands.

Construction on a 24x24 grid: ring of radius 7 with a 2dp stroke, a 2dp line through it, and a 2dp-diameter point on the line. Nothing else - no second shape, no letter, no enclosure.

| Variant | Rule |
|---|---|
| On graphite | copper ring and point, `ink` line - the one place the accent carries the brand |
| Monochrome | single `ink` colour, same geometry; the point stays a distinct shape so it survives a tinted launcher |
| Adaptive icon | background layer = graphite flat fill, foreground layer = the mark inside the 66dp safe zone, monochrome layer = the mark alone |

Prohibited for the mark: gradient, drop shadow, glow, outline-on-outline, text inside the ring, a second accent colour, perspective. A mark that needs an effect to read is a failed mark.

The test before it is used anywhere: legible at 24dp, correct on graphite **and** on paper, correct inverted, correct in monochrome, and clean under a round mask.

### 15.2 Assets: where they live


| Path | Contains | Source of truth for |
|---|---|---|
| `design/logo/` | `signal-mark.svg`, `signal-adaptive-icon.svg` | the drawings |
| `design/icons/` | `droidroute-icons.svg` - the own set, as symbols with shared path data | the drawings |
| `design/mock/` | `dashboard.svg`, plus later mock-ups | layout intent, not implementation |
| `design/preview.html` | the living preview: tokens, type scale, components, motion, icon grid | what the system looks like assembled |
| `design/screenshots/` | the real captures, filled by T-197 | evidence |
| `design/analysis/`, `design/review/` | machine analysis and the visual Q&A documents, filled by T-198/T-199 | findings |

This document owns the rules; `design/` owns the drawings. If a drawing contradicts the rules, the drawing is wrong.

**Icon set.** Nine own icons cover the product's own concepts; everything else comes from Material Symbols. Own: signal path, provider, key, quota window, local model, MCP bridge, tunnel, cost, log stream. Grid 24x24, 2dp stroke, round caps and joins, no fills except a lamp dot, optically corrected (a circle is drawn slightly larger than a square of the same size). Own icons exist because the product's concepts have no standard glyph - not to avoid a dependency.

### 15.3 Motion: the Instrument level

The owner chose the middle level. Everything below is the complete allowed set; anything not listed is not allowed without a reason recorded in the task log.

| Moment | Motion | Duration | Why it earns its place |
|---|---|---|---|
| A request is in flight | the point travels the signal path | 240 ms | shows where the request is, and where it stopped |
| A lamp changes state | colour + scale from 0.95 to 1 with a fade | 180 ms | shows that the gateway heard the change |
| A number changes | count-up in tabular monospace | 400 ms max | the movement matches the change; tabular figures stop the layout shifting |
| A sheet or dialog opens | slide/fade, origin-aware for popovers, centred for dialogs | 220 ms in, 180 ms out | shows where the panel came from and where it goes back to |
| Reduced motion is on | the path is static with the failing hop marked; numbers jump | - | the information is identical, only the movement is gone |

Curve: `CubicBezierEasing(0.23f, 1f, 0.32f, 1f)` for entering and interactive motion, `CubicBezierEasing(0.77f, 0f, 0.175f, 1f)` for movement across the screen. Never the built-in ease-in: it delays the first frame, which is the frame the eye is watching.

Forbidden at this level: looping or ambient motion, a pulse or shimmer that waits for attention, parallax and depth effects, charts that grow in, stagger on list content, screen-transition choreography beyond the platform default, and any animation that runs on a repeated action (a command used a hundred times a day gets none).

Every animation states, in the task log, what it explains: state, causality, continuity or spatial change. "It feels nicer" is not one of the four.



</div>
