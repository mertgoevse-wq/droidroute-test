# Glossar (einfach erklärt)

Für den Besitzer — alle Fachwörter, die im Projekt vorkommen, in einfachen Worten. (English docs stay in English; this page explains them.)

| Wort | Einfache Erklärung |
|---|---|
| **Provider** | Ein Anbieter von KI-Modellen (z.B. OpenAI, Google, Bynara). |
| **Adapter** | Ein Übersetzer-Baustein: Er bringt einem Anbieter die Sprache der App bei. |
| **Manifest** | Eine kleine Textdatei (JSON), die beschreibt, wie ein Anbieter aussieht: Adresse, Login-Art, Modelle. |
| **API-Schlüssel (Key)** | Geheimer Zugangscode zu einem Anbieter. |
| **OAuth / Abo-Login** | Anmeldung per Knopf („Mit Google anmelden") statt mit Code — für Abo-Konten wie Google AI Pro. |
| **localhost / 127.0.0.1** | „Dieses Gerät". Der Server läuft auf dem Handy selbst. |
| **Port (z.B. 8787)** | Die Tür-Nummer, über die Programme den Server erreichen. |
| **Endpunkt (Endpoint)** | Eine einzelne Adresse, die der Server anbietet, z.B. `/v1/messages`. |
| **OpenAI-kompatibel** | Der Server versteht das Anfrage-Format, das OpenAI benutzt. |
| **Anthropic-kompatibel** | Der Server versteht das Anfrage-Format von Anthropic (nötig für Claude Code). |
| **Gemini-Format** | Das Anfrage-Format von Google. |
| **SSE / Streaming** | Die Antwort wird in kleinen Stücken geliefert, statt am Ende auf einmal — so fühlt sich KI „live" an. |
| **Router / Routing** | Die Entscheidung, welcher Anbieter eine Anfrage bekommt. |
| **Kandidat** | Ein möglicher Anbieter+Schlüssel+Modell, aus dem der Router wählt. |
| **Failover / Weiterschalten** | Fällt ein Anbieter aus, kommt automatisch der nächste. |
| **Kontingent (Quota)** | Tages- oder Stunden-Limit bei Gratis-Anbietern. |
| **Key-Rotation** | Mehrere Schlüssel pro Anbieter; ist einer leer, greift der nächste. |
| **Health-Score** | Eine Note (0–1) pro Anbieter-Schlüssel: wie zuverlässig und schnell er ist. |
| **Circuit Breaker** | Eine „Sicherung": Ein Anbieter, der dauerhaft Fehler wirft, wird kurz ausgeschaltet. |
| **Hedging** | Vorsichtshalber zwei Anbieter gleichzeitig fragen (kostet doppelt — nur optional). |
| **Alias** | Ein selbst gewählter Name (z.B. „mein-bestes-modell"), hinter dem mehrere echte Modelle stehen. |
| **Vault / Keystore** | Der verschlüsselte Tresor des Handys für Geheimnisse. |
| **Maskierung (5/5)** | Schlüssel wird angezeigt als `sk-ab••••••••yz-12` — nur Anfang und Ende sichtbar. |
| **Redaction** | Automatisches Unkenntlichmachen von Geheimnissen in Logs und Antworten. |
| **Foreground-Service** | Hintergrunddienst mit dauerhafter Anzeige in der Statusleiste; Android darf ihn nicht einfach stoppen. |
| **Bind-Modus** | An welche Netzwerkadresse der Server hört: nur Handy, WLAN, oder von außen. |
| **Tunnel** | Ein sicherer Weg von außen ins Handy hinein (z.B. Tailscale oder Cloudflare Tunnel). |
| **MCP-Server** | Helfer-Programm, das Agenten Extra-Fähigkeiten gibt (Dateien, Suche, Datenbanken). |
| **Bridge** | Eine Brücke: Die App reicht MCP-Anfragen der Agenten an die Helfer-Programme weiter. |
| **Plugin / Connector** | Zusatzbausteine, die angedockt werden können. |
| **Skill** | Eine Fähigkeits-Anleitung für einen Agenten (z.B. „Tests schreiben"). |
| **Subagent** | Ein Neben-Arbeiter; der Haupt-Agent lässt mehrere gleichzeitig arbeiten. |
| **Task** | Eine einzelne Aufgabe; hier genau eine `.md`-Datei in `plan/`. |
| **Phases (Phasen)** | Gruppen von Tasks (z.B. Phase 1 = Kernserver). |
| **One-Shot** | Ein Durchlauf: alle Tasks automatisch nacheinander, ohne Eingreifen. |
| **Commit / Stage / Push** | Speicherpunkt (commit), vorbereiten (stage), zu GitHub hochladen (push). |
| **Checkpoint-Tag** | Ein Lesezeichen im Verlauf, zu dem man zurückgehen kann. |
| **Handover / Resume** | Übergabe: Ein anderes Modell kann an derselben Stelle weitermachen. |
| **Status-Dateien** | Textdateien (`status/`), die jederzeit sagen: was fertig ist, was als Nächstes kommt, warum was entschieden wurde, was kaputt ist. |
| **Log** | Protokolldatei: wann wurde was getan, mit welchem Ergebnis. |
| **llama.cpp** | Programm, das KI-Modelle direkt auf dem Handy ohne Internet laufen lässt. |
| **GGUF / Quant** | Modell-Dateiformat / „verkleinerte" Version eines Modells (Q4, Q5 …). |
| **KV-Cache** | Zwischenspeicher beim lokalen Modell — verbraucht RAM, wächst mit dem Kontext. |
| **APK** | Die installierbare App-Datei für Android. |
| **CI / GitHub Actions** | Automatischer Bau-Service von GitHub: baut die APK bei jedem Hochladen. |
| **Room / DataStore** | Zwei Android-Speichertechniken: Datenbank (Room) und Einstellungen (DataStore). |
| **Ktor** | Kotlin-Bibliothek für den eingebauten Webserver. |
| **Compose / Material 3** | Googles moderne Bauweise für Android-Oberflächen. |
| **TBC** | „To be confirmed" — noch offener Punkt. Alle 7 sind in `docs/11-tbc-resolutions.md` entschieden. |
| **Anti-Slop** | Regeln gegen KI-Füllstoff: keine Platzhalter, keine erfundenen Adressen, keine unnötigen Änderungen. |
| **Skill-Bibliothek** | Eine Sammlung fertiger Fähigkeits-Anleitungen (Skills), die ein Agent laden kann. |
| **Projekt-Skill** | Ein Skill, der nur für dieses Projekt gilt (`.claude/skills/`) und die Projektregeln enthält. Gewinnt gegen globale Skills. |
| **Plugin-Marktplatz** | Eine Quelle, aus der Plugins installiert werden (z.B. das offizielle Anthropic-Repository). |
| **Inventar (TOOLING.md)** | Automatisch erzeugte Liste: welche Skills, Plugins, MCP-Server und Befehle gerade da sind. |
| **Combo** | Eine Kette von Modellen: Läuft eins aus oder fällt aus, geht es automatisch zum nächsten. |
| **Virtuelles Modell (auto)** | Ein Name wie `auto/fast`, hinter dem kein echtes Modell steht, sondern eine Auswahlregel. |
| **Fusion** | Mehrere Modelle antworten, ein Richter-Modell fasst zusammen. Teurer, oft besser. |
| **Pipeline** | Die Ausgabe von Schritt 1 geht als Eingabe in Schritt 2 (und so weiter). |
| **Token-Kompression** | Lange Eingaben werden gekürzt (verlustfrei wo möglich), damit weniger Tokens bezahlt werden. |
| **Cache-Treffer** | Der Anbieter erkennt eine schon bekannte Eingabe und rechnet sie günstiger ab. |
| **Kosten-Telemetrie** | Zahlen zu Verbrauch und Kosten, sichtbar als Kopfzeilen (`X-DroidRoute-*`) und im Armaturenbrett. |
| **Quota-Share** | Ein gemeinsames Konto wird gerecht über mehrere Schlüssel aufgeteilt; ungenutztes Kontingent wird verliehen. |
| **Gedächtnis (Memory)** | Optionale Erinnerung an Fakten und Entscheidungen. Standard: ausgeschaltet. |
| **A2A** | Agent-zu-Agent: Ein anderer Agent darf Aufgaben an DroidRoute übergeben. |
| **Agent-Card** | Die „Visitenkarte", die sagt, was DroidRoute auf Anfrage wirklich kann. |
| **OCR** | Texterkennung aus Bildern und Dokumenten. |
| **Modality-Bridge** | Die Brücke, die Bild-, Ton- und Video-Anfragen an ein passendes Modell weiterleitet. |
| **Prompt-Injection** | Ein Angriff, bei dem fremder Text dem Modell heimlich Befehle gibt. |
| **Guardrail** | Schutzregel, z.B. gegen Prompt-Injection oder dafür, dass Geheimnisse nicht nach außen gelangen. |
| **Parität** | Gleichstand bei den Funktionen — hier: DroidRoute kann alles, was OmniRoute kann. |
