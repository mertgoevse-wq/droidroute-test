# Logs

The audit trail. Committed on purpose: these files are how a different model picks up the work and how every acceptance criterion in `docs/10-acceptance.md` is evidenced.

| Path | Content | Retention |
|---|---|---|
| `chain.log` | one record per task transition, commit and push | never pruned |
| `tasks/T-0xx.log` | everything that happened in one task | newest 60 |
| `daily/YYYY-MM-DD.log` | all records of one day, all tasks | newest 14 days |
| `archive/` | pruned files moved here | local only, git-ignored |

Format: line-oriented JSON, redacted. Full spec in [`handbooks/05-logging-standard.md`](../handbooks/05-logging-standard.md).

Write a record with:

```bash
scripts/log-step.sh T-042 "test" "gradle testDebugUnitTest --tests '*QuotaLedgerTest'" "pass" --actor verify --dur 4210
scripts/log-step.sh T-042 "error" "provider call" "fail: timeout" --level error --extra '{"provider":"bynara"}'
```

Read them with:

```bash
tail -n 50 logs/chain.log
grep '"task":"T-042"' logs/tasks/T-042.log | tail -20
jq -r 'select(.level=="error") | .ts + "  " + .task + "  " + .result' logs/tasks/*.log
```

Rotation runs weekly via `.github/workflows/repo-hygiene.yml` or by hand: `scripts/weekly-cleanup.sh [--dry-run]`.

**Never log a secret.** The script redacts known key shapes, but do not hand it a credential in the first place.
