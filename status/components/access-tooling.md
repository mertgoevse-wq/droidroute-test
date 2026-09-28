# Component: access-tooling

**Purpose:** getting started costs one tap and no identity; DroidRoute's own keys are readable by nobody; and the build agents use the tools that exist instead of the three they remember.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-203 … T-208 |
| Owns | one-tap free start, device-code sign-in, local-only key issuing, tooling coverage, the reusable workflow plugin, clone-from-scratch freeze |
| Depends on | accounts-oauth, ui, routing, security |
| Canonical docs | [status/TOOLING.md](../TOOLING.md) · [handbooks/09-skill-resolution.md](../../handbooks/09-skill-resolution.md) |

## Deliverables

- One tap, no account, no key typed, and a verified working endpoint — with the per-candidate reasons when nothing answers (T-203).
- Device-code sign-in reused by onboarding, provider list and provider detail (T-204).
- Issued keys shown once, masked afterwards, scoped, revocable, and unreadable by anyone including the owner — enforced by a test that fails if a read-back path appears (T-205).
- `status/TOOLING-COVERAGE.md`: every installed skill, plugin and MCP server used or declined with a reason; CI fails while one is undecided (T-206).
- The build workflow packaged as an installable plugin, consumed here, published in its own private repository with a leak check (T-207).
- A recorded clone-from-scratch drill: clone → bootstrap → all checks green → a fresh agent completes one task (T-208).

## Open risks

- "No account" depends on third-party free tiers that change without notice. The probe order is evidence-based and the failure path is the honest one, but a day with no free capacity is possible and must be shown as such.
- The key-issuing claim is an *absence* claim, which is the hardest kind to test. The test has to search for a read-back path rather than assert one is missing.
- A coverage report can be gamed by marking everything `declined`. The reason field is the control, and the review is where it is checked.
- The workflow plugin and this repository must not drift into two copies of the same file. Whatever the plugin owns, this repository references.

## Evidence log

_No entries yet._
