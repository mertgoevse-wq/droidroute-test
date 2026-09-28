<div align="center">

# DroidRoute — Design drawings

**Where the system is drawn, not described.** The rules live in [`docs/14-design-system.md`](../docs/14-design-system.md); this folder holds the artefacts. If a drawing contradicts the rules, the drawing is wrong.

`Direction: Graphit-Instrumententafel · Akzent: Kupfer · Marke: „Signal“ · Signatur: der Signalweg`

</div>

---

## 1. What is in here

| Path | What it is | Source of truth for |
|---|---|---|
| [`logo/signal-mark.svg`](logo/signal-mark.svg) | The mark "Signal" on graphite, on paper, in monochrome, plus a 48/32/24 dp size proof | the mark |
| [`logo/signal-adaptive-icon.svg`](logo/signal-adaptive-icon.svg) | The three adaptive-icon layers with the 66 dp safe zone drawn, and three mask proofs | the launcher icon |
| [`icons/droidroute-icons.svg`](icons/droidroute-icons.svg) | The nine own icons on the 24×24 grid, with a legibility proof at 20 dp and 16 dp | the own icon set |
| [`mock/dashboard.svg`](mock/dashboard.svg) | The Dashboard layout in both modes, annotated with the tokens it uses | layout intent — *not* implementation |
| [`preview.html`](preview.html) | The living preview: palette, type scale, space, components, states, motion, icon grid | what the system looks like assembled |
| `screenshots/` | Real captures from the running app — filled by [`T-197`](../plan/phase-16-visual-evidence/T-197-screenshot-harness.md) | evidence |
| `analysis/` `review/` | Machine analysis and the visual Q&A documents — filled by `T-198`, `T-199` | findings |

Open a drawing with `python3 -m http.server` in the repository root and browse to `/design/preview.html`; the SVGs also open directly.

## 2. The rules these drawings follow

Every drawing in this folder is bound by [`handbooks/07-anti-slop-rules.md`](../handbooks/07-anti-slop-rules.md) §11–§14 and by §4–§12 of [`docs/14-design-system.md`](../docs/14-design-system.md). In short, and without exception:

1. **Borders only.** No gradient, no drop shadow, no glow, no blur, no glass — not even to make a preview look polished.
2. **One accent.** Copper, exactly one per drawing, and never used for a status. Status is carried by the real lamp colours in §5.5.
3. **Drawings do not invent.** Every colour comes from §5, every size from §6/§7, every duration from §15.3. A value that appears in a drawing and not in the system is a defect in the drawing.
4. **Unknown is drawn as unknown.** If a value would be unknown in the app, the drawing shows the hatched marker and the word — never a confident number.
5. **A drawing states its own limits.** `mock/dashboard.svg` is layout intent; it is not a screenshot and must never be presented as one. Screenshots live in `screenshots/` and are produced by the harness.

## 3. Colour, for reference while drawing

Copy from here; do not re-derive. Full method and the measured contrast table are in §5.7.

| Role | Dark | Light |
|---|---|---|
| canvas | `#0E1217` | `#F5F7F9` |
| surface-1 / surface-2 / surface-3 | `#151A1F` / `#1C2126` / `#22272C` | `#FFFFFF` / — / — |
| inset | `#080C10` | `#F0F2F4` |
| ink / ink-2 / ink-3 / ink-muted | `#E5E8EB` / `#B4B8BC` / `#8E9398` / `#898E94` | `#161B20` / `#3E4349` / `#595E63` / `#65696F` |
| ink-disabled | `#62676C` | — |
| accent / accent-ink / accent-quiet | `#DE8F57` / `#1D140D` / `#3B2617` | `#AC5500` / `#FFFCF8` / — |
| ok / warn / err / info | `#71C38F` / `#F0B55D` / `#E66E68` / `#88B8DA` | `#00864B` / `#B37000` / `#CC3336` / `#0070A6` |
| border / hairline | `ink` at 12 % / 8 % | `ink` at 12 % / 8 % |

## 4. How an asset gets added

1. Draw it against the grid (24×24, 2 dp stroke, round caps) or against the token values above.
2. Add the row to the table in §1 — an undrawn asset that is listed is worse than one that is missing.
3. Open it at its smallest real size before it is used anywhere: 24 dp for the mark, 20 dp for an icon, 360 dp wide for a screen.
4. Commit the drawing and the reference together. There is no separate asset pipeline: SVG sources are committed, and the Android vector drawables are derived from them in `T-202`.
