<div align="center">

# DroidRoute — Design System

**One direction, decided once, applied everywhere.**

`Direction: Graphit-Instrumententafel · Akzent: Messing · Signatur: der Signalweg`

Rules that bind agents: [`handbooks/07-anti-slop-rules.md`](../handbooks/07-anti-slop-rules.md) §11–§14
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
| Is it still true | `python3 tools/check_design_slop.py` (CI) |

No theme package writes its own design note. Token names and values live here and in `ui/theme/Tokens.kt`; if the two disagree, the Kotlin is wrong.

## 4. Direction

### 4.1 The world this product lives in

DroidRoute is a **switchboard**. Requests arrive, are examined, and are switched to one of many lines. That world has real objects, and the interface borrows from them instead of from "SaaS dashboard".

| Axis | Decision | Consequence |
|---|---|---|
| **Domain vocabulary** | switchboard, patch panel, line, lane, signal, relay, patch cable, circuit, toll, meter, timetable, relief (Ablösung), slot | Labels use the product's real nouns; the router's own terms (`provider`, `key`, `quota`, `breaker`) stay in English |
| **Colour world** | dark bakelite panel, engraved labels, signal lamps (green / amber / red), brass terminals, manila timetable paper, cable jackets in muted slate and olive | graphite structure + one brass accent + real lamp colours |
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
| Gradient or glass hero, coloured card fills | flat surfaces, hairline borders, one brass accent used only for the primary action |
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

| Token | OKLCH | Level |
|---|---|---|
| `ink` | `oklch(0.930 0.005 250)` | primary — never pure white |
| `ink-2` | `oklch(0.780 0.008 250)` | secondary / supporting |
| `ink-3` | `oklch(0.660 0.010 250)` | tertiary / labels |
| `ink-muted` | `oklch(0.545 0.010 250)` | metadata, disabled |

Hierarchy comes from **size + weight + colour together**. A single 14sp size holds three tiers: `value 600/ink`, `label 500/ink-3`, `meta 400/ink-muted`.

### 5.4 Accent — exactly one, and it is not a status colour

| Token | OKLCH | Role |
|---|---|---|
| `accent` | `oklch(0.800 0.115 080)` | brass. The one primary action per screen, focus-adjacent emphasis, the active destination |
| `accent-ink` | `oklch(0.220 0.020 080)` | text/icons **on** an accent fill |
| `accent-quiet` | `oklch(0.300 0.035 080)` | accent-tinted container when a filled control would be too loud |

Rules: one accent per screen; the accent never appears on a status chip, a lamp or a chart series (see §5.5); ~10 % of pixels at most.

### 5.5 Status — real lamps, never colour alone

| Token | OKLCH | Meaning |
|---|---|---|
| `ok` | `oklch(0.750 0.110 155)` | healthy, quota available |
| `warn` | `oklch(0.810 0.125 075)` | degraded, near a limit, breaker half-open |
| `err` | `oklch(0.680 0.150 025)` | failing, quota exhausted, breaker open |
| `info` | `oklch(0.760 0.070 240)` | neutral system fact |
| `unknown` | `ink-3` + hatch pattern | value not known — **never** rendered as a neutral ok |

Every status is carried by **colour + shape + label** together: a filled circle, a half-filled circle, a bar, a triangle — plus the word. `warn` sitting near the brass accent is deliberate and safe because the accent never marks state, and every lamp carries a shape and a word.

Constraints: body text ≥ 4.5:1, large text and UI components ≥ 3:1, no meaning conveyed by hue alone, all pairs verified during T-188 with recorded ratios.

### 5.6 Light mode ("Timetable")

`canvas oklch(0.975 0.004 250)` · `surface-1 oklch(1.0 0 0)` · `inset oklch(0.960 0.004 250)` · `ink oklch(0.220 0.012 250)` · `ink-2 oklch(0.380 0.012 250)` · `ink-3 oklch(0.480 0.012 250)` · accents and status colours keep their hue with lightness shifted for ≥ 4.5:1 on light surfaces. Same hierarchy, inverted values, same single hue.

### 5.7 Dynamic colour

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
python3 tools/check_design_slop.py          # scan the UI sources
python3 tools/check_design_slop.py --self-test   # prove the gate itself still bites
```

It fails on: a banned aesthetic (glass, blur, neumorphism, skeuomorphic gradients), decorative shadow/elevation, gradient brushes, hardcoded `Color(0x…)` outside `ui/theme/Tokens.kt`, spacing or radius values off the scales in §7, user-facing string literals in composables, and a missing state family for a screen that loads data. It is wired into CI (`.github/workflows/repo-hygiene.yml`), and it runs against a fixture in `--self-test` so a gate that has stopped working is itself a failure.

Design work is not "done" because the gate passes. The gate catches what a machine can catch; §11 catches the rest.

---

<div align="center">

*DroidRoute should look like an instrument, not like a generated dashboard.*

</div>
