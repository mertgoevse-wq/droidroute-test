# Logging Standard

Everything is logged: every command, every file written, every verification result, every error, every decision. The logs are pushed to the repository, so they are redacted by default — a log that contains a secret is a bug.

## Layout

```
logs/
├── chain.log              # one line per task transition — never pruned
├── tasks/
│   ├── T-001.log
│   └── T-147.log          # last 60 kept
├── daily/
│   └── 2026-09-28.log     # last 14 days kept
└── archive/               # pruned content, git-ignored
```

## Record format

Line-oriented JSON, one record per line, UTF-8, no trailing prose:

```json
{"ts":"2026-09-28T16:41:07+02:00","task":"T-042","actor":"implement","level":"info","action":"write","target":"app/src/main/kotlin/com/droidroute/routing/QuotaLedger.kt","result":"created","dur_ms":812,"extra":{}}
```

| Field | Rules |
|---|---|
| `ts` | ISO-8601 with UTC offset, local timezone |
| `task` | `T-0xx` or `chain` |
| `actor` | `main`, or the workstream name (`implement`, `verify`, `docs`) |
| `level` | `debug` \| `info` \| `warn` \| `error` |
| `action` | `read` \| `write` \| `edit` \| `run` \| `test` \| `commit` \| `push` \| `decide` \| `error` |
| `target` | file path, command, or endpoint |
| `result` | short outcome (`created`, `pass`, `fail: timeout`, `skipped: no credentials`) |
| `dur_ms` | duration when meaningful, else omitted |
| `extra` | free-form object; keys must never contain secret values |

Write with `scripts/log-step.sh` (shell) or the app's `LogWriter` (Kotlin). Both apply the same redactor and the same format, so human and machine logs are identical in shape.

## What must be logged

- Start and end of every task, with the task id and the skills dispatched.
- Every verification command **verbatim** plus its raw result (pass/fail and the relevant output lines).
- Every acceptance criterion tick, naming the evidence.
- Every error, including ones that were handled — with the reason they were handled silently, if at all.
- Every deviation: a substituted skill, a serialised workstream, a reordered step, an environment limitation.
- Credential validation calls: provider id, key label, outcome. **Never** the key value.

## What must never be logged

Key values, `Authorization` headers, cookies, session tokens, vault ciphertext, full MCP `env` blocks, personal data from the owner's documents. The redactor catches known patterns, but do not rely on it — do not pass a secret to the logger in the first place.

## Rotation

`scripts/weekly-cleanup.sh` (also scheduled by the `repo-hygiene` workflow):

- keep 14 days of `logs/daily/`, 60 newest `logs/tasks/`, `chain.log` forever;
- move pruned files to `logs/archive/` (git-ignored) instead of deleting them immediately;
- print a one-line summary into `logs/daily/<today>.log`.

## Reading the logs

```bash
grep '"task":"T-042"' logs/tasks/T-042.log | tail -20
jq -r 'select(.level=="error") | .ts + " " + .task + " " + .result' logs/tasks/*.log
tail -n 50 logs/chain.log
```

The logs are the evidence base for `docs/10-acceptance.md`. If a criterion cannot be evidenced from a log line, it was not verified.
