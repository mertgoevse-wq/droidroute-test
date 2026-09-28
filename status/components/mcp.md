# Component: mcp

**Purpose:** every MCP server, plugin and connector that is already connected gets discovered, shown and used — not re-invented.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-118 … T-126 |
| Owns | `com.droidroute.mcp` |
| Depends on | core-server, Termux bridge |

## Deliverables

- Discovery across Claude Code, Freebuff/Codex-style, Cursor-style and owner-defined config paths, with file watching.
- Aggregated registry (`~/.droidroute/mcp.registry.json`) with `source`, `transport`, `enabled`, `last_status`, `tools[]`; secrets redacted everywhere.
- Bridge API: `/mcp/servers`, `/mcp/tools`, `/mcp/{id}` JSON-RPC pass-through, `/mcp/refresh`, ping with tool refresh.
- stdio servers launched inside Termux/Debian, `http`/`sse` called directly; stderr tails captured (redacted) for failures.
- Connectors screen: provider, GitHub, tunnel and search connectors with their real state.
- Plugin inventory endpoint (`GET /plugins`) so an agent can see what the host offers.

## Open risks

- Config formats differ per tool and change between versions; parsing must be tolerant and report "unknown format" rather than silently dropping servers.
- A stdio server that never terminates must not block a task — timeouts and process reaping are mandatory.

## Evidence log

_No entries yet._
