# Git Protocol

## Identity and remote

```bash
git config user.name                 # Mert Zet
git config user.email                # 240211895+mertgoevse-wq@users.noreply.github.com
git remote -v                        # origin → github.com/mertgoevse-wq/droidroute (private)
```

Never change global git config. Never add a second remote. Never commit with a different identity.

## The one sanctioned commit path

```bash
scripts/step-commit.sh "T-042: implement quota ledger"
scripts/step-commit.sh --checkpoint "T-043"          # lightweight tag before starting a risky task
scripts/step-commit.sh --tag "v0.1.0" "T-147: release"
```

Internally it runs: secrets preflight → `git add -A` → commit → optional tag → `git push origin main` → append the result to `logs/chain.log`. If you are about to run `git commit` by hand, stop and use the script instead — the preflight check is the reason the repository has never leaked a key.

## Commit message format

```
T-042: implement quota ledger

Adds per-key quota windows with daily/hourly/monthly reset handling and
parking of exhausted keys. Verified with QuotaLedgerTest (9 tests) and a
live 429 against a free gateway.
```

Rules:

- Subject: `T-0xx: <task title>` — exactly the task's title, so history maps 1:1 to the plan.
- Body: 1–3 lines — what changed, how it was verified. No "misc fixes", no emoji, no `Co-Authored-By` trailers other than the one the tooling adds.
- One task = one commit. If a task genuinely needs two commits (e.g. mechanical rename then logic), say so in the log and keep both subjects prefixed with the task id.
- Never mix two tasks in one commit. The handover protocol depends on this mapping.

## Branches and tags

- `main` only. The agent does not open pull requests against itself.
- Backup points: `checkpoint/T-0xx` lightweight tags, pushed, created before a risky task.
- Releases: `v0.1.0`, `v0.2.0`, … annotated tags after a delivery task, which triggers the release workflow.

```bash
git tag --list 'checkpoint/*' | tail -5      # find a rollback point
git diff checkpoint/T-042..HEAD --stat       # what changed since
git revert <sha>                             # preferred over reset, keeps history
```

## Push failure

Sync problems are normal on a phone with intermittent connectivity:

1. The commit stays local — never `git reset` it away.
2. Append to `status/ERRORS.md`: task id, error text, whether the commit exists locally.
3. Retry at the next task boundary (`git pull --rebase --autostash && git push`).
4. If a rebase conflict touches a file another workstream is editing, stop the chain and report — do not resolve blindly.
5. `logs/chain.log` records every failed push so the trail survives a reboot.

## Hygiene

- `.gitignore` covers build output, secrets, keystores, `local.properties`, IDE files, model weights, and large log archives.
- `scripts/preflight-secrets.sh` blocks the commit when staged content matches key patterns (`sk-`, `ghp_`, `gho_`, `AIza`, `pplx-`, `Bearer <long>`, `-----BEGIN ... PRIVATE KEY-----`).
- Never commit: `.gguf` model files, APKs, `logs/archive/`, vault exports.
- Large text logs are pruned by `scripts/weekly-cleanup.sh`, not by deleting history.

## What the history must show

`git log --oneline` is the project's audit trail: a reader must be able to see, per task, that it happened, in order, with a verification note. If the history cannot be read that way, the protocol was violated, even if the code works.
