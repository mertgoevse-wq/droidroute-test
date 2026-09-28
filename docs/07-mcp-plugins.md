# MCP, Plugins & Connectors

The owner's requirement is blunt: **every connected MCP server, plugin and connector must be used.** DroidRoute therefore discovers them from where they already live, aggregates them, and serves them to agents over the local API.

## Discovery sources

| Source | Paths (evaluated in order, later wins on id collision) |
|---|---|
| Bundled defaults | `assets/mcp/defaults.json` (shipped examples, disabled by default) |
| Claude Code | `~/.claude.json`, `~/.claude/settings.json`, `<project>/.mcp.json`, `<project>/.claude/settings.json` |
| Freebuff / Codex-style | `~/.codex/config.toml`, `~/.config/freebuff/*.json` |
| Cursor-style | `<project>/.cursor/mcp.json` |
| Owner-defined | `~/.droidroute/mcp.json` |

Paths are relative to the Termux home (`/data/data/com.termux/files/home`) and/or the proot-Debian root, both of which the app can read via the configured Termux integration. Discovery runs at startup, on manual refresh, and whenever a watched file changes.

## Aggregated registry

`~/.droidroute/mcp.registry.json`, one entry per server:

```json
{
  "id": "filesystem",
  "name": "Filesystem",
  "source": "~/.claude.json",
  "transport": "stdio",
  "launch": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/sdcard/droidroute"] },
  "env_keys": ["ALLOWED_DIRS"],
  "enabled": true,
  "last_status": { "state": "ok", "checked_at": "2026-09-28T16:40:00Z", "tools": 7 }
}
```

Rules:
- **Secrets are redacted** in every HTTP response and never written to the repository; `env_keys` lists *names*, not values.
- `enabled` defaults to the source's own state: if Claude Code had it active, DroidRoute treats it as active.
- A server that fails to start is reported with its stderr tail (redacted) instead of disappearing.

## Bridge API

| Endpoint | Method | Purpose |
|---|---|---|
| `/mcp/servers` | GET | aggregated registry, secrets redacted |
| `/mcp/servers` | POST | add/override an entry (owner-defined source) |
| `/mcp/servers/{id}/ping` | POST | liveness check + `tools/list` refresh |
| `/mcp/tools` | GET | flattened tool index: `tool → server → description → input schema` |
| `/mcp/{id}` | POST | JSON-RPC pass-through: `initialize`, `tools/list`, `tools/call` |
| `/mcp/refresh` | POST | force re-discovery from all sources |

`stdio` transports are launched by the bridge inside the Termux/Debian environment, long-lived, with stdout/stderr captured into the log stream. `http` and `sse` transports are called directly.

## Plugs and connectors

| Concept | Meaning here |
|---|---|
| **Connector** | An outbound integration DroidRoute uses on behalf of agents: a provider adapter, a GitHub token for repo actions, a Tailscale/Cloudflare tunnel, a search backend. Connectors are configured in the Connectors screen and appear in `/v1/providers` or `/health` depending on kind. |
| **Plugin** | A capability bundle attached to the *build* toolchain (Claude Code skills, agent plugins). DroidRoute exposes the inventory read from the host environment at `/plugins` (read-only) so an agent can see what it has available without shelling out. |
| **Skill** | A reusable instruction pack for an agent. `handbooks/03-skills-catalog.md` lists the ones this project relies on; the runtime inventory is whatever the host reports. |

## Use-by-default policy

- All discovered servers that the source marked enabled are **enabled in DroidRoute too** — the app does not silently second-guess the owner.
- Agents are expected to consult `/mcp/tools` before writing new tool code; if a capability already exists as an MCP tool, it is used instead of reimplemented. This is stated as a hard rule in `CLAUDE.md` and `AGENTS.md`.
- A task that adds a new MCP server must also add it to `~/.droidroute/mcp.json` (owner-defined source) so it survives a fresh install, and document it in `docs/07-mcp-plugins.md`.

## Failure etiquette

- A dead MCP server never blocks a build task: it is marked `unavailable`, the task notes the degraded path, and work continues. Repeated failure is recorded in `status/ERRORS.md`.
- Tools that mutate the owner's data (deleting files, pushing code) require an explicit confirmation step in the task that uses them; read-only tools do not.
