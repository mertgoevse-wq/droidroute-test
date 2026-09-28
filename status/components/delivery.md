# Component: delivery

**Purpose:** prove the app works, ship it as an APK, and leave the repository in a state a future agent can operate.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-136 … T-147 |
| Owns | build, CI, signing, acceptance evidence, owner documentation |
| Depends on | all other components |

## Deliverables

- Performance pass: battery drain while idle with one connected agent, memory ceiling, Compose recomposition hot spots.
- Security review against `docs/05-security.md`: redaction canary test, bind-mode refusal test, keystore round-trip, permission minimisation.
- Dependency and licence review recorded in `status/DECISIONS.md`.
- Full acceptance run against `docs/10-acceptance.md` with per-criterion evidence in `logs/`.
- Release pipeline verified: tag → signed APK → checksums → release notes.
- Owner documentation: install, first run, connect Claude Code and Freebuff, add a provider, enable a local model, enable MCP — in German where the owner reads it.
- A resume drill: a fresh session continues the chain using only `status/` and `plan/`.

## Open risks

- Signing secrets must be configured in the repository before the first tag, or the release job fails by design (it refuses to build unsigned releases).
- The acceptance run needs the owner's real accounts for A3/A4 — everything else must be provable without them.

## Evidence log

_No entries yet._
