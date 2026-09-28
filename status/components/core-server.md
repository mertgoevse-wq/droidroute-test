# Component: core-server

**Purpose:** keep a Ktor server alive in a foreground service, on a configurable port, with a bind mode that cannot accidentally expose the phone.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-011 … T-023 |
| Owns | `com.droidroute.server` |
| Depends on | T-001 … T-010 (scaffold, CI, scripts) |

## Deliverables

- Foreground service lifecycle with `START_STICKY` and a persistent notification (port, bind mode, request counter).
- Ktor CIO server bootstrap, graceful start/stop/rebind.
- `ServerConfig`: port (default 8787), bind mode (`local`, `lan`, `external`), auth floor per mode.
- Port collision detection with a suggested free port.
- `/health` endpoint and uptime/version reporting.
- On-boot restart handling (opt-in) and clean state rehydration from Room/DataStore.

## Open risks

- Android 15 foreground-service type requirements (`dataSync`) must be declared exactly, or the service is killed at start.
- Doze mode may delay rebinds; the notification must reflect reality rather than intent.

## Evidence log

_No entries yet._
