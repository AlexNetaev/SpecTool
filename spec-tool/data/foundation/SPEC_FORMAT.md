---
doc_id: foundation/SPEC_FORMAT.md
doc_type: format-definition
version: 1.0.0
status: BINDEND
schema_version: spec-format-1.0
layer: foundation
builds_on: []
conflict_rule: []
roles_defined: []
roles_referenced: []
dataflows_defined: []
last_modified: 2026-08-21
---

<!-- @section id="0" title="Zweck und Geltung" type="meta" -->
# 📐 SPEC_FORMAT — FORMATDEFINITION FÜR SPEZIFIKATIONSDOKUMENTE

## §0 Zweck und Geltung

Dieses Dokument definiert das einheitliche Dateiformat für alle
Spezifikationsdokumente des MYRMEX-Systems.

Es ist die **verbindliche Referenz** für:
- Den Spec-Tool-Parser (maschinelles Einlesen)
- Die Erstellung neuer Spezifikationsdokumente
- Die Migration bestehender Dokumente
- Die Validierung der Dokumentstruktur

Regel: Alle Dokumente in `foundation/`, `specs/`, `ops/` und `views/`
MÜSSEN diesem Format folgen.

Konfliktregel: Bei Widersprüchen zwischen diesem Dokument und einem
Spezifikationsdokument gilt das Spezifikationsdokument für den Inhalt,
aber dieses Dokument für die Struktur.

<!-- @section id="1" title="Dateistruktur" type="prose" -->
## §1 Dateistruktur

Jede Spezifikationsdatei besteht aus drei Teilen:

| Teil | Beschreibung | Pflicht |
|------|-------------|---------|
| YAML-Frontmatter | Metadaten zwischen `---`-Markern | ✅ Pflicht |
| Markdown-Körper | Inhalt mit @-Markern | ✅ Pflicht |
| Anhang (optional) | Akzeptanzprüfung, Korrekturhinweise | Optional |

### §1.1 Verzeichnisstruktur

| Verzeichnis | Layer | Inhalt |
|-------------|-------|--------|
| `foundation/` | foundation | CHARTER, CONTRACTS, SPEC_FORMAT |
| `specs/` | specs | GREMIUM, GREMIUM_STRATEGY, QUESTOR, HAL, CAROUSEL_TWIN |
| `ops/` | ops | VALIDATION, VALIDATION_ATLAS, ROADMAP |
| `views/` | views | Generierte Sichten (ROLE_VIEWS, DATAFLOW_MAP, TEST_MATRIX) |
| `patches/` | patches | Änderungsanweisungen (archiviert nach Einarbeitung) |
| `archive/` | archive | Veraltete Dokumente |

<!-- @section id="2" title="YAML-Frontmatter" type="prose" -->
## §2 YAML-Frontmatter

### §2.1 Pflichtfelder

| Feld | Typ | Beschreibung | Beispiel |
|------|-----|-------------|---------|
| `doc_id` | string | Relativer Pfad der Datei | `specs/GREMIUM.md` |
| `doc_type` | enum | Dokumenttyp | `spec` |
| `version` | string | Semantische Version | `2.0.0-strat.1` |
| `status` | string | Dokumentstatus | `BINDEND` |
| `schema_version` | string | Formatversion | `spec-format-1.0` |
| `layer` | enum | Schicht | `specs` |
| `builds_on` | list | Abhängigkeiten | `[foundation/CHARTER.md@1.0.0]` |
| `conflict_rule` | list | Konflikthierarchie | `[CHARTER, CONTRACTS, THIS_DOC]` |
| `last_modified` | string | ISO-8601 Datum | `2026-08-21` |

### §2.2 Optionale Felder

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `roles_defined` | list | In diesem Dokument definierte Rollen |
| `roles_referenced` | list | Referenzierte Rollen |
| `dataflows_defined` | list | Definierte Datenflüsse |
| `test_suites_defined` | list | Definierte Test-Suiten |

### §2.3 doc_type — Dokumenttypen

| Wert | Beschreibung | Verzeichnis |
|------|-------------|-------------|
| `charter` | Verfassung, Sicherheitsregeln | `foundation/` |
| `contracts` | Datenverträge, Pydantic-Modelle | `foundation/` |
| `format-definition` | Formatdefinition (dieses Dokument) | `foundation/` |
| `spec` | Spezifikation | `specs/` |
| `test-strategy` | Teststrategie | `ops/` |
| `roadmap` | Implementierungsplan | `ops/` |
| `view` | Generierte Sicht | `views/` |
| `patch` | Änderungsanweisung | `patches/` |

### §2.4 layer — Schichten

| Wert | Rang | Beschreibung |
|------|------|-------------|
| `foundation` | 0 | Höchste Autorität |
| `specs` | 1 | Spezifikationen |
| `ops` | 2 | Operationale Dokumente |
| `views` | 3 | Generierte Sichten |

<!-- @section id="3" title="Marker-Typen Übersicht" type="prose" -->
## §3 Marker-Typen Übersicht

Alle Marker sind HTML-Kommentare der Form `<!-- @marker-name attribut="wert" -->`.

| Marker | Zweck | Beispiel |
|--------|-------|---------|
| `@section` | Abschnitt definieren | `<!-- @section id="3.2" title="Kartograph" type="role-definition" -->` |
| `@table` | Tabelle mit Schema | `<!-- @table schema="role_permissions" role="kartograph" -->` |
| `@ref` | Querverweis | `<!-- @ref target="CHARTER §SR-04" type="security-rule" -->` |
| `@role` | Rolle definieren | `<!-- @role id="kartograph" layer="4" llm="false" -->` |
| `@role-ref` | Rolle referenzieren | `<!-- @role-ref id="archivar" -->` |
| `@contract` | Vertrag definieren | `<!-- @contract name="QuestorErgebnisPaket" type="pydantic" -->` |
| `@state-machine` | Zustandsmaschine | `<!-- @state-machine id="questor_state" states="11" -->` |
| `@dataflow` | Datenfluss | `<!-- @dataflow id="ergebnis_rueckfluss" trigger="QUESTOR_COMPLETED" -->` |
| `@dataflow-step` | Datenfluss-Schritt | `<!-- @dataflow-step order="1" -->` |
| `@safety-rule` | Sicherheitsregel | `<!-- @safety-rule id="SR-04" category="grundregel" -->` |
| `@test` | Testfall | `<!-- @test id="I-01" suite="I" component="integration" -->` |

<!-- @section id="4" title="@section Marker" type="prose" -->
## §4 @section Marker

### §4.1 Syntax

```
<!-- @section id="ABSCHNITTS_ID" title="TITEL" type="TYP" [weitere Attribute] -->
```

### §4.2 Pflichtattribute

| Attribut | Typ | Beschreibung |
|----------|-----|-------------|
| `id` | string | Eindeutige ID innerhalb der Datei (z.B. `3.2`, `6.14.4`) |
| `title` | string | Menschenlesbarer Titel |
| `type` | enum | Abschnittstyp |

### §4.3 Abschnittstypen

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

### §4.4 Optionale Attribute

| Attribut | Typ | Anwendung |
|----------|-----|-----------|
| `role` | string | Bei `type="role-definition"` |
| `contract` | string | Bei `type="contract"` |
| `dataflow` | string | Bei `type="dataflow"` |
| `suite` | string | Bei `type="test-suite"` |
| `machine` | string | Bei `type="state-machine"` |

<!-- @section id="5" title="@table Marker und Standard-Schemata" type="prose" -->
## §5 @table Marker und Standard-Schemata

### §5.1 Syntax

```
<!-- @table schema="SCHEMA_NAME" [rolle="ROLLE"] [suite="SUITE"] -->
| Spalte1 | Spalte2 | Spalte3 |
|---------|---------|---------|
| Wert1   | Wert2   | Wert3   |
```

### §5.2 Standard-Schemata

| Schema | Spalten | Verwendung |
|--------|---------|-----------|
| `role_permissions` | Erlaubt, Verboten, CHARTER-Ref | Rollenrechte |
| `role_inputs` | Quelle, Daten, Vertrag, Bedingung | Rolleneingänge |
| `role_outputs` | Ziel, Daten, Vertrag, Bedingung | Rollenausgänge |
| `role_rules` | Regel, CHARTER-Ref, Konsequenz | Rollenregeln |
| `safety_rules` | ID, Regel, Kategorie | Sicherheitsregeln |
| `state_machine_states` | Zustand, Bedeutung, Dauer | Zustände |
| `state_transitions` | Von, Nach, Auslöser, Bedingung | Übergänge |
| `test_cases` | Test-ID, Test, Erwartet, CHARTER-Ref, Rolle | Testfälle |
| `test_suite_overview` | Suite, Tests, Status, Zweck | Suiten-Übersicht |
| `error_codes` | Fehler, Bedeutung, Fehlerklasse | Fehlercodes |
| `enum_values` | Wert, Bedeutung | Enum-Werte |
| `config_params` | Parameter, Typ, Default, Besitzer, Beschreibung | Konfiguration |
| `phase_tasks` | Phase, Aufgabe, Dauer, Abhängigkeit | Phasen |
| `acceptance_criteria` | #, Kriterium, Status | Akzeptanz |
| `corrections` | #, Korrektur, Quelle, Status | Korrekturen |
| `document_hierarchy` | Layer, Dateien, Beschreibung | Hierarchie |
| `architecture_decisions` | Thema, Entscheidung, Quelle | Entscheidungen |
| `coverage_targets` | Modul, Mindestabdeckung, Begründung | Coverage |
| `risk_matrix` | #, Risiko, Wahrscheinlichkeit, Auswirkung, Mitigation | Risiken |
| `zone_definitions` | Zone-ID, Beschreibung, Dimensionen, Initialzustand | Zonen |
| `capabilities_overview` | Capability-ID, Slot-ID, Parameter, physical_actuation | Capabilities |
| `parameter_space` | Dimension, Typ, Bereich, Einheit, Beschreibung | Parameterraum |

<!-- @section id="6" title="@ref Marker" type="prose" -->
## §6 @ref Marker

### §6.1 Syntax

```
<!-- @ref target="ZIEL" type="TYP" -->
```

### §6.2 Referenztypen

| Typ | Beschreibung | Beispiel |
|-----|-------------|---------|
| `security-rule` | CHARTER-Sicherheitsregel | `CHARTER §SR-04` |
| `contract` | Datenvertrag | `CONTRACTS §6.10.19` |
| `spec` | Spezifikationsabschnitt | `GREMIUM.md §6.14` |
| `enum` | Enum-Definition | `CONTRACTS §10 NodeType` |
| `role` | Rolle | `role:kartograph` |
| `dataflow` | Datenfluss | `dataflow:ergebnis_rueckfluss` |
| `test` | Testfall | `I-01` |
| `config` | Konfigurationsparameter | `config:divergence_threshold` |

### §6.3 Referenzformate

| Format | Bedeutung | Beispiel |
|--------|-----------|---------|
| `DOKUMENT §ABSCHNITT` | Abschnitt in anderem Dokument | `CONTRACTS §6.10.19` |
| `DOKUMENT §SR-NN` | Sicherheitsregel | `CHARTER §SR-04` |
| `role:ID` | Rolle | `role:kartograph` |
| `dataflow:ID` | Datenfluss | `dataflow:twin_drift` |
| `config:NAME` | Konfigurationsparameter | `config:divergence_threshold` |

<!-- @section id="7" title="@role und @role-ref Marker" type="prose" -->
## §7 @role und @role-ref Marker

### §7.1 @role — Rolle definieren

```
<!-- @role id="ROLLEN_ID" layer="SCHICHT" llm="true|false" [pipeline_stage="N"] -->
```

| Attribut | Typ | Pflicht | Beschreibung |
|----------|-----|---------|-------------|
| `id` | string | ✅ | Eindeutige Rollen-ID |
| `layer` | int | ✅ | Schicht (1–5) |
| `llm` | bool | ✅ | Nutzt LLM |
| `pipeline_stage` | int | Optional | Stufe in der Pipeline |

### §7.2 @role-ref — Rolle referenzieren

```
<!-- @role-ref id="ROLLEN_ID" -->
```

Wird verwendet, um in Fließtext oder Tabellen auf eine Rolle zu verweisen,
ohne sie neu zu definieren.

<!-- @section id="8" title="@contract Marker" type="prose" -->
## §8 @contract Marker

### §8.1 Syntax

```
<!-- @contract name="VERTRAGSNAME" type="TYP" [section="ABSCHNITT"] -->
```

### §8.2 Vertragstypen

| Typ | Beschreibung |
|-----|-------------|
| `pydantic` | Pydantic-v2-Modell |
| `enum` | Enum-Definition |
| `protocol` | Python Protocol/Interface |
| `config` | Konfigurationsmodell |
| `yaml` | YAML-basierte Definition |

<!-- @section id="9" title="@state-machine Marker" type="prose" -->
## §9 @state-machine Marker

### §9.1 Syntax

```
<!-- @state-machine id="MASCHINEN_ID" states="ANZAHL" -->
```

Wird vor Zustandsmaschinen-Definitionen verwendet. Die zugehörigen
Zustände und Übergänge werden mit `@table schema="state_machine_states"`
und `@table schema="state_transitions"` definiert.

<!-- @section id="10" title="@dataflow und @dataflow-step Marker" type="prose" -->
## §10 @dataflow und @dataflow-step Marker

### §10.1 @dataflow Syntax

```
<!-- @dataflow id="DATENFLUSS_ID" trigger="AUSLÖSER" [source_role="ROLLE"] [target_role="ROLLE"] -->
```

| Attribut | Typ | Pflicht | Beschreibung |
|----------|-----|---------|-------------|
| `id` | string | ✅ | Eindeutige Datenfluss-ID |
| `trigger` | string | Optional | Auslösendes Ereignis |
| `source_role` | string | Optional | Start-Rolle |
| `target_role` | string | Optional | Ziel-Rolle |

### §10.2 @dataflow-step Syntax

```
<!-- @dataflow-step order="N" [condition="BEDINGUNG"] -->
```

| Attribut | Typ | Pflicht | Beschreibung |
|----------|-----|---------|-------------|
| `order` | int | ✅ | Reihenfolge (1-basiert) |
| `condition` | string | Optional | Bedingung für diesen Schritt |

<!-- @section id="11" title="@safety-rule Marker" type="prose" -->
## §11 @safety-rule Marker

### §11.1 Syntax

```
<!-- @safety-rule id="SR-NN" category="KATEGORIE" -->
```

| Attribut | Typ | Pflicht | Beschreibung |
|----------|-----|---------|-------------|
| `id` | string | ✅ | Regel-ID (SR-01 bis SR-58) |
| `category` | string | Optional | Kategorie (grundregel, sanitization, capability, shutdown, queue) |

<!-- @section id="12" title="@test Marker" type="prose" -->
## §12 @test Marker

### §12.1 Syntax

```
<!-- @test id="TEST_ID" suite="SUITE" [component="KOMPONENTE"] [charter_ref="SR-NN"] -->
```

| Attribut | Typ | Pflicht | Beschreibung |
|----------|-----|---------|-------------|
| `id` | string | ✅ | Eindeutige Test-ID |
| `suite` | string | ✅ | Suite-Zugehörigkeit |
| `component` | string | Optional | Getestete Komponente |
| `charter_ref` | string | Optional | Bezogene CHARTER-Regel |

<!-- @section id="13" title="Validierungsregeln" type="prose" -->
## §13 Validierungsregeln

Der Parser prüft folgende Regeln:

| ID | Regel | Schwere |
|----|-------|---------|
| V-01 | YAML-Frontmatter vorhanden und gültig | ERROR |
| V-02 | `doc_id` entspricht Dateipfad | ERROR |
| V-03 | Alle Pflichtfelder im Frontmatter vorhanden | ERROR |
| V-04 | Jeder `@section`-Marker hat `id`, `title`, `type` | ERROR |
| V-05 | Jeder `@table`-Marker hat ein bekanntes `schema` | ERROR |
| V-06 | Tabellen haben korrekte Spaltenanzahl für ihr Schema | ERROR |
| V-07 | Jeder `@ref` verweist auf ein existierendes Ziel | WARNING |
| V-08 | Rollen-IDs sind konsistent (definiert ↔ referenziert) | WARNING |
| V-09 | Test-IDs sind eindeutig über alle Dateien | ERROR |
| V-10 | `builds_on` referenziert existierende Dateien | ERROR |
| V-11 | Konflikthierarchie ist konsistent mit Layer-Struktur | ERROR |
| V-12 | Keine zirkulären `builds_on`-Referenzen | ERROR |
| V-13 | `@role`-Marker nur in `role-definition`-Abschnitten | ERROR |
| V-14 | `@dataflow-step` hat `order`-Attribut | ERROR |
| V-15 | Sicherheitsregeln SR-01 bis SR-58 sind eindeutig | ERROR |

<!-- @section id="14" title="Namenskonventionen" type="prose" -->
## §14 Namenskonventionen

| Entität | Format | Beispiel |
|---------|--------|---------|
| Datei-ID | `layer/DATEINAME.md` | `specs/GREMIUM.md` |
| Abschnitts-ID | `N` oder `N.N` oder `N.N.N` | `3.2`, `6.14.4` |
| Rollen-ID | `snake_case` | `kartograph`, `quest_compass` |
| Datenfluss-ID | `snake_case` | `ergebnis_rueckfluss`, `twin_drift` |
| Test-ID | `SUITE-NN` oder `PRÄFIX-NN` | `I-01`, `STRAT-AX-05` |
| Suite-ID | `SUITE` oder `SUITE-KÜRZEL` | `ATLAS-CTR`, `STRAT-KANZ` |
| Sicherheitsregel | `SR-NN` | `SR-04` |
| Vertrag | `PascalCase` | `QuestorErgebnisPaket` |
| Enum | `PascalCase` | `NodeType`, `SecurityMode` |
| Konfiguration | `snake_case` | `divergence_threshold` |
| Fehlercode | `UPPER_SNAKE_CASE` | `COMMAND_INVALID` |
| Zustand | `UPPER_SNAKE_CASE` | `ESTOP_LOCKED` |

<!-- @section id="15" title="Dokumentenhierarchie" type="prose" -->
## §15 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `foundation/` und definiert
das Format für alle anderen Dokumente.

Regel: Änderungen an diesem Dokument erfordern eine Versionsänderung
und eine Überprüfung aller bestehenden Dokumente auf Konformität.

| Rang | Dokument | Autorität |
|------|----------|-----------|
| 1 | `CHARTER.md` | Sicherheitsregeln, Prinzipien |
| 2 | `CONTRACTS.md` | Datenverträge |
| 3 | `SPEC_FORMAT.md` (dieses Dokument) | Dateiformat |
| 4 | `specs/*` | Spezifikationen |
| 5 | `ops/*` | Operationale Dokumente |
| 6 | `views/*` | Generierte Sichten |