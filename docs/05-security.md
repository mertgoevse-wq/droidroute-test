# Security

## Threat model

The phone is the only machine involved, but it holds a lot of credentials. The realistic risks are: a stolen/unlocked device, a malicious app on the same device reading app-private files, an accidental `git push` of a key, and an over-eager external bind that exposes the port to the internet.

## Secret storage

| Rule | Implementation |
|---|---|
| Keys never stored in plaintext | `KeyVault`: AES-256-GCM, per-record random IV, key material wrapped by Android Keystore (`setUserAuthenticationRequired(false)` so long-running agents survive screen locks) |
| Keys never leave the app except to their provider | no telemetry, no cloud sync, no backup of vault files (`android:allowBackup="false"` for the vault dir) |
| Reveal once | plaintext is shown at entry time; afterwards `first5••••last5` |
| Explicit reveal | an extra "reveal" action requires device-credential confirmation (BIOMETRIC_STRONG or device PIN) and is logged |
| Copy | "copy to clipboard" auto-clears after 60 s |
| Delete | removing a key wipes the vault record and its quota ledger in one transaction |
| Screenshots | `FLAG_SECURE` on key-entry and reveal screens only |

Masking format is fixed: first 5 and last 5 characters, `••••` for anything longer than 12 characters; shorter keys show only the first 3 and a fixed bullet run (never enough to reconstruct).

## Auth modes

| Mode | Behaviour | Use |
|---|---|---|
| `none` | no header required | localhost only; ideal for Termux agents on the same device |
| `api_key` | `Authorization: Bearer <key>` or `x-api-key: <key>`; keys are generated in-app (`dr_` + 32 random chars), hashed at rest (salted SHA-256), shown once, individually revocable | laptop over LAN, tunnel mode |
| `oauth` | device/browser flow issuing short-lived tokens (default 24 h) with refresh | clients that support interactive login |

Multiple client keys can exist at once (one per agent/machine), each with its own name, created date, last-used date and revoke button. The default for a fresh install is `none` **bound to localhost** — the safe combination.

## Bind modes

| Mode | Bind address | Auth floor enforced by the app |
|---|---|---|
| Local only (default) | `127.0.0.1` | `none` allowed |
| LAN | `0.0.0.0` | `api_key` mandatory |
| External (tunnel/tailnet) | `0.0.0.0` | `api_key` mandatory + warning screen + explicit confirmation checkbox |

The app refuses to start a non-local bind with `none` and writes the refusal to `status/ERRORS.md`-style app logs. There is no hidden override.

## Redaction

A single `Redactor` runs on every log line, HTTP response and error body. It masks: known key values (by matching vault entries), `Authorization`/`x-api-key` headers, `api_key`/`token`/`password` JSON fields, cookie values, and anything matching the common key shapes (`sk-…`, `ghp_…`, `gho_…`, `AIza…`, `pplx-…`). The repository's test suite asserts that a canary key never appears in any log.

## Repository hygiene

- `.gitignore` blocks `*.key`, `*.pem`, `secrets/`, `local.properties`, `*.keystore`, `*.jks`, `.env*` (except `.env.example`).
- `assets/providers/*.example.json` files carry placeholder keys only.
- A pre-commit check (`scripts/preflight-secrets.sh`) greps staged files for the known key patterns and aborts with a clear message.
- `status/*` and `logs/*` files are redacted before being written, since they are pushed to the repository.

## Network

- No certificate pinning on provider calls (providers rotate certificates; pinning would break the app), but TLS verification is never disabled.
- No `usesCleartextTraffic` except for `127.0.0.1` and the private LAN ranges the owner enabled, declared via a network security config.
- The app only calls a provider after the owner enabled it; there is no catalogue-wide "phone home".

## Permissions

| Permission | Why | Scope |
|---|---|---|
| `INTERNET` | provider calls, MCP HTTP servers | always |
| `FOREGROUND_SERVICE` + `FOREGROUND_SERVICE_DATA_SYNC` | keep the server alive | always |
| `POST_NOTIFICATIONS` | the persistent status notification | always |
| `com.termux.permission.RUN_COMMAND` | start/stop llama.cpp, run scripts | optional, requested when the owner first uses a Termux feature |
| Storage (SAF) | export/import a manifest or a model file | optional, per action |
| Biometric | key reveal | optional, per action |

Denying a permission degrades one feature and never crashes the app or the server.
