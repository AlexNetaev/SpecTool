---
doc_id: foundation/MASTER_INDEX.md
doc_type: format-definition
version: 2.0.0
status: BINDEND
schema_version: spec-format-1.0
layer: foundation
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1-twin.1
  - foundation/SPEC_FORMAT.md@1.0.0
conflict_rule: [CHARTER, CONTRACTS, SPEC_FORMAT, THIS_DOC]
roles_defined: []
roles_referenced: []
dataflows_defined: []
last_modified: 2026-08-21
---

<!-- @section id="0" title="Architektur-Freeze" type="meta" -->
# 🏛️ MASTER INDEX & ARCHITECTURE FREEZE v2.0.0

## §0 Der Anti-Endlosschleifen-Pakt

**Status: 🛑 ARCHITECTURE FROZEN.**

| Feld | Wert |
|------|------|
| Datum | 21. August 2026 |
| System | MYRMEX v2.4.0 + Questor v0.2.3 + HAL v0.2.0 + Strategic Layer v1.0.0 |
| Format | SPEC_FORMAT v1.0.0 |
| Migration | ✅ Abgeschlossen (alle 11 Dokumente migriert) |

Dieses Dokument friert den Scope der Architektur ein.

- Es werden **keine neuen Spezifikations-Features** mehr für v2.4.0 erfunden.
- Unklare Details während der Codierung werden als **"Implementation Detail"** im Code gelöst, nicht durch neue Spec-Patches.
- Jede neue Idee wandert in ein **"Backlog für v3.0.0"**.

<!-- @section id="1" title="Aktive Source-of-Truth Dokumente" type="prose" -->
## §1 Aktive Source-of-Truth Dokumente (Bindend für Code)

Diese Dokumente definieren die exakte Architektur. Widersprüche in
älteren Docs werden ignoriert. Alle Dokumente folgen dem
`SPEC_FORMAT v1.0.0`.

### §1.1 Foundation (Layer 0)

| Dokument | Version | Zweck |
|----------|---------|-------|
| `foundation/CHARTER.md` | 1.0.0 | Verfassung, 58 Sicherheitsregeln, Kernprinzipien |
| `foundation/CONTRACTS.md` | 1.2.1-twin.1 | Alle Pydantic-Datenverträge, Zustandsmaschinen, Enums |
| `foundation/SPEC_FORMAT.md` | 1.0.0 | Dateiformat-Definition für alle Dokumente |
| `foundation/MASTER_INDEX.md` | 2.0.0 | Dieses Dokument |

### §1.2 Spezifikationen (Layer 1)

| Dokument | Version | Zweck |
|----------|---------|-------|
| `specs/GREMIUM.md` | 2.0.0-strat.1 | Pipeline-Mechanik, Atlas-Hybrid, Rollen |
| `specs/GREMIUM_STRATEGY.md` | 1.0.0 | Strategische Steuerung, 4-Achsen, Kanzler/Königin |
| `specs/QUESTOR.md` | 1.1.0-atlas-hyb.1 | Questor-Interna, Zustandsmaschine, Sanitization |
| `specs/HAL.md` | 1.1.0-atlas-hyb.1 | Hardware Abstraction Layer |
| `specs/CAROUSEL_TWIN.md` | 1.1.0-patch.1 | Karussell-MVP Hardware, Digital Twin |

### §1.3 Operationale Dokumente (Layer 2)

| Dokument | Version | Zweck |
|----------|---------|-------|
| `ops/VALIDATION.md` | 1.2.0-strat.1 | Teststrategie, ~711 Tests |
| `ops/VALIDATION_ATLAS.md` | 1.0.0-atlas-hyb.1 | Atlas-Hybrid-Teststrategie, ~120 Tests |
| `ops/ROADMAP.md` | 1.2.0-strat.1 | Implementierungsplan, 50 Phasen |

<!-- @section id="2" title="Archivierte / Deprecated Dokumente" type="prose" -->
## §2 Archivierte / Deprecated Dokumente (NICHT in den Code-Chat laden!)

| Dokument | Status | Grund |
|----------|--------|-------|
| `structure_standalone_v2.3.1.md` | ❌ Veraltet | Enthält alte "Schwarm"-Begriffe |
| `questor_myrmex_integration_addendum_v0.1.md` | ❌ Ersetzt | Ersetzt durch VALIDATION.md |
| `structure_standalone_questor_v0.2.3.md` | ⚠️ Historisch | Nur historisch, bei Konflikt gilt QUESTOR.md |
| `structure_hal_v0.2.0.md` | ⚠️ Historisch | Nur historisch, bei Konflikt gilt HAL.md |
| `GREMIUM_UNIFIED_SPECIFICATION_v1.0.0.md` | ❌ Ersetzt | Ersetzt durch GREMIUM.md + GREMIUM_STRATEGY.md |
| `DIGITAL-TWIN-SEM-1.0.0.md` | ✅ Einarbeitet | Integriert in CONTRACTS.md §6.10.19–20 |
| `CONTRACTS_udpate.md` | ✅ Einarbeitet | Integriert in CONTRACTS.md v1.2.0–1.2.1 |
| `VALIDATION_update.md` | ✅ Einarbeitet | Integriert in VALIDATION.md v1.2.0 |
| `ROADMAP_update.md` | ✅ Einarbeitet | Integriert in ROADMAP.md v1.2.0 |
| `GREMIUM_update.md` | ✅ Einarbeitet | Integriert in GREMIUM.md v2.0.0 |
| `CAROUSEL_TWIN_BLOCKFIX-1.0.0.md` | ✅ Einarbeitet | Integriert in CAROUSEL_TWIN.md v1.1.0 |
| `CAROUSEL_TWIN_REMAINING_FIXES-1.0.0.md` | ✅ Einarbeitet | Integriert in CAROUSEL_TWIN.md v1.1.0 |

<!-- @section id="3" title="Format-Referenz" type="prose" -->
## §3 Format-Referenz

Alle aktiven Dokumente folgen dem `SPEC_FORMAT v1.0.0`.

| Aspekt | Definition |
|--------|-----------|
| Frontmatter | YAML zwischen `---`-Markern mit Pflichtfeldern |
| Abschnitte | `<!-- @section id="..." title="..." type="..." -->` |
| Tabellen | `<!-- @table schema="..." -->` mit Standard-Schemata |
| Querverweise | `<!-- @ref target="..." type="..." -->` |
| Rollen | `<!-- @role id="..." layer="..." llm="..." -->` |
| Verträge | `<!-- @contract name="..." type="..." -->` |
| Zustandsmaschinen | `<!-- @state-machine id="..." states="..." -->` |
| Datenflüsse | `<!-- @dataflow id="..." trigger="..." -->` |
| Sicherheitsregeln | `<!-- @safety-rule id="SR-NN" category="..." -->` |
| Tests | `<!-- @test id="..." suite="..." -->` |

Vollständige Definition: → `foundation/SPEC_FORMAT.md`

<!-- @section id="4" title="Migrationsstatus" type="prose" -->
## §4 Migrationsstatus

| # | Dokument | Status | Datum |
|---|----------|--------|-------|
| 1 | `foundation/CHARTER.md` | ✅ Migriert | 2026-08-21 |
| 2 | `foundation/CONTRACTS.md` | ✅ Migriert | 2026-08-21 |
| 3 | `specs/GREMIUM.md` | ✅ Migriert | 2026-08-21 |
| 4 | `specs/GREMIUM_STRATEGY.md` | ✅ Migriert | 2026-08-21 |
| 5 | `specs/QUESTOR.md` | ✅ Migriert | 2026-08-21 |
| 6 | `specs/HAL.md` | ✅ Migriert | 2026-08-21 |
| 7 | `specs/CAROUSEL_TWIN.md` | ✅ Migriert | 2026-08-21 |
| 8 | `ops/VALIDATION.md` | ✅ Migriert | 2026-08-21 |
| 9 | `ops/VALIDATION_ATLAS.md` | ✅ Migriert | 2026-08-21 |
| 10 | `ops/ROADMAP.md` | ✅ Migriert | 2026-08-21 |
| 11 | `foundation/SPEC_FORMAT.md` | ✅ Erstellt | 2026-08-21 |
| 12 | `foundation/MASTER_INDEX.md` | ✅ Aktualisiert | 2026-08-21 |

**Gesamt: 12/12 Dokumente migriert.**

<!-- @section id="5" title="Regel für die implementierende KI" type="prose" -->
## §5 Regel für die implementierende KI

Wenn du als KI diesen Index liest:

1. **Deine Aufgabe ist es NICHT**, die Spezifikation zu hinterfragen oder zu erweitern.
2. **Deine Aufgabe ist es**, die in den oben genannten Dokumenten definierten Verträge in lauffähigen, getesteten Python-Code (Pydantic v2, pytest) zu übersetzen.
3. **Bei Unklarheiten** in der Spezifikation: Löse sie als "Implementation Detail" im Code. Erfinde keine neuen Spec-Features.
4. **Bei Widersprüchen**: Folge der Konflikthierarchie (CHARTER > CONTRACTS > SPECS > OPS).
5. **Alle Dokumente** folgen dem `SPEC_FORMAT v1.0.0`. Der Parser kann sie maschinell einlesen.

<!-- @section id="6" title="Dokumentenhierarchie" type="prose" -->
## §6 Dokumentenhierarchie

```
foundation/
├── CHARTER.md          ← Oberste Autorität (58 Sicherheitsregeln)
├── CONTRACTS.md        ← Datenverträge (Pydantic-Modelle)
├── SPEC_FORMAT.md      ← Dateiformat-Definition
└── MASTER_INDEX.md     ← Dieses Dokument

specs/
├── GREMIUM.md          ← Pipeline-Mechanik
├── GREMIUM_STRATEGY.md ← Strategische Steuerung
├── QUESTOR.md          ← Questor-Interna
├── HAL.md              ← Hardware Abstraction Layer
└── CAROUSEL_TWIN.md    ← Karussell-MVP

ops/
├── VALIDATION.md       ← Teststrategie
├── VALIDATION_ATLAS.md ← Atlas-Tests
└── ROADMAP.md          ← Implementierungsplan

views/                  ← Generiert (nicht manuell editieren)
├── ROLE_VIEWS.md
├── DATAFLOW_MAP.md
└── TEST_MATRIX.md

patches/                ← Archiviert nach Einarbeitung
archive/                ← Veraltete Dokumente
```

Konfliktregel: `CHARTER` > `CONTRACTS` > `SPEC_FORMAT` > `specs/*` > `ops/*` > `views/*`