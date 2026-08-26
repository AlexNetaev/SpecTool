# 🛠️ spec-tool

**Parser, Validator und View-Generator für strukturierte Spezifikationsdokumente.**

`spec-tool` ist ein Python-basiertes CLI-Tool zum Einlesen, Validieren und Verwalten von Markdown-Spezifikationsdokumenten im **SPEC_FORMAT v1.0.0**. Es wurde entwickelt, um komplexe Dokument-Ökosysteme (wie das MYRMEX-Projekt mit 12+ vernetzten Spezifikationsdateien) maschinenlesbar, konsistent und nachvollziehbar zu machen.

---

## 📑 Inhaltsverzeichnis

- [Übersicht](#-übersicht)
- [Architektur](#-architektur)
- [Installation](#-installation)
- [Schnellstart](#-schnellstart)
- [CLI-Befehle](#-cli-befehle)
- [Das SPEC_FORMAT](#-das-spec_format)
- [Modul-Referenz](#-modul-referenz)
  - [Frontmatter-Parser](#1-frontmatter-parser)
  - [Marker-Parser](#2-marker-parser)
  - [MD-Hauptparser](#3-md-hauptparser)
  - [Referenzgraph](#4-referenzgraph)
  - [Konsistenz-Validator](#5-konsistenz-validator)
  - [View-Generator](#6-view-generator)
- [Datenmodell](#-datenmodell)
- [Testsuite](#-testsuite)
- [Projektstruktur](#-projektstruktur)
- [Konfigurationsmöglichkeiten](#-konfigurationsmöglichkeiten)
- [Fehlerbehandlung](#-fehlerbehandlung)
- [FAQ](#-faq)
- [Lizenz](#-lizenz)

---

## 🎯 Übersicht

### Was macht spec-tool?

| Funktion | Beschreibung |
|----------|-------------|
| **Parsen** | Liest Markdown-Dateien mit SPEC_FORMAT-Markern und erzeugt strukturierte Datenobjekte |
| **Validieren** | Prüft Konsistenz, Referenzen und Formatregeln |
| **Verknüpfen** | Baut einen Referenzgraphen über alle Dokumente |
| **Impact-Analyse** | Zeigt, welche Dokumente von Änderungen betroffen sind |
| **View-Generierung** | Erzeugt rollenzentrierte Sichten, Datenfluss-Karten und Test-Matrizen |

### Kernprinzipien

- **Generisch**: Keine hartkodierten Dokumentnamen — funktioniert mit jedem SPEC_FORMAT-Projekt
- **Strikt**: Fehler werden gemeldet statt toleriert
- **Nachvollziehbar**: Jede Referenz ist auf die Zeile genau lokalisierbar
- **Plattformunabhängig**: Windows (`\r\n`), Unix (`\n`) und Mac (`\r`) werden unterstützt

---

## 🏗️ Architektur

### Datenfluss

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Markdown-Dateien                              │
│                   (mit SPEC_FORMAT-Markern)                          │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   1. Frontmatter-Parser │
                    │   (frontmatter.py)      │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   2. Marker-Parser      │
                    │   (markers.py)          │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   3. MD-Hauptparser     │
                    │   (md_parser.py)        │
                    │   → Abschnitte          │
                    │   → Tabellen            │
                    │   → Referenzen          │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   SpecDocument (Model)  │
                    └───┬───────────────┬────┘
                        │               │
          ┌─────────────▼──┐      ┌────▼──────────────┐
          │ 4. Referenzgraph│      │ 5. Konsistenz-    │
          │ (reference_     │      │    Validator       │
          │  graph.py)      │      │ (consistency.py)  │
          └────────┬────────┘      └────┬──────────────┘
                   │                     │
          ┌────────▼────────┐      ┌────▼──────────────┐
          │ 6. View-        │      │  ValidationReport  │
          │    Generator    │      └───────────────────┘
          │ (views.py)      │
          └─────────────────┘
                   │
          ┌────────▼────────┐
          │  Generierte     │
          │  Views (.md)    │
          └─────────────────┘
```

### Verarbeitungspipeline

```
Datei einlesen → Normalisieren → Frontmatter → Marker → Abschnitte
                                                              ↓
                     Referenzen ← Tabellen ←                  ↓
                          ↓            ↓                     ↓
                    SpecDocument (vereinheitlichtes Objekt)
                          ↓
              ┌───────────┼───────────┐
              ↓           ↓           ↓
         Referenzgraph  Validator  View-Generator
              ↓           ↓           ↓
         Impact-Analyse  Report    .md-Dateien
```

---

## 💻 Installation

### Voraussetzungen

- **Python** ≥ 3.9
- **pip** (aktuell)

### Installation aus dem Quellcode

```bash
# 1. Repository klonen oder herunterladen
cd spec-tool

# 2. Virtuelle Umgebung erstellen (empfohlen)
python -m venv .venv

# 3. Umgebung aktivieren
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Paket im Editable-Mode installieren (inkl. Dev-Dependencies)
pip install -e ".[dev]"
```

### Verifikation der Installation

```bash
# Version prüfen
spec-tool --version

# Hilfe anzeigen
spec-tool --help

# Syntax-Check (ohne Dateien)
spec-tool stats data/
```

### Abhängigkeiten

| Paket | Version | Zweck |
|-------|---------|-------|
| `pydantic` | ≥ 2.0 | Datenmodell-Validierung |
| `pyyaml` | ≥ 6.0 | YAML-Frontmatter-Parsing |
| `click` | ≥ 8.0 | CLI-Framework |
| `rich` | ≥ 13.0 | Terminal-Ausgabe (Tabellen, Farben) |
| `pytest` | ≥ 7.0 | Test-Framework (dev) |
| `pytest-cov` | ≥ 4.0 | Coverage-Reports (dev) |

---

## 🚀 Schnellstart

### 1. Dokumente vorbereiten

Erstelle ein Verzeichnis mit deinen Markdown-Dateien:

```
data/
├── foundation/
│   ├── CHARTER.md
│   └── CONTRACTS.md
└── specs/
    └── MODULE.md
```

### 2. Alle Dokumente parsen

```bash
spec-tool parse-all data/
```

**Erwartete Ausgabe:**

```
📂 data
   Gefundene Dateien: 3

  ✅ foundation/CHARTER.md (v1.0.0, 12 Abschnitte, 5 Referenzen)
  ✅ foundation/CONTRACTS.md (v1.2.1, 88 Abschnitte, 25 Referenzen)
  ✅ specs/MODULE.md (v0.1.0, 6 Abschnitte, 3 Referenzen)

Gesamt: 3 Dokumente geparst, 0 Fehler
```

### 3. Dokumente validieren

```bash
spec-tool validate data/
```

### 4. Impact-Analyse

```bash
spec-tool impact foundation/CHARTER.md --directory data/
```

### 5. Views generieren

```bash
spec-tool generate-views data/ --output-dir views/
```

### 6. Vollständige Verifikation

```bash
spec-tool verify data/
```

---

## 📖 CLI-Befehle

### `spec-tool parse`

Parst eine einzelne Datei und zeigt Details.

```bash
spec-tool parse data/foundation/CHARTER.md
spec-tool parse data/foundation/CHARTER.md --verbose  # Ausführlich
```

**Optionen:**

| Option | Beschreibung |
|--------|-------------|
| `--verbose`, `-v` | Zeigt alle Abschnitte und Referenzen |

**Exit-Codes:**
- `0`: Datei erfolgreich geparst
- `1`: Fehler beim Parsen

---

### `spec-tool parse-all`

Parst alle Markdown-Dateien in einem Verzeichnis.

```bash
spec-tool parse-all data/
spec-tool parse-all data/ --verbose
```

**Verhalten:**
- Durchsucht rekursiv alle `.md`-Dateien
- Ignoriert Verzeichnisse mit `archive` im Namen
- Zeigt pro Datei: Version, Abschnitte, Referenzen
- Zeigt Gesamtstatistik am Ende

---

### `spec-tool validate`

Validiert die Konsistenz aller Dokumente.

```bash
spec-tool validate data/
spec-tool validate data/ --strict  # Auch Warnungen als Fehler
```

**Optionen:**

| Option | Beschreibung |
|--------|-------------|
| `--strict` | Bricht auch bei Warnungen ab |

**Ausgabe:**

```
🔍 Validierung von data

Metrik               Wert
──────────────────────────
Dokumente geprüft    12
Referenzen geprüft   1140
Fehler               0
Warnungen            0
Status               GÜLTIG
```

---

### `spec-tool check`

Validiert eine einzelne Datei.

```bash
spec-tool check data/foundation/CHARTER.md
```

**Ausgabe:**

```
✅ CHARTER.md ist gültig
```

oder

```
✗ CHARTER.md ist ungültig
  ✗ V-01 Kein YAML-Frontmatter gefunden
```

---

### `spec-tool impact`

Zeigt, welche Dokumente von Änderungen betroffen sind.

```bash
spec-tool impact foundation/CHARTER.md --directory data/
spec-tool impact foundation/CONTRACTS.md --section 6.10 --directory data/
```

**Optionen:**

| Option | Beschreibung |
|--------|-------------|
| `--section`, `-s` | Abschnitts-ID für gezielte Analyse |
| `--directory`, `-d` | Verzeichnis mit Dokumenten (Default: `data`) |

**Ausgabe:**

```
🎯 Impact-Analyse für foundation/CHARTER.md

11 betroffene Dokumente/Abschnitte:

  → foundation/CONTRACTS.md
  → specs/GREMIUM.md
  → specs/QUESTOR.md
  → ...
```

---

### `spec-tool stats`

Zeigt Statistiken über den Referenzgraphen.

```bash
spec-tool stats data/
```

**Ausgabe:**

```
📊 Statistiken für data

╭───────────────────────────┬──────╮
│ Metrik                    │ Wert │
├───────────────────────────┼──────┤
│ Dokumente                 │ 12   │
│ Abschnitte                │ 88   │
│ Referenzen                │ 1140 │
│ Cross-Document-Referenzen │ 1140 │
│ Cross-Layer-Referenzen    │ 490  │
│ Gebrochene Referenzen     │ 0    │
│ Graph-Knoten              │ 582  │
│ Graph-Kanten              │ 1140 │
╰───────────────────────────╯
```

---

### `spec-tool graph`

Zeigt den Referenzgraphen als Baum oder Liste.

```bash
spec-tool graph data/
spec-tool graph data/ --format list
```

**Optionen:**

| Option | Beschreibung |
|--------|-------------|
| `--format` | `tree` (Default) oder `list` |

---

### `spec-tool roles`

Listet alle definierten Rollen auf.

```bash
spec-tool roles data/
```

**Ausgabe:**

```
👥 Rollen (26)

╭──────────────────────────┬─────────┬──────┬──────────┬──────────┬────────╮
│ Rolle                    │ Schicht │ LLM  │ Eingänge │ Ausgänge │ Regeln │
├──────────────────────────┼─────────┼──────┼──────────┼──────────┼────────┤
│ archivar                 │ 4       │ Nein │ 1        │ 3        │ 6      │
│ kartograph               │ 4       │ Nein │ 2        │ 5        │ 7      │
│ kanzler                  │ 4       │ Nein │ 3        │ 3        │ 3      │
│ ...                      │         │      │          │          │        │
╰──────────────────────────┴─────────┴──────┴──────────┴──────────┴────────╯
```

---

### `spec-tool dataflows`

Listet alle definierten Datenflüsse auf.

```bash
spec-tool dataflows data/
```

**Verhalten:**
- Dedupliziert Datenflüsse nach `dataflow_id`
- Zeigt Trigger, Schritte und Quelldatei

---

### `spec-tool generate-views`

Generiert Views als Markdown-Dateien.

```bash
spec-tool generate-views data/ --output-dir views/
```

**Erzeugte Dateien:**

| Datei | Inhalt |
|-------|--------|
| `views/ROLE_VIEWS.md` | Alle Rollen mit Eingängen, Ausgängen, Regeln |
| `views/DATAFLOW_MAP.md` | Alle Datenflüsse mit Schritten |
| `views/TEST_MATRIX.md` | Alle Test-Einträge nach Rollen gruppiert |

---

### `spec-tool verify`

Führt eine vollständige Verifikation durch (Parse + Validate + Graph + Stats + Views-Vorschau).

```bash
spec-tool verify data/
spec-tool verify data/ --strict
```

**Ausgabe:**

```
╭────────────────────────────────────────────────╮
│ 🔬 Vollständige Verifikation                   │
╰────────────────────────────────────────────────╯

Schritt 1: Parse
  12 Dokumente geparst

Schritt 2: Validate
  Fehler: 0
  Warnungen: 0
  Status: GÜLTIG

Schritt 3: Graph
  Knoten: 582
  Kanten: 1140
  Gebrochene Referenzen: 0

Schritt 4: Views (Vorschau)
  Rollen: 26
  Datenflüsse: 21
  Test-Einträge: 0

==================================================
✅ Verifikation bestanden
```

---

## 📐 Das SPEC_FORMAT

Das SPEC_FORMAT ist das Dateiformat, das `spec-tool` versteht. Es besteht aus drei Schichten:

### Schicht 1: YAML-Frontmatter

Jede Datei beginnt mit einem YAML-Block zwischen `---`-Markern:

```yaml
---
doc_id: foundation/CONTRACTS.md
doc_type: contracts
version: 1.2.1-twin.1
status: BINDEND
schema_version: spec-format-1.0
layer: foundation
builds_on:
  - foundation/CHARTER.md@1.0.0
conflict_rule: [CHARTER, THIS_DOC]
roles_defined: []
roles_referenced: []
dataflows_defined: []
last_modified: 2026-08-21
---
```

#### Pflichtfelder

| Feld | Typ | Beschreibung | Beispiel |
|------|-----|-------------|---------|
| `doc_id` | string | Eindeutiger Pfad der Datei | `foundation/CHARTER.md` |
| `doc_type` | enum | Dokumenttyp | `charter`, `contracts`, `spec` |
| `version` | string | Semantische Version | `1.2.1-twin.1` |
| `status` | string | Dokumentstatus | `BINDEND`, `ENTWURF` |
| `schema_version` | string | SPEC_FORMAT-Version | `spec-format-1.0` |
| `layer` | enum | Schicht | `foundation`, `specs`, `ops` |
| `builds_on` | list | Abhängigkeiten | `[foundation/CHARTER.md@1.0.0]` |
| `conflict_rule` | list | Konflikthierarchie | `[CHARTER, THIS_DOC]` |
| `last_modified` | string | ISO-8601 Datum | `2026-08-21` |

#### Optionale Felder

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `roles_defined` | list | In dieser Datei definierte Rollen |
| `roles_referenced` | list | Referenzierte Rollen |
| `dataflows_defined` | list | Definierte Datenflüsse |
| `test_suites_defined` | list | Definierte Test-Suiten |

#### doc_type — Mögliche Werte

| Wert | Beschreibung | Typische Schicht |
|------|-------------|-----------------|
| `charter` | Verfassung, Sicherheitsregeln | `foundation/` |
| `contracts` | Datenverträge, Pydantic-Modelle | `foundation/` |
| `spec` | Spezifikation | `specs/` |
| `test-strategy` | Teststrategie | `ops/` |
| `roadmap` | Implementierungsplan | `ops/` |
| `format-definition` | Formatdefinition | `foundation/` |
| `view` | Generierte Sicht | `views/` |
| `patch` | Änderungsanweisung | `patches/` |

#### layer — Mögliche Werte

| Wert | Rang | Beschreibung |
|------|------|-------------|
| `foundation` | 0 | Höchste Autorität (CHARTER, CONTRACTS) |
| `specs` | 1 | Spezifikationen |
| `ops` | 2 | Operationale Dokumente |
| `views` | 3 | Generierte Sichten |

---

### Schicht 2: HTML-Kommentar-Marker

Marker sind HTML-Kommentare mit `@`-Präfix. Sie sind **unsichtbar im gerenderten Markdown**, aber für den Parser lesbar.

#### Syntax

```markdown
<!-- @marker-name attribut="wert" attribut2="wert2" -->
```

#### Verfügbare Marker-Typen

##### `@section`

Definiert einen Abschnitt.

```markdown
<!-- @section id="3.2" title="Kartograph" type="role-definition" role="kartograph" -->
### §3.2 Kartograph (Stufe 4)
```

| Attribut | Pflicht | Beschreibung |
|----------|---------|-------------|
| `id` | ✅ | Eindeutige ID (z.B. `3.2`, `6.10.19`) |
| `title` | ✅ | Menschenlesbarer Titel |
| `type` | ✅ | Abschnittstyp (siehe Tabelle unten) |
| `role` | Optional | Rolle (bei `type="role-definition"`) |
| `contract` | Optional | Vertragsname (bei `type="contract"`) |
| `dataflow` | Optional | Datenfluss-ID (bei `type="dataflow"`) |
| `suite` | Optional | Test-Suite (bei `type="test-suite"`) |
| `machine` | Optional | Zustandsmaschine (bei `type="state-machine"`) |

**Abschnittstypen:**

| Typ | Beschreibung |
|-----|-------------|
| `meta` | Geltung, Änderungsregeln, Präambel |
| `prose` | Freitext, Beschreibungen |
| `change-request` | Änderungsantrag |
| `contract` | Vertragsdefinition |
| `enum` | Enum-Definition |
| `state-machine` | Zustandsmaschine |
| `dataflow` | Datenflussbeschreibung |
| `role-definition` | Rollendefinition |
| `test-suite` | Test-Suite |
| `test-case` | Einzelner Testfall |
| `safety-rule` | Sicherheitsregel |
| `implementation-phase` | Implementierungsphase |
| `acceptance` | Akzeptanzprüfung |
| `config` | Konfiguration |

##### `@table`

Definiert eine Tabelle mit Schema.

```markdown
<!-- @table schema="role_permissions" role="kartograph" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Atlas schreiben | QuestorBlackbox lesen | SR-07 |
```

**Verfügbare Schemata:**

| Schema | Spalten |
|--------|---------|
| `role_permissions` | Erlaubt, Verboten, CHARTER-Ref |
| `role_inputs` | Quelle, Daten, Vertrag, Bedingung |
| `role_outputs` | Ziel, Daten, Vertrag, Bedingung |
| `role_rules` | Regel, CHARTER-Ref, Konsequenz |
| `state_machine_states` | Zustand, Bedeutung, Dauer |
| `state_transitions` | Von, Nach, Auslöser, Bedingung |
| `test_cases` | Test-ID, Test, Erwartet, CHARTER-Ref, Rolle |
| `enum_values` | Wert, Bedeutung |
| `error_codes` | Fehler, Bedeutung, Fehlerklasse |
| `status_semantics` | Status, abbruch_grund, abbruch_klasse |
| `corrections` | #, Korrektur, Quelle, Status |
| `safety_rules` | ID, Regel, Kategorie |

##### `@ref`

Definiert einen Querverweis.

```markdown
<!-- @ref target="CHARTER §SR-04" type="security-rule" -->
→ Siehe CHARTER §SR-04 für Details.
```

| Attribut | Pflicht | Beschreibung |
|----------|---------|-------------|
| `target` | ✅ | Ziel (z.B. `CHARTER §SR-04`) |
| `type` | Optional | Referenztyp (Default: `spec`) |

**Referenztypen:**

| Typ | Beschreibung |
|-----|-------------|
| `security-rule` | CHARTER-Sicherheitsregel |
| `contract` | Datenvertrag |
| `spec` | Spezifikationsabschnitt |
| `enum` | Enum-Definition |
| `role` | Rolle |
| `dataflow` | Datenfluss |
| `test` | Testfall |
| `config` | Konfigurationsparameter |

##### `@role`

Definiert eine Rolle.

```markdown
<!-- @role id="kartograph" layer="4" llm="false" pipeline_stage="2" -->
```

| Attribut | Pflicht | Beschreibung |
|----------|---------|-------------|
| `id` | ✅ | Eindeutige Rollen-ID |
| `layer` | ✅ | Schicht (1–5) |
| `llm` | ✅ | `true` oder `false` |
| `pipeline_stage` | Optional | Stufe in der Pipeline |

##### `@contract`

Definiert einen Vertrag.

```markdown
<!-- @contract name="ResearchPackage" type="pydantic" section="1.1" charter_refs="SR-04,SR-15" -->
```

| Attribut | Pflicht | Beschreibung |
|----------|---------|-------------|
| `name` | ✅ | Vertragsname |
| `type` | ✅ | Vertragstyp (`pydantic`, `protocol`, `config`) |
| `section` | Optional | Abschnitts-ID |
| `charter_refs` | Optional | CHARTER-Referenzen |

##### `@dataflow` und `@dataflow-step`

Definieren einen Datenfluss.

```markdown
<!-- @dataflow id="twin_drift" trigger="TWIN_DIVERGENCE" source_role="kartograph" target_role="strategic_layer" -->
<!-- @dataflow-step order="1" -->
1. Extrahiere metric_vector aus Sim-Kristall und Real-Kristall.
```

##### `@safety-rule`

Definiert eine Sicherheitsregel.

```markdown
<!-- @safety-rule id="SR-04" category="grundregel" -->
```

##### `@state-machine`

Definiert eine Zustandsmaschine.

```markdown
<!-- @state-machine id="questor_state" states="11" -->
```

---

### Schicht 3: Markdown-Inhalt

Der eigentliche Inhalt der Datei — Abschnitte, Tabellen, Code-Blöcke.

---

## 📦 Modul-Referenz

### 1. Frontmatter-Parser

**Datei:** `src/spec_tool/parser/frontmatter.py`

**Zweck:** Extrahiert den YAML-Frontmatter aus dem Dateianfang.

**Funktion:**

```python
def parse_frontmatter(content: str) -> tuple[Optional[Frontmatter], str]:
    """
    Parst den YAML-Frontmatter aus dem Inhalt.

    Returns:
        Tuple aus (Frontmatter | None, restlicher Inhalt)
    """
```

**Verhalten:**

1. Sucht nach `---\n...\n---` am Dateianfang
2. Parst den YAML-Block mit `yaml.safe_load`
3. Konvertiert Datumsangaben (`datetime.date` → `str`)
4. Erzeugt ein `Frontmatter`-Pydantic-Objekt
5. Gibt den restlichen Inhalt ohne Frontmatter zurück

**Fehlerbehandlung:**

| Fall | Verhalten |
|------|-----------|
| Kein Frontmatter gefunden | Gibt `(None, content)` zurück |
| Ungültiges YAML | Gibt `(None, content)` zurück |
| Fehlende Pflichtfelder | Gibt `(None, content)` zurück |

---

### 2. Marker-Parser

**Datei:** `src/spec_tool/parser/markers.py`

**Zweck:** Extrahiert alle HTML-Kommentar-Marker aus dem Inhalt.

**Funktion:**

```python
def parse_markers_multiline(content: str) -> list[Marker]:
    """
    Parst alle Marker aus dem Inhalt.

    Returns:
        Liste von Marker-Objekten
    """
```

**Regex-Pattern:**

```python
MARKER_PATTERN = re.compile(
    r"<!--\s*@([\w-]+)(.*?)-->",
    re.DOTALL
)
```

**Wichtig:** Das Pattern matcht auch Bindestriche in Marker-Namen (`@safety-rule`, `@state-machine`).

**Attribut-Parsing:**

```python
ATTRIBUTE_PATTERN = re.compile(
    r'(\w[\w-]*)=["\']([^"\']*?)["\']'
)
```

**Typ-Konvertierung:**

| Attribut | Konvertierung |
|----------|--------------|
| `llm` | `"true"`/`"false"` → `bool` |
| `layer`, `order`, `line`, `states` | `str` → `int` |
| Alle anderen | Bleiben `str` |

---

### 3. MD-Hauptparser

**Datei:** `src/spec_tool/parser/md_parser.py`

**Zweck:** Orchestrat das gesamte Parsing und erzeugt ein `SpecDocument`-Objekt.

**Klasse:**

```python
class MarkdownParser:
    def parse_file(self, file_path: Path) -> SpecDocument: ...
    def parse_content(self, content: str, file_path: Optional[Path] = None,
                      known_doc_ids: Optional[Set[str]] = None) -> SpecDocument: ...
```

**Verarbeitungsschritte:**

| Schritt | Methode | Beschreibung |
|---------|---------|-------------|
| 1 | `parse_frontmatter()` | Frontmatter extrahieren |
| 2 | `parse_markers_multiline()` | Marker extrahieren |
| 3 | `_parse_sections()` | Abschnitte parsen |
| 4 | `_parse_tables()` | Tabellen parsen |
| 5 | `_parse_references()` | Referenzen parsen |
| 6 | `_assign_references_to_sections()` | Referenzen zuordnen |
| 7 | `_assign_markers_to_sections()` | Marker zuordnen |

**Abschnittserkennung:**

Der Parser erkennt drei Arten von Abschnitts-Überschriften:

1. **Markdown-Überschriften:** `## §1 Titel`
2. **§-Textzeilen:** `§1 Titel` (ohne `#`)
3. **Nummerierte Textzeilen:** `1. Titel` (ohne `§` und `#`)

**Referenzauflösung (generisch):**

Der Parser leitet bekannte Dokumentnamen **dynamisch aus den geladenen Dateien** ab:

```python
# Aus "foundation/CHARTER.md" werden die Aliase:
known_aliases = {
    "CHARTER": "foundation/CHARTER.md",
    "CHARTER.md": "foundation/CHARTER.md",
}
```

Dadurch funktioniert das Tool mit **jedem Projekt**, nicht nur mit MYRMEX.

**Textbasierte Referenzen:**

```python
TEXT_REF_PATTERN = re.compile(
    r"→\s*(?:Siehe\s+)?(?:`)?([\w/\.]+)\s+§([\w\.\-]+)(?:`)?"
)
```

**Wichtig:** Textbasierte Referenzen werden nur erkannt, wenn ein `§`-Symbol vorhanden ist. Das verhindert, dass Aufzählungen oder Zustandsdiagramme als Referenzen erkannt werden.

---

### 4. Referenzgraph

**Datei:** `src/spec_tool/graph/reference_graph.py`

**Zweck:** Baut einen gerichteten Graphen aus allen Querverweisen.

**Klasse:**

```python
class ReferenceGraph:
    def add_document(self, doc: SpecDocument): ...
    def build(self): ...
    def find_broken_references(self) -> list[Reference]: ...
    def impact_analysis(self, doc_id: str, section_id: Optional[str] = None) -> list[str]: ...
    def get_statistics(self) -> dict: ...
```

**Funktionsweise:**

1. `add_document()`: Registriert ein Dokument und seine Abschnitte als Knoten
2. `build()`: Erstellt Kanten aus allen Referenzen
3. `find_broken_references()`: Findet Referenzen, deren Ziel nicht existiert
4. `impact_analysis()`: BFS über den Reverse-Graphen

**Logik für gebrochene Referenzen:**

| Fall | Verhalten |
|------|-----------|
| Ziel-Dokument bekannt + Abschnitt existiert | ✅ Gültig |
| Ziel-Dokument bekannt + Abschnitt fehlt | ❌ Gebrochen |
| Ziel-Dokument unbekannt + `@ref`-Marker | ❌ Gebrochen (explizit gewollt) |
| Ziel-Dokument unbekannt + Textreferenz | ⏭️ Ignoriert (informell) |

**Alias-Auflösung:**

Der Graph löst Dokumentnamen über Aliase auf:

```python
# "CHARTER" wird zu "foundation/CHARTER.md" aufgelöst
# wenn "foundation/CHARTER.md" geladen ist
```

---

### 5. Konsistenz-Validator

**Datei:** `src/spec_tool/validator/consistency.py`

**Zweck:** Prüft die Konsistenz aller Dokumente.

**Validierungsregeln:**

| Regel | Beschreibung | Schwere |
|-------|-------------|---------|
| V-01 | Frontmatter vorhanden und gültig | ERROR |
| V-02 | `doc_id` entspricht Dateipfad | ERROR |
| V-03 | Alle Pflichtfelder vorhanden | ERROR |
| V-04 | `@section`-Marker vollständig | ERROR |
| V-05 | `doc_id` stimmt mit Pfad überein | WARNING |
| V-06 | Gebrochene Referenzen | WARNING |
| V-07 | CHARTER-Regeln existieren | WARNING |
| V-08 | Rollen-IDs konsistent | WARNING |
| V-09 | Abschnitts-IDs eindeutig | WARNING |
| V-10 | Test-IDs eindeutig | WARNING |
| V-11 | `builds_on` referenziert existierende Dateien | WARNING |
| V-12 | Keine zirkulären Abhängigkeiten | ERROR |

**Rückgabewert:**

```python
@dataclass
class ValidationReport:
    results: list[ValidationResult]
    documents_checked: int
    references_checked: int

    @property
    def errors(self) -> list[ValidationResult]: ...

    @property
    def warnings(self) -> list[ValidationResult]: ...

    @property
    def is_valid(self) -> bool: ...
```

---

### 6. View-Generator

**Datei:** `src/spec_tool/generator/views.py`

**Zweck:** Erzeugt rollenzentrierte Sichten, Datenfluss-Karten und Test-Matrizen.

**Klassen:**

```python
class ViewGenerator:
    def generate_role_views(self, documents: list[SpecDocument]) -> list[RoleView]: ...
    def generate_dataflow_views(self, documents: list[SpecDocument]) -> list[DataflowView]: ...
    def generate_test_matrix(self, documents: list[SpecDocument]) -> list[TestMatrixEntry]: ...

    def render_role_views_markdown(self, role_views: list[RoleView]) -> str: ...
    def render_dataflow_views_markdown(self, df_views: list[DataflowView]) -> str: ...
    def render_test_matrix_markdown(self, test_entries: list[TestMatrixEntry]) -> str: ...
```

**Erkennungslogik:**

| View | Erkennung | Quelle |
|------|-----------|--------|
| Rolle | `@section type="role-definition"` + `@role`-Marker | Abschnitte |
| Datenfluss | `@section type="dataflow"` + `@dataflow`-Marker | Abschnitte |
| Test | `@section type="test-suite"` + Tabelle `schema="test_cases"` | Tabellen |

**Deduplizierung:**

- Datenflüsse werden nach `dataflow_id` dedupliziert
- Rollen werden nach `role_id` zusammengeführt
- Rekursive Suche durch Abschnittshierarchie

---

## 🗂️ Datenmodell

### SpecDocument

```python
class SpecDocument(BaseModel):
    file_path: Path
    frontmatter: Optional[Frontmatter]
    sections: list[Section]
    references: list[Reference]
    markers: list[Marker]
    tables: list[ParsedTable]
    raw_content: str
    parse_errors: list[str]
```

### Section

```python
class Section(BaseModel):
    section_id: str
    title: str
    section_type: SectionType
    level: int
    content: str
    markers: list[Marker]
    tables: list[ParsedTable]
    references: list[Reference]
    children: list[Section]
    line_number: int

    # Rollen-spezifisch
    role_id: Optional[str]
    role_layer: Optional[int]
    role_llm: Optional[bool]

    # Vertrags-spezifisch
    contract_name: Optional[str]
    contract_type: Optional[str]

    # Datenfluss-spezifisch
    dataflow_id: Optional[str]
    dataflow_trigger: Optional[str]

    # Sicherheitsregel-spezifisch
    safety_rule_id: Optional[str]
```

### Reference

```python
class Reference(BaseModel):
    source_doc: str
    source_section: Optional[str]
    target_doc: str
    target_section: Optional[str]
    reference_type: ReferenceType
    raw_text: str
    line_number: int
```

### Marker

```python
class Marker(BaseModel):
    marker_type: MarkerType
    raw: str
    line_number: int
    attributes: dict[str, Any]
```

### ParsedTable

```python
class ParsedTable(BaseModel):
    schema_name: Optional[str]
    headers: list[str]
    rows: list[list[str]]
    line_number: int
```

---

## 🧪 Testsuite

### Struktur

```
tests/
├── conftest.py                          # Fixtures
├── fixtures/
│   ├── minimal_doc.md                   # Minimale Testdatei
│   └── broken_refs.md                   # Datei mit gebrochenen Referenzen
├── test_e2e.py                          # End-to-End-Tests (12 Tests)
├── test_parser/
│   ├── test_frontmatter.py              # Frontmatter-Tests (8 Tests)
│   ├── test_markers.py                  # Marker-Tests (11 Tests)
│   └── test_md_parser.py               # MD-Parser-Tests (9 Tests)
├── test_graph/
│   └── test_reference_graph.py          # Referenzgraph-Tests (5 Tests)
└── test_validator/
    └── test_consistency.py              # Konsistenz-Tests (5 Tests)
```

### Ausführen

```bash
# Alle Tests
pytest -v

# Mit Coverage
pytest -v --cov=src/spec_tool --cov-report=html

# Nur Unit-Tests
pytest -v -m "not e2e"

# Nur E2E-Tests
pytest -v tests/test_e2e.py
```

### Test-Übersicht

| Test-Datei | Tests | Beschreibung |
|-----------|-------|-------------|
| `test_frontmatter.py` | 8 | Frontmatter-Parsing |
| `test_markers.py` | 11 | Marker-Parsing |
| `test_md_parser.py` | 9 | MD-Hauptparser |
| `test_reference_graph.py` | 5 | Referenzgraph |
| `test_consistency.py` | 5 | Konsistenz-Validator |
| `test_e2e.py` | 12 | End-to-End mit echten Dateien |
| **Gesamt** | **50** | |

---

## 📁 Projektstruktur

```
spec-tool/
├── pyproject.toml                       # Projekt-Konfiguration
├── README.md                            # Diese Datei
│
├── src/
│   └── spec_tool/
│       ├── __init__.py                  # Paket-Initialisierung
│       ├── cli.py                       # CLI-Einstiegspunkt
│       ├── models.py                    # Datenmodell (Pydantic)
│       │
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── frontmatter.py           # Frontmatter-Parser
│       │   ├── markers.py               # Marker-Parser
│       │   └── md_parser.py             # MD-Hauptparser
│       │
│       ├── graph/
│       │   ├── __init__.py
│       │   └── reference_graph.py       # Referenzgraph
│       │
│       ├── validator/
│       │   ├── __init__.py
│       │   └── consistency.py           # Konsistenz-Validator
│       │
│       └── generator/
│           ├── __init__.py
│           └── views.py                 # View-Generator
│
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── minimal_doc.md
│   │   └── broken_refs.md
│   ├── test_e2e.py
│   ├── test_parser/
│   ├── test_graph/
│   └── test_validator/
│
└── data/                                # Spezifikationsdokumente
    ├── foundation/
    │   ├── CHARTER.md
    │   ├── CONTRACTS.md
    │   ├── MASTER_INDEX.md
    │   └── SPEC_FORMAT.md
    ├── specs/
    │   ├── GREMIUM.md
    │   ├── GREMIUM_STRATEGY.md
    │   ├── QUESTOR.md
    │   ├── HAL.md
    │   └── CAROUSEL_TWIN.md
    └── ops/
        ├── VALIDATION.md
        ├── VALIDATION_ATLAS.md
        └── ROADMAP.md
```

---

## ⚙️ Konfigurationsmöglichkeiten

### pyproject.toml

```toml
[project]
name = "spec-tool"
version = "0.2.0"
description = "Parser, Validator und View-Generator für strukturierte Spezifikationsdokumente"
requires-python = ">=3.9"
dependencies = [
    "pydantic>=2.0",
    "pyyaml>=6.0",
    "click>=8.0",
    "rich>=13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[project.scripts]
spec-tool = "spec_tool.cli:main"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
    "unit: Unit-Tests",
    "integration: Integrationstests",
    "e2e: End-to-End-Tests",
]

[tool.coverage.run]
source = ["src/spec_tool"]

[tool.coverage.report]
fail_under = 80
```

### Optional: spec-tool.yaml

Für projektspezifische Anpassungen kann eine Konfigurationsdatei erstellt werden:

```yaml
# spec-tool.yaml (optional)
reference_aliases:
  CHARTER: foundation/CHARTER.md
  QUESTOR: specs/QUESTOR.md
  "GREMIUM_STRATEGY": specs/GREMIUM_STRATEGY.md

ignore_dirs:
  - archive
  - drafts
```

---

## 🚨 Fehlerbehandlung

### Parse-Fehler

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `Kein gültiger YAML-Frontmatter gefunden` | Frontmatter fehlt oder ist ungültig | Frontmatter hinzufügen/korrigieren |
| `ImportError: cannot import name 'MarkdownParser'` | Syntaxfehler in `md_parser.py` | Datei mit `python -c "import ast; ast.parse(...)"` prüfen |
| `AttributeError: 'bool' object has no attribute 'lower'` | `llm`-Attribut ist bereits `bool` | `isinstance`-Prüfung verwenden |

### Referenz-Fehler

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| Viele gebrochene Referenzen | Textbasierte Referenzen auf Nicht-Dokumente | Nur `→ DOKUMENT §ABSCHNITT` als Referenz verwenden |
| `CHARTER` wird nicht aufgelöst | `CHARTER.md` nicht geladen | Alle referenzierten Dokumente laden |

### Validierungs-Fehler

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `V-01: Kein YAML-Frontmatter gefunden` | Datei ohne Frontmatter | Frontmatter hinzufügen |
| `V-02: doc_id stimmt nicht mit Pfad überein` | `doc_id` ≠ Dateipfad | `doc_id` anpassen |

---

## ❓ FAQ

### Funktioniert spec-tool nur mit MYRMEX?

**Nein.** Der Parser ist generisch und funktioniert mit jedem Projekt, das das SPEC_FORMAT verwendet. Dokumentnamen werden dynamisch aus den geladenen Dateien abgeleitet.

### Wie füge ich neue Marker-Typen hinzu?

1. Neuen Wert in `MarkerType`-Enum (`models.py`) hinzufügen
2. Pattern in `markers.py` hinzufügen
3. Verarbeitung in `md_parser.py` hinzufügen

### Wie funktionieren die Alias-Auflösungen?

Aus jedem geladenen Dokument werden automatisch Aliase erzeugt:

```
foundation/CHARTER.md → CHARTER, CHARTER.md
specs/QUESTOR.md → QUESTOR, QUESTOR.md
```

Referenzen wie `→ CHARTER §SR-04` werden dann zu `→ foundation/CHARTER.md §SR-04` aufgelöst.

### Warum werden manche Referenzen ignoriert?

Textbasierte Referenzen (ohne `@ref`-Marker) werden nur erkannt, wenn:
1. Ein `§`-Symbol vorhanden ist (z.B. `→ CHARTER §SR-04`)
2. Das Ziel-Dokument bekannt ist (geladen oder als Alias registriert)

Das verhindert, dass Aufzählungen wie `→ PENDING` oder `→ Questor` als Referenzen erkannt werden.

### Wie kann ich Views anpassen?

Die `ViewGenerator`-Klasse kann erweitert werden:

```python
class CustomViewGenerator(ViewGenerator):
    def render_role_views_markdown(self, role_views):
        # Angepasstes Rendering
        ...
```

---

## 📄 Lizenz

Dieses Projekt ist ein internes Werkzeug für das MYRMEX-Projekt.

---

## 🔗 Weiterführende Links

- [SPEC_FORMAT v1.0.0](data/foundation/SPEC_FORMAT.md) — Die vollständige Formatdefinition
- [CHARTER.md](data/foundation/CHARTER.md) — Die Verfassung des MYRMEX-Systems
- [CONTRACTS.md](data/foundation/CONTRACTS.md) — Alle Datenverträge

---

*Letzte Aktualisierung: 2026-08-21*