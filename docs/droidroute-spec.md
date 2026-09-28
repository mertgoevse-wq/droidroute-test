# DroidRoute — Projekt-Spezifikation (Spec)

> **Status:** Verbindliche Master-Spec, erstellt aus einem 9-Runden-Interview mit dem Besitzer (Datum: 28.09.2026).
> **Zweck:** Diese Datei ist die **einzige Quelle der Wahrheit**. Aus ihr werden später **135+ englischsprachige .md-Projektdateien** erzeugt (Bauplan + Handbuch + CLAUDE.md + alle übrigen .md), mit denen Claude Code und/oder Freebuff das komplette Projekt **autonom in einem Durchlauf (One-Shot)** bauen. Jeder Task nutzt **mindestens 2 Skills parallel über Subagenten**. Jeder Schritt wird geloggt, protokolliert, committed, gestaged und gepusht, damit **jederzeit abgebrochen und von einem anderen Modell/Programm weitergearbeitet** werden kann.
> **Wichtig:** Diese Spec ist ein Dokument. Es wurden **keine Code-Änderungen** vorgenommen.

---

## 1. Vision in einem Satz

Eine **Android-native App („DroidRoute")** auf dem Galaxy A56 des Besitzers, die wie OmniRoute funktioniert — ein lokaler Server auf localhost, an den sich Coding-Agenten (Claude Code, Freebuff u.a.) per OpenAI-, Anthropic- und Google-kompatiblen Schnittstellen verbinden — aber **native**, mit **allen OmniRoute-Providern plus vielen zusätzlichen** (xKiro, Experiential Labs, FreeLLMAPI, APInex, GoRouter, Bynara, TokenRouter, TokenReply, FastRouter u.v.m.), mit **Abo-Logins** (Google AI Pro, Perplexity Pro), **lokalen Modellen**, **intelligentem Routing mit automatischem Kontingent-Wechsel**, **MCP/Plugin/Connector-Nutzung** und einem **vollautomatisierten, abbruchsicheren Agenten-Bau-System** über ein privates GitHub-Repo.

---

## 2. Wörterbuch (Grundbegriffe — im Interview so vereinbart)

| Begriff | Einfache Erklärung |
|---|---|
| **Provider** | Ein Unternehmen, das KI-Modelle anbietet (z.B. OpenAI, Google, Bynara). |
| **API-Schlüssel (API-Key)** | Ein geheimer Zugangs-Code (Text-Schnipsel), mit dem man einen Provider benutzen darf. |
| **OAuth / Abo-Login** | Anmeldung über einen Knopf („Mit Google anmelden") statt mit einem Schlüssel — für Abo-Konten wie Google AI Pro. |
| **localhost / Port** | Der Server läuft auf dem Handy selbst. „localhost" = „dieses Gerät". Der „Port" ist die Tür-Nummer (z.B. 8787), über die Programme den Server erreichen. |
| **OpenAI-kompatibel / Anthropic-kompatibel** | Zwei Standard-„Sprachen", in denen Programme mit KI-Servern reden. Der Server versteht beide (+ Google-Format). |
| **Routing / Weiterleitung** | Die App entscheidet, welcher Provider eine Anfrage bekommt. |
| **Failover / Weiterschalten** | Wenn ein Provider nicht antwortet oder leer ist, wird automatisch der nächste probiert. |
| **Kontingent (Quota)** | Tages-Limit an Nutzung (Tokens) bei Gratis-Providern. Ist es aufgebraucht → nächster Schlüssel/Provider. |
| **Token** | Die „Zähleinheit" für KI-Nutzung (Text-Brocken). |
| **MCP-Server** | Kleine Helfer-Programme, die Agenten (Claude Code, Freebuff) zusätzliche Fähigkeiten geben (z.B. Dateien lesen, Web suchen). |
| **Plugin / Connector** | Zusatzbausteine, die Agenten oder Apps andocken können. |
| **Subagent** | Ein Neben-Arbeiter: Der Haupt-Agent (Claude Code/Freebuff) lässt mehrere Helfer gleichzeitig an einem Task arbeiten. |
| **Skill** | Eine vorgefertigte Fähigkeits-Anleitung, die ein Agent laden kann (z.B. „Tests schreiben"). |
| **proot-distro / Debian** | Ein Linux-System innerhalb von Termux (Handy), in dem Claude Code und Freebuff laufen. |
| **Termux** | Eine Android-App, die eine Linux-Umgebung auf dem Handy bereitstellt. |
| **Foreground-Service / Anzeige oben** | Ein dauerhaftes Symbol in der Android-Statusleiste, das verhindert, dass Android den Server stoppt. |
| **Keystore** | Androids verschlüsselter Tresor im Handy, für Geheimnisse wie API-Schlüssel. |
| **llama.cpp** | Ein Programm, das KI-Modelle direkt auf dem Handy ohne Internet laufen lässt. |
| **Commit / Push / Stage** | Speichern-Punkt in Git (Commit), Vorbereiten (Stage), Hochladen zu GitHub (Push). |
| **One-Shot** | Ein Durchlauf: Alle Tasks hintereinander automatisch abarbeiten, ohne dass der Besitzer eingreifen muss. |
| **Handover (Übergabe)** | Jederzeit ein anderes Modell/Programm kann an derselben Stelle weiterarbeiten, weil Status-Dateien alles festhalten. |

---

## 3. Umgebung des Besitzers (festgelegte Fakten)

- **Gerät:** Samsung Galaxy A56, 8 GB Arbeitsspeicher, Android.
- **Software-Umgebung:** Termux mit proot-distro **Debian**; darin laufen **Claude Code** und **Freebuff** (Coding-Agenten) bereits produktiv.
- **Bestehende Abos:** Google AI Pro (Gemini), Perplexity Pro; diverse Provider-Konten mit Credits/Guthaben.
- **Git/GitHub:** Ist auf dem Handy bereits eingerichtet (Login vorhanden). Es wird ein **privates Repo namens `droidroute`** verwendet.
- **Projektordner:** Der aktuelle Arbeitsordner heißt derzeit `loki.code` und soll in **`droidroute`** umbenannt werden (Umbenennung bewusst als eigener, letzter Schritt nach der Spec-Erstellung, damit laufende Arbeit nicht abbricht).
- **Der Besitzer will einfache Worte:** Alle interviewbezogenen Dokumente erklären Fachbegriffe (siehe Wörterbuch). Die erzeugten .md-Dateien sind englisch, aber klar und einfach gehalten.

---

## 4. Produkt: DroidRoute (Android-App)

### 4.1 Technische Basis
- **Sprache/Framework:** **Kotlin + Jetpack Compose** (die „echte" Android-Sprache von Google; stabilster Hintergrund-Betrieb, akkuschonendste Lösung).
- **Hintergrund-Betrieb:** **Foreground-Service mit dauerhafter Anzeige in der Statusleiste** („Feste Anzeige oben"). Keine zusätzlichen Pflicht-Einstellungen vom Besitzer (Batterie-Ausnahme ist optional und wird in der App nur als Hinweis angeboten).
- **Mindest-Android:** TBC (Target API der aktuellen Android-Version des A56; in den .md-Tasks festzulegen).

### 4.2 Lokaler Server in der App
- Startet im Hintergrund auf **localhost** mit einem **einstellbaren, festen Port** (Besitzer wählbar in der App; sinnvoller Standard: ein Port ungleich 20128, z.B. 8787, damit kein Konflikt mit parallel laufendem OmniRoute entsteht — Endgültiger Standardwert: TBC in Task-Dateien).
- **Verstandene Protokolle (alle drei von Anfang an):**
  1. **OpenAI-Format** (`/v1/chat/completions`, `/v1/models`, Streaming via SSE)
  2. **Anthropic-Format** (`/v1/messages`, `/v1/models` — zwingend für Claude Code)
  3. **Google-Format** (Gemini `/v1beta`-Stil)
  4. **Medien-Endpunkte von Anfang an:** Bilder (Bilderzeugung/bildverstehende Anfragen) und Sprache (Sprach-Ein-/Ausgabe) — soweit der jeweils angeschlossene Provider das unterstützt; die App übersetzt zwischen den Formaten.
- **Modell-Liste:** Der Server bietet eine kombinierte `/v1/models`-Liste aller aktiven Provider an.

### 4.3 Zugangsschutz (Auth) — „Alles einstellbar"
- Pro Konfigurationsfall wählbar: **No Auth** (ohne Schlüssel, nur gerätelokal), **API-Key** (in der App erzeugbare Schlüssel), **OAuth-Login**.
- „npauth" aus der ursprünglichen Anfrage wurde als **Tippfehler für „no auth"** geklärt.
- **Erreichbarkeit (dreistufig):**
  1. **Nur das Handy** (Standard; Termux/Debian erreichen localhost immer).
  2. **Zusätzlich WLAN-Schalter:** Geräte im Heim-WLAN dürfen zugreifen (nur mit API-Key).
  3. **Zusätzlich Zugriff von außen** über einen Tunnel (z.B. Cloudflare Tunnel / Tailscale oder vergleichbar — konkrete Wahl in den Task-Dateien) mit Schlüsselzwang.

### 4.4 Provider-Unterstützung
- **Basis:** **Alle Provider, die OmniRoute unterstützt** (OmniRoute listet 350+; siehe OmniRoute-Repository als Referenz — die .md-Tasks enthalten die Übernahme/Neuimplementierung dieser Provider-Adapter, **keine direkte Portierung** des OmniRoute-Codes).
- **Zusätzlich mindestens namentlich genannt:** xKiro, Experiential Labs, FreeLLMAPI, APInex, GoRouter, **Bynara (NaraRouter) mit Vorrang**, TokenRouter, TokenReply, FastRouter — **und „viele weitere mehr"**: Die Provider-Liste ist als **erweiterbares Verzeichnis (Registry)** gebaut, damit neue Provider ohne Umbau des Kerns hinzugefügt werden können.
- **Eigene Provider hinzufügen:** Formular in der App (Name, Basis-URL, API-Schlüssel, Typ: OpenAI- oder Anthropic-kompatibel). Die App **fragt automatisch die Modell-Liste des Providers ab** (Standard `/v1/models`); Falls kein Standard vorhanden: Hand-Eingabe der Modellliste möglich.
- **Gratis-Provider mit One-Click:** Für kostenlose Provider gibt es einen **„Verbinden"-Knopf** (direktes Verbinden ohne umfangreiche Einrichtung), inklusive Anleitung/Hinweis, wo der Schlüssel geholt wird.
- **Abo-Konten des Besitzers:**
  - **Google AI Pro:** Abo-Login (OAuth-Knopf „Mit Google anmelden"), nutzt Gemini-Modelle des Abos.
  - **Perplexity Pro:** Abo-Login, speziell als **Pro-Suche (Sonar-Modelle)** nutzbar — nicht nur als normaler Chat, sondern als Such-Werkzeug.
  - **GitHub (Copilot) und HuggingFace:** OAuth-Logins ebenfalls vorgesehen.
  - Umsetzungsreihenfolge: Zuerst alles, was mit normalen API-Schlüsseln geht; OAuth-Logins als eigener Baustein direkt danach (beides ist beauftragt).
- **API-Schlüssel-Behandlung:** Schlüssel werden **lokal verschlüsselt** (Android Keystore) gespeichert, **nur einmal im Klartext angezeigt**, danach **dauerhaft maskiert: die ersten 5 und die letzten 5 Zeichen sichtbar** (Rest `••••`).

### 4.5 Routing & Failover (Herzstück)
- **Automatisches Weiterschalten (Failover):** Antwortet ein Provider nicht (Timeout/Fehler) oder ist das Guthaben/Kontingent aufgebraucht → automatisch der nächste in der Reihenfolge, bis einer Erfolg hat.
- **Mehrere Schlüssel pro Provider/Modell:** Der Besitzer kann **pro Provider oder pro Modell mehrere API-Keys hinterlegen — auch von mehreren verschiedenen Providern**. Ist ein Kontingent aufgebraucht, wird **automatisch der nächste Schlüssel** geschaltet (Key-Rotation mit Kontingent-Erkennung).
- **Routing-Methoden (alle auswählbar):**
  - **Gratis zuerst** (Abos/Gratis-Konten vor Guthaben vor bezahlt),
  - **Schnellster zuerst** (die App merkt sich Antwortzeiten),
  - **Eigene Reihenfolge** pro Modell/Modell-Gruppe,
  - **Intelligentes Auto-Routing**, u.a. „automatisch beste kostenlose Modelle",
  - **alles, was OmniRoute mindestens kann, plus mehr** (OmniRoute-Parität als Untergrenze).
- **Neue eigene Routing-Ideen (über OmniRoute hinaus, beauftragt):**
  - **Kontingent-Bewusstsein:** Die App kennt Tages-Limits (z.B. Bynara ~7 Mio. Token/Tag) und plant vorausschauend (wieviele Tokens bleiben heute?).
  - **Gesundheits-Score pro Provider** (Fehlerrate, Tempo, Verfügbarkeit der letzten Anfragen) fließt in die Auswahl ein.
  - **Kosten-Bewusstsein:** Rechenschaft pro Anfrage (welcher Provider, wieviel Token, was hat es „gekostet" — bei Gratis: 0) und Ausweichen auf günstigere Optionen bei gleicher Qualität.
  - **Modell-Gruppen/kanonische Namen:** Der Besitzer kann logische Namen (z.B. „mein-bestes-modell") definieren, hinter denen mehrere echte Provider-Modelle mit Prioritäten stehen.

### 4.6 Dashboard & Verbrauch
- **Armaturenbrett:** Verbundene Provider, verbrauchte Tokens **pro Provider**, Fehler, **Tempo (Latenz)** der letzten Anfragen.
- **Zusätzlich:** **Tages- und Wochenverbrauch** pro Provider als Übersicht.
- Live-Status des Servers (an/aus, Port, Erreichbarkeit, welche Agenten gerade verbunden sind).

### 4.7 Lokale Modelle (auf dem Handy)
- **Beide Wege beauftragt, Reihenfolge: zuerst Termux, eingebaut danach:**
  1. **Über Termux:** Die App startet/steuert llama.cpp im Termux (kleine Modelle, z.B. 1–4 GB, laufen direkt auf dem A56; deutlich langsamer als Internet, aber ohne Netz nutzbar).
  2. **In der App eingebaut:** llama.cpp-Technik eingebacken (ON-Device ohne Termux) als spätere Verbesserung.
- **Größen-Limit:** **Kein hartes Limit + Warnung.** Der Besitzer entscheidet pro Modell selbst; die App zeigt immer eine Warnung und den Speicherverbrauch an (Risiko: Android wird langsam oder stoppt die App).
- **Sondermodelle:** Zusätzlich Spezialbehandlung für Einbettungs-Modelle (für Suche), Sprach-Modelle (Ein-/Ausgabe) und Bild-Modelle.

### 4.8 Termux-Anbindung
- **Beides:**
  1. **Offizieller Android-Weg:** App darf Termux-Funktionen offiziell aufrufen (Termux:API / RUN_COMMAND- Berechtigung) — llama.cpp starten/stoppen aus der App.
  2. **Nur übers Netz (HTTP auf localhost)** als Rückfallebene; Termux-Skripte machen den Rest.

### 4.9 MCP-Server, Plugins, Connectoren (wichtig!)
- **Alle verbundenen MCP-Server, Plugins und Connectoren sollen genutzt werden.**
- **Beide Quellen:**
  1. **Automatisch aus Termux/Debian:** Die App liest die Konfigurationen von Claude Code & Freebuff im Termux/Debian-System und übernimmt deren MCP-Server/Plugins automatisch.
  2. **Eigene Liste in der App:** Zusätzliche manuelle Einträge möglich (Name, Server-Adresse, Werkzeuge).
- Die App stellt Agenten die MCP-Infos bereit bzw. agiert selbst als MCP-kompatibler Bestandteil des Ökosystems (konkrete Schnittstelle in den Task-Dateien festzulegen: TBC).

### 4.10 App-Sprache
- **Deutsch + Englisch:** Deutsch als Voreinstellung, automatisch auf Englisch umschaltbar (folgt Android-Sprache).

---

## 5. Das Agenten-Bau-System (135+ .md-Dateien)

### 5.1 Was die Dateien sind (Korrektur des Besitzers — verbindlich)
- **Nicht** ein lose Dokumentenset, sondern **die Projektdateien selbst**: **135+ .md-Dateien**, die **Claude Code bzw. Freebuff benötigen, um in einem Durchgang (One-Shot) das fertige Produkt in der Hand zu halten**.
- DroidRoute ist **keine direkte Portierung von OmniRoute**, hat aber **alle Funktionen von OmniRoute inkl. aller und mehr Provider**.
- Enthalten sind mindestens:
  - die **Bauplan-/Task-Dateien** (jede = abgeschlossener, prüfbarer Arbeitsschritt),
  - eine **CLAUDE.md** (Einstiegs- und Verhaltensdatei für Claude Code),
  - **alle weiteren .md-Dateien, die man braucht**, um das Produkt komplett zu bauen (Agenten-Handbuch, Regeln, Abläufe, Beispiele, Prüf-Listen).
- Die Dateien werden **aus dieser Spec generiert** (durch Claude Code oder Freebuff), aufgeteilt in Tasks/Aufgaben.

### 5.2 Task-Regeln (verbindlich)
- **Ablaufart:** Task-Liste, **nacheinander** abarbeiten; Startbefehl beginnt bei Task 1 und arbeitet alle hintereinander ab (nach jedem Task: speichern, pushen, weiter).
- **Skills:** **Mindestens 2 Skills pro Task, parallel** — gemeint ist: **die bauenden Agenten (Freebuff/Claude Code) sollen beim Bauen mehrere Subagenten mit mehreren Skills gleichzeitig nutzen** (z.B. einer schreibt Code, einer schreibt Tests, einer dokumentiert). Nicht DroidRoute selbst ist das Multi-Skill-System, sondern der Bau-Prozess.
- **Skill-Auswahl:** **Vorschlag + Freiheit** — jede Task-Datei schlägt 2–3 konkrete Skills vor; der Agent darf abweichen, wenn es sinnvoller ist. Pflicht bleibt: **mindestens 2 Skills parallel (Subagenten)**.
- **Task-Größe:** **Gemischt** — kleine Schritte (ca. 15–30 Min Agentenarbeit) für kritische Teile, ganze Bauteile für einfache Teile. Spec/Task-Dateien definieren es pro Bauteil.
- **Jede Task-Datei enthält (Mindeststruktur):** Ziel, Vorbedingungen, Schritte, Prüf-Liste (Abnahme-Kriterien), Log-Vorgaben, Commit-/Push-Anweisung, Abbruch-/Wiedereinstiegs-Punkt, Skills-Vorschlag (≥2), Abhängigkeiten zu anderen Tasks.

### 5.3 Sprache der Dateien
- **Englisch** (maximale Verständlichkeit für alle Agenten: Claude Code, Freebuff, andere Modelle).
- (Für den Besitzer erklärt: Fachbegriffe werden in den Dateien beim ersten Auftreten kurz erklärt — gleicher Stil wie das Wörterbuch hier.)

### 5.4 Abbruchsicherheit & Handover (jederzeit weiterarbeiten können)
- **Status-Dateien im Repo — maximale Ausführung:**
  - `PROGRESS.md` — was ist fertig?
  - `NEXT.md` — was kommt als Nächstes?
  - `DECISIONS.md` — welche Entscheidungen wurden getroffen und warum?
  - `ERRORS.md` — was ist schiefgelaufen?
  - **Plus: eine Status-Datei pro großem Bauteil** mit eigenem Stand.
  - **Plus: tägliche Zusammenfassung** (daily summary).
- **Protokollierung — alles:** Jeder Befehl, jede Datei-Änderung und jede Modell-Antwort landen mit Datum/Uhrzeit in Log-Dateien.
- **Logs nach GitHub:** Ja, Logs kommen ins Repo, aber ein **automatischer wöchentlicher Aufräum-Schritt** löscht alte Log-Dateien, damit das Repo nicht anschwillt.
- **Git-Ablauf — immer automatisch:** Nach **jedem** fertigen Schritt: automatisch **stage + commit + push** zum privaten Repo. Kein Nachfragen. **Plus Backup-Punkt vor jedem Schritt**, damit man jederzeit zu einem früheren Stand zurück kann.
- Ziel: Jederzeit abbrechbar; im schlimmsten Fall kann **ein anderes Modell oder Programm** an derselben Stelle weiterarbeiten.

---

## 6. GitHub-Repo

- **Privates Repo, Name: `droidroute`** (unter dem GitHub-Konto des Besitzers).
- GitHub ist auf dem Handy bereits eingerichtet (Login vorhanden).
- **Geheimnis-Regel (verbindlich): Niemals Schlüssel ins Repo.** Echte Provider-Schlüssel bleiben nur verschlüsselt auf dem Handy (Keystore). Im Repo gibt es nur **Muster-Dateien ohne echte Schlüssel** (Beispiel-Konfigurationen mit Platzhaltern).
- **APK-Bau — beides:**
  1. **GitHub baut automatisch:** Bei jedem Hochladen baut GitHub (GitHub Actions, kostenlos) die APK; Besitzer lädt sie von der GitHub-Seite herunter und installiert sie.
  2. **Auf dem Handy bauen:** Lokaler Bau in Termux als **Notfall-Fallback** (ohne Internet; dauert ca. 10–30 Min, viel Akku).
- **Ordner-Umbenennung:** Der aktuelle Projektordner `loki.code` wird in `droidroute` umbenannt (eigener, letzter Schritt nach der Spec — erledigt die Arbeitssitzung, die die Spec erstellt hat, direkt im Anschluss; bewusst zuletzt, um laufende Prozesse nicht zu unterbrechen).

---

## 7. Anforderungen-Liste (kompakt, nummeriert)

1. Android-native App **DroidRoute** in **Kotlin + Compose**.
2. Lokaler Server im Hintergrund (Foreground-Service + Statusleisten-Anzeige), **einstellbarer fester Port**.
3. Versteht **OpenAI-, Anthropic- und Google(Gemini)-Format + Medien-Endpunkte** von Anfang an.
4. Zugangsschutz einstellbar: **No Auth / API-Key / OAuth**; Erreichbarkeit: Handy + WLAN-Schalter + von außen (Tunnel).
5. **Alle OmniRoute-Provider** + **xKiro, Experiential Labs, FreeLLMAPI, APInex, GoRouter, Bynara (Vorrang), TokenRouter, TokenReply, FastRouter** + erweiterbare Registry + „viele weitere".
6. **Eigene Provider** per Formular (OpenAI-/Anthropic-kompatibel) mit **automatischer Modell-Listen-Abfrage**.
7. **One-Click-Verbinden** für Gratis-Provider.
8. **Abo-Logins:** Google AI Pro (Gemini), Perplexity Pro (als **Sonar-Suche**), GitHub (Copilot), HuggingFace.
9. Schlüssel: **verschlüsselt (Keystore)**, einmalige Klartext-Anzeige, dauerhafte **Maskierung (erste 5 + letzte 5 Zeichen)**.
10. **Failover automatisch**; **mehrere Keys pro Provider/Modell** mit **automatischem Kontingent-Wechsel**.
11. **Routing-Methoden:** Gratis zuerst / Schnellster zuerst / eigene Reihenfolge / intelligentes Auto-Routing (beste kostenlose Modelle) / OmniRoute-Parität + mehr (Gesundheits-Score, Kontingent-Bewusstsein, Kosten-Bewusstsein, Modell-Gruppen).
12. **Dashboard + Tages-/Wochenverbrauch** pro Provider, Fehler, Latenzen.
13. **Lokale Modelle:** llama.cpp über **Termux zuerst**, eingebaut danach; **kein Größen-Limit + Warnung**; Sondermodelle (Einbettungen, Sprache, Bilder).
14. **Termux-Anbindung:** offizieller Weg + HTTP-Fallback.
15. **Alle verbundenen MCP-Server, Plugins, Connectoren nutzen**; automatisch aus Termux/Debian gelesen **+** eigene Liste.
16. App-Sprache **Deutsch + Englisch**.
17. **135+ .md-Projektdateien** (Bauplan + Handbuch + CLAUDE.md + alles für den kompletten Durchlauf), **englisch**, aus dieser Spec generierbar.
18. Tasks **nacheinander als Liste**, One-Shot-Abarbeitung; **min. 2 Skills parallel via Subagenten pro Task** (Vorschlag + Freiheit).
19. **Jeder Schritt geloggt/protokolliert; automatisch stage + commit + push; Backup-Punkt vor jedem Schritt.**
20. **Maximale Status-Dateien** (PROGRESS/NEXT/DECISIONS/ERRORS + pro Bauteil + Tageszusammenfassung) für **Handover an jedes andere Modell/Programm**.
21. **Privates Repo `droidroute`**; **niemals Schlüssel ins Repo**; Logs ins Repo mit **wöchentlichem Aufräumen**.
22. **APK-Bau:** GitHub Actions automatisch + Termux-Fallback.
23. Ordner **`loki.code` → `droidroute`** umbenennen (letzter Schritt).

---

## 8. Abnahmekriterien (wann ist DroidRoute „fertig" im Sinne der Spec?)

1. App läuft auf dem Galaxy A56; Server startet im Hintergrund mit dauerhafter Anzeige; Port ist einstellbar.
2. Claude Code im Termux-Debian verbindet sich **ohne weiteres Zutun über localhost** (Anthropic-Format) und arbeitet produktiv; Freebuff ebenso (OpenAI-Format).
3. Mindestens: alle OmniRoute-Provider-Kategorien + die 9 namentlich genannten Zusatz-Provider sind angebbar; eigene Provider per Formular; mind. ein Gratis-Provider per One-Click.
4. Google AI Pro (OAuth) und Perplexity Pro (Sonar) sind verbunden; Perplexity liefert Such-Antworten.
5. Failover + Key-Rotation nachweisbar (Test: künstlicher Fehler → automatisch nächster Key/Provider).
6. Dashboard zeigt Token/Provider, Tages-/Wochenverbrauch, Fehler, Latenzen.
7. Ein lokales Modell läuft über Termux, von der App steuerbar; Warnung bei großen Modellen erscheint.
8. MCP-Server aus Termux/Debian werden automatisch erkannt und angezeigt; eigene Einträge sind möglich; alle verbundenen werden genutzt.
9. Repo `droidroute` ist privat; ein automatisierter Lauf hat ≥135 .md-Dateien erzeugt und das Projekt daraus gebaut; jeder Schritt ist commit+push; Status-Dateien sind aktuell; Log-Aufräumarbeit läuft wöchentlich.
10. Ein „Fremd-Agent" (anderes Modell/Programm) kann allein anhand der Repo-Dateien (Status + Spec + Tasks) weiterarbeiten.
11. APK wird von GitHub Actions gebaut und ist installierbar; Termux-Fallback-Bau dokumentiert und getestet.
12. Ordner heißt `droidroute`.

---

## 9. Bewusste Abgrenzungen (Nicht-Ziele)

- **Keine direkte Portierung** des OmniRoute-Codes — Funktions-Parität als Untergrenze, eigenes natives Design.
- Kein Multi-Tenant-Betrieb (nur der Besitzer nutzt die App; keine fremden Nutzer).
- Kein App-Store-Release (Seitensprung/„sideload" über APK reicht; TBC ob später Play Store).
- Keine Schlüssel-Speicherung im Klartext im Repo (nie).
- Kein Zwang zu Batterie-Ausnahme-Einstellungen (nur Hinweis).

---

## 10. Offene Punkte (TBC — in den Task-Dateien festzulegen)

1. **Standard-Port** (Vorschlag: 8787 statt 20128; Besitzer kann ihn ändern).
2. **Tunnel-Dienst** für „von außen" (Cloudflare Tunnel vs. Tailscale vs. alternatives Verfahren).
3. **Exakte Mindest-Android-Version / Target-API** für den Galaxy A56.
4. **MCP-Anbindung im Detail:** Wie genau DroidRoute selbst als MCP-Client agiert und wie die App die erkannten Server an Claude Code/Freebuff zurückspielt.
5. **Perplexity-Sonar-Anbindung im Detail** (Abo-Login-Verfahren, Endpunkte).
6. **llama.cpp-Binaries** für aarch64-Android (Termux-Paket vs. eigenes Build).
7. **Umfang der Provider-Registry in Version 1** (welche der 350+ OmniRoute-Provider zuerst; Priorisierung über Gratis-Provider empfohlen).

---

## 11. Historie der Interview-Runden (Nachweis)

- **R1:** Technik (Kotlin+Compose), Hintergrund (Anzeige oben), Port (fest, einstellbar), Zugang (alles einstellbar).
- **R2:** Abo-Zugänge (OAuth + API-Schlüssel gestuft, Perplexity als Suche), Failover (automatisch), Schlüssel-Speicher (verschlüsselt/Keystore), lokale Modelle (llama.cpp + Sondermodelle).
- **R3:** 135+ Dateien (Bauplan + Handbuch), Tasks (Liste nacheinander), Git (immer automatisch commit+push), GitHub (eingerichtet).
- **R4:** Status-Dateien (maximal), Protokoll (alles), Datei-Sprache (Englisch), MCP-Quelle (beides).
- **R5:** Name (DroidRoute), „npauth" = no auth (Tippfehler), eigene Provider (Formular + Auto-Liste), Übersicht (Dashboard + Verbrauch).
- **R6:** Klärung Multi-Skills (bauende Agenten nutzen Subagenten mit ≥2 Skills parallel), Routing (alle OmniRoute-Methoden + eigene Ideen, Multi-Key-Kontingent-Wechsel), Erreichbarkeit (Handy + WLAN + außen), Repo (niemals Schlüssel).
- **R7:** Lokale Modelle (beides, Termux zuerst), APK-Bau (beides), Logs (ins Repo + wöchentliches Aufräumen), App-Sprache (de+en).
- **R8:** Korrektur: 135+ Dateien = Projekt-Dateien für den One-Shot-Bau (keine Dokumentation darüber hinaus nötig, aber CLAUDE.md + alle benötigten .md inklusive); Modell-Größe (kein Limit + Warnung); Termux-Link (beides); OAuth zuerst (Google, GitHub, HuggingFace + alle OmniRoute-fähigen + xKiro, FreeLLMAPI, APInex, Bynara v.a., TokenRouter, TokenReply, GoRouter, FastRouter + Gratis-Provider mit One-Click; Schlüssel-Maskierung 5/5).
- **R9:** Repo-Name (`droidroute`), Protokolle (alle drei + Medien von Anfang an), Task-Größe (gemischt), Skills (Vorschlag + Freiheit; zusätzlich CLAUDE.md und alle .md für einen kompletten Durchlauf).

---

*Ende der Spec. Aus dieser Datei werden die 135+ englischsprachigen .md-Projektdateien generiert. Es wurden keine Code-Änderungen vorgenommen.*
