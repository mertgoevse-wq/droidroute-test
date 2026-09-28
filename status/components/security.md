# Component: security

**Purpose:** make the security claims checkable — a threat model with a test per threat, and reviewed secret storage, network surface, app surface and supply chain.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-191 … T-196 |
| Owns | threat model, static analysis and dependencies, vault crypto, network exposure, components and data at rest, signing and audit trail |
| Depends on | core-server, accounts-oauth, protocols, delivery, design |
| Canonical docs | [docs/05-security.md](../../docs/05-security.md) — the standing rules · `docs/16-threat-model.md` and `docs/17-security-audit.md` are *created by this phase* and are named here, not linked, until they exist |

## Deliverables

- Threat model with assets, entry points, boundaries and a test (or an accepted risk) per threat (T-191).
- Pinned dependencies with licences and purposes, and lint security checks that fail the build (T-192).
- Vault review with nonce, tamper and revocation tests, plus the list of what is *not* protected (T-193).
- Exposure matrix where every bind/auth combination has a test, TLS verified, cleartext to public hosts refused (T-194).
- No component exported without a reason, every intent extra validated, vault excluded from backup (T-195).
- Actions pinned by SHA, minimal workflow permissions, published checksums, an append-only audit record (T-196).

## Open risks

- A rooted device and a device-unlocked attacker are out of scope. This must be written down, not implied away.
- An offline audit cannot query a live advisory database; the report has to say which tooling ran and what it could not see.
- The strongest control in this phase is the *test* behind each claim. A threat model with an untested row is documentation, not security.
- `docs/16-threat-model.md` and `docs/17-security-audit.md` are produced by these tasks. Until they exist, nothing links to them and no document may cite findings from them.

## Evidence log

_No entries yet._
