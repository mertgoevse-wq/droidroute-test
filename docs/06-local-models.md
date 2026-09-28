# Local Models

Local models make DroidRoute useful with no network at all. On a Galaxy A56 (Exynos 1580, 8 GB RAM) the honest expectation is small quantised models: usable for summaries, classification, small code edits and offline fallback — not a replacement for a hosted frontier model.

## Runtime resolution (see TBC-6)

Ordered, evaluated at first use and re-evaluated on demand:

1. `pkg install llama-cpp` inside Termux (aarch64 community build) — preferred.
2. Build from source in proot-Debian: `cmake -B build -DGGML_NATIVE=ON -DLLAMA_BUILD_SERVER=ON`, then `build/bin/llama-server`.
3. Prebuilt `llama-server` for `linux-arm64`, unpacked into `~/.droidroute/runtimes/llama.cpp/<version>/`.

The resolved path, version and capability probe (`llama-server --version`) are stored, displayed in the UI, and shown in `/health`. If none resolves, the local-model screen explains exactly which of the three options failed and why.

## Process control

- DroidRoute starts the runtime **inside Termux/Debian** (never in the app process) and talks to it over `127.0.0.1:<model-port>`.
- Each loaded model gets its own port from a reserved local range; the app registers it as a normal provider id `local/llamacpp/<model>` so routing, logging, metrics and MCP treat it like any other provider.
- Lifecycle: `load`, `unload`, `idle-unload after N minutes` (default 15, configurable, off for pinned models).
- The `.gguf` file stays where the owner put it; DroidRoute stores a pointer, never a copy, unless the owner imports one into `~/.droidroute/models/`.

## Memory safety

There is **no size limit** — the owner asked for that explicitly — but the app is never silent about the risk:

- Before loading, DroidRoute estimates need = file size + KV cache (context × layers × head dim) + ~200 MB overhead, and compares it to available RAM.
- Estimate > 70 % of available RAM → yellow warning with the numbers and a "load anyway" action.
- Estimate > available RAM → red warning stating that Android may kill the backend or the app, plus the recommendation to lower `-c` (context) or pick a smaller quant.
- Loaded state is shown permanently: model, quant, context, estimated RAM, tokens/s so far.
- An idle watchdog unloads a model that has produced no request for N minutes when memory pressure is reported by Android (`onTrimMemory`).

## Defaults for this device

| Setting | Default | Reason |
|---|---|---|
| Threads `-t` | 4 | A56 big cores; more threads oversubscribe |
| GPU layers `-ngl` | 0, offered up to detected max | OpenCL/Vulkan support varies; measured per model, not assumed |
| Context `-c` | 4096 | KV cache is the main RAM consumer |
| `--mlock` | off | Would fight Android's memory manager |
| Quant guidance | Q4_K_M sweet spot; Q5/Q6 warned | Quality per byte |

## Model catalog

- Owner-provided `.gguf` files are scanned (a folder the owner picks, plus `~/.droidroute/models/`).
- A curated "known good on 8 GB" list is bundled with sizes and expected tokens/s, so the owner can download a proven model in one tap.
- Each entry shows: size, quant, parameter count, context, licence, source URL, and a compatibility badge (`comfortable`, `tight`, `risky`) computed from the device's real available RAM at scan time.
- Download runs in the foreground service with resume support and a checksum check.

## Special models

| Kind | Handling |
|---|---|
| Embeddings | loaded by the same runtime (`--embeddings`), exposed as `/v1/embeddings`, tagged so the router never sends chat traffic to them |
| Speech-to-text | whisper.cpp (same resolution strategy), exposed as `/v1/audio/transcriptions` |
| Text-to-speech | resolved separately; if unavailable, the endpoint reports a clear `not_supported` error naming the missing runtime |
| Vision | multimodal `.gguf` (e.g. small VLMs) exposed as normal chat models with image parts, RAM warning adjusted upward |

Embedded (JNI) runtime stays out of v1: it is tracked as a dedicated spike task with a go/no-go decision recorded in `status/DECISIONS.md`.
