<div align="center">

# DroidRoute — Start

**Codewort:** `Anlauf-8787`

Gib dieses Wort einem Coding-Agenten (Claude Code oder Freebuff) in diesem Ordner.
Er liest dann alle Projektdateien und baut DroidRoute autonom, Task für Task.

</div>

---

## Was du tust

Öffne ein Terminal in diesem Ordner und starte Claude Code:

```bash
cd ~/loki.route        # nach dem Umbenennen: ~/droidroute
claude
```

Dann tippe in Claude Code genau das:

```text
Anlauf-8787
```

Mehr ist nicht nötig. Alles Weitere steht in den Dateien, die der Agent jetzt liest.

## Was der Agent dann tut

1. Er liest [`AGENTS.md`](AGENTS.md) — die verbindlichen Regeln — und [`CLAUDE.md`](CLAUDE.md).
2. Er liest den Zustand: `status/HANDOVER.md`, `status/PROGRESS.md`, `status/NEXT.md`, `status/DECISIONS.md`, `status/ERRORS.md`, `status/TOOLING.md`.
3. Er liest [`plan/INDEX.md`](plan/INDEX.md) — **190 Tasks in 15 Phasen** — und beginnt bei [`T-001`](plan/phase-00-foundation/T-001-repository-hygiene.md).
4. Pro Task: zwei Skills **gleichzeitig** über Subagenten (einer davon prüft), jeder Schritt wird geloggt, am Ende **ein Commit und ein Push**.
5. Er arbeitet weiter, bis alle Tasks fertig sind — ohne Rückfrage, außer ein Stop-Grund aus `AGENTS.md` §9 greift.

Ergebnis: eine installierbare Android-App, ein privates GitHub-Repo, vollständiger Verlauf, und die Möglichkeit, jederzeit mit einem anderen Modell weiterzumachen.

## Was du erwarten kannst

| | |
|---|---|
| Sichtbarer Fortschritt | `status/PROGRESS.md` (Zähler) und `logs/tasks/T-0xx.log` (jeder Schritt) |
| Jeder Task ein Commit | `git log --oneline` |
| Unterbrochen? | Neuer Agent, gleiches Codewort — er macht dort weiter, wo es aufhörte |
| Nichts geht verloren | Alles ist committet und gepusht, bevor der nächste Task beginnt |

## Die Regeln, die der Agent nicht brechen darf

- **Kein Geheimnis ins Repository.** `scripts/preflight-secrets.sh` läuft vor jedem Commit.
- **Keine erfundenen URLs, Modellnamen oder Felder.** Wenn die Doku eines Anbieters nicht erreichbar ist, wird das protokolliert und gestoppt.
- **Keine Platzhalter.** Kein „machen wir später", kein Fake-Rückgabewert.
- **Nichts außerhalb des Tasks anfassen.** Keine Schönheitsreparaturen nebenbei.
- **Keine Prüfung abschwächen**, um einen Commit durchzubekommen.
- **Kein AI-Slop im Aussehen.** Verbindlich: [`docs/14-design-system.md`](docs/14-design-system.md), geprüft von `tools/check_design_slop.py`.

## Wenn du nachsehen willst, ob es gesund läuft

```bash
python3 tools/check_plan_consistency.py   # Plan und Dokumente stimmen überein
python3 tools/generate_plan.py --check    # die 190 Task-Dateien passen zu den Daten
python3 tools/check_links.py              # alle Querverweise stimmen
python3 tools/check_skills.py             # jede Skill-Angabe zeigt auf etwas Installiertes
python3 tools/check_design_slop.py        # kein verbotenes Design
scripts/preflight-secrets.sh              # keine Schlüssel im Repository
gh run list --limit 5                     # läuft die Automatik auf GitHub sauber?
```

## Wenn du stoppen willst

`Ctrl+C` in Claude Code. Nichts geht verloren, weil jeder abgeschlossene Task bereits committet und gepusht ist.
Starte später einfach neu und gib wieder das Codewort — der Agent liest `status/NEXT.md` und macht weiter.

## Wenn ein Task hängen bleibt

Der Agent schreibt den Grund nach `status/ERRORS.md` und stoppt. Öffne die Datei, lies den Eintrag, und entscheide: Umgebung reparieren, Task präzisieren, oder einen anderen Task vorziehen. Danach wieder das Codewort.

---

<div align="center">

*Kein Chat-Verlauf nötig. Alles Wissen liegt im Repository.*

</div>
