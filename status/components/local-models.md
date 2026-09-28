# Component: local-models

**Purpose:** run models on the phone itself, managed honestly — no artificial size cap, but no silent memory ambushes either.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-107 … T-117 |
| Owns | `com.droidroute.local` + `com.droidroute.bridge` |
| Depends on | core-server (provider registration), provider-layer |

## Deliverables

- Runtime resolution in the documented order (Termux package → build from source in Debian → prebuilt aarch64 binary), with the winning path recorded and shown.
- Termux bridge: RUN_COMMAND intent client with HTTP fallback; start/stop/status for the runtime.
- Model catalog: scan `.gguf` files, curated "known good on 8 GB" list, downloads with resume and checksum.
- RAM estimate before load, colour-coded warning, never a silent kill; idle unload under memory pressure.
- Registration as a normal provider (`local/llamacpp/<model>`) so routing, logging and MCP work unchanged.
- Special models: embeddings, whisper STT, TTS (clear `not_supported` when missing), small VLMs.

## Open risks

- GPU layer support (`-ngl`) varies by driver and model; it must be measured per model, never assumed.
- The embedded (JNI) runtime is out of v1 scope — a spike task records the go/no-go.

## Evidence log

_No entries yet._
