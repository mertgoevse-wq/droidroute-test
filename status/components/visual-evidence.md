# Component: visual-evidence

**Purpose:** make the interface visible and checkable — deterministic screenshots, machine analysis, a visual Q&A loop, a gallery CI keeps true, and a launch video made from the real product.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-197 … T-202 |
| Owns | screenshot harness, automatic visual analysis, visual Q&A, README gallery, launch video, launch assets |
| Depends on | ui (phase 07), design audit (phase 14) |
| Canonical docs | [docs/14-design-system.md](../../docs/14-design-system.md) §11–§13 |

## Deliverables

- One command reproduces the whole screenshot matrix (screens × modes × widths × states) deterministically (T-197).
- Deterministic analysis with measured values, plus an advisory craft pass that is labelled advisory (T-198).
- Every finding closed by an after-picture, with a named focal element per screen and a residual list (T-199).
- A README gallery generated from the files on disk, with a CI staleness check (T-200).
- The launch video from `plugin:brag` with poster and share copy, or a recorded reason it could not be produced (T-201).
- Own icon set, adaptive launcher icon, store graphics from real screenshots, and the A18 evidence chain (T-202).

## Open risks

- The launch video needs Node 22+ and FFmpeg on `PATH`. The phone may not have them; the honest paths are CI or another machine, and a documented gap — never a described video that does not exist.
- Golden-image diffing cries wolf on rendering noise. The tolerance is a decision, and it has to be written down where the failure is read.
- A screenshot review that finds nothing is usually a shallow review. At least one finding per pass should be a removal, or the reason none was possible is stated.
- Committed images grow the repository. The weight budget in T-200 is the control, not good intentions.

## Evidence log

_No entries yet._
