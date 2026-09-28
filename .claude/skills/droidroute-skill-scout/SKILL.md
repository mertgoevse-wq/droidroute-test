---
name: droidroute-skill-scout
description: Find and apply the right installed skill, plugin or MCP server before writing instructions by hand - search the global and project inventories, the design skill library, and the community skill index. Use at the start of an unfamiliar task, when no skill in status/TOOLING.md obviously fits, or when the user says "use your skills", "check what tools exist" or "search for a skill".
---

# Scout before you improvise

A hand-rolled procedure for something a skill already solves is duplicated work. Spend one minute looking.

## 1. Read what exists

```bash
python3 scripts/discover_tooling.py --json | head -60     # refresh + print the inventory
less status/TOOLING.md                                     # global skills by domain, plugins, MCP servers
ls .claude/skills .claude/agents                           # project scope
```

Precedence: **project skill > global skill > community skill > write it yourself.**

## 2. Search the community index when nothing fits

```bash
npx skills find <query>                 # search
npx skills add <owner/repo> --list      # preview a repo's skills
npx skills add <owner/repo> --skill <name> --yes   # install into .agents/skills/
```

Community skills are **not vetted**. Confirm with the owner before installing one from a repo you cannot inspect, and never install something that needs credentials you do not have.

## 3. Design work goes through the library

`~/.claude/design-skill-library` holds the curated design set (index and curation files included). For UI, colour, typography, motion or critique work, check it before reaching for generic advice; the `design-library` skill exposes it on demand.

## 4. MCP servers are the first option for data access

If a capability already exists as an MCP tool, use it instead of writing code to do the same thing. Check `status/TOOLING.md` (MCP section) and, once DroidRoute runs, `GET /mcp/tools`.

## 5. Record what you chose

```
skill-selection: droidroute-routing + superpowers:test-driven-development (verify workstream)
skill-substitution: security-audit -> android-intent-security (host has no generic security skill)
skill-install-request: <repo>/<skill> — asked the owner before installing
```

An unrecorded choice looks like an accident to whoever resumes the work.
