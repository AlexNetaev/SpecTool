---
doc_id: specs/GREMIUM.md
doc_type: spec
version: 2.0.0-strat.1
status: BINDEND
schema_version: spec-format-1.0
layer: specs
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1-twin.1
conflict_rule: [CHARTER, CONTRACTS, GREMIUM_STRATEGY, THIS_DOC]
roles_defined:
  - archivar
  - kartograph
  - kanzler
  - vordenker
  - pre_filter
  - lotse
  - quartiermeister
  - richter
  - seher
  - dispatcher
  - receiver
roles_referenced:
  - koenigin
dataflows_defined:
  - ergebnis_rueckfluss
  - ideen_pipeline
  - paket_pipeline
  - twin_drift_detection
  - kalibrierungs_loop
last_modified: 2026-08-21
---

<!-- @section id="0" title="Geltung und Änderungsregeln" type="meta" -->
# 🏛️ GREMIUM — VOLLSTÄNDIGE SPEZIFIKATION

## §0 Geltung und Änderungsregeln

Dieses Dokument definiert die vollständige Gremium-Spezifikation (Schicht 4 im MYRMEX-System).

Regel: Dieses Dokument referenziert Verträge aus `CONTRACTS.md` und Sicherheitsregeln aus `CHARTER.md`.
Es definiert keine neuen Verträge und keine neuen Sicherheitsregeln.

Konfliktregel: Bei Widersprüchen gilt `CHARTER.md` > `CONTRACTS.md` > `GREMIUM_STRATEGY.md` > dieses Dokument.

<!-- @section id="0.1" title="Änderungsantrag ATLAS-HYB-1.0.0" type="change-request" -->
### §0.1 Änderungsantrag ATLAS-HYB-1.0.0 — Atlas-Hybrid-Erweiterung

Dieser Änderungsantrag integriert das Atlas-Hybrid-System in die Gremium-Spezifikation.

Das Atlas-Hybrid-System erweitert den Atlas um:
- Evidence-Semantik
- Qualitäts- und Reproduktionsmetadaten
- Typed Dimensions und ZoneGeometry
- Atlas-Knoten und Atlas-Kanten
- Objective Families für Multi-Objective-Forschung
- DiagnosticResolution
- SafetyConstraints
- ExclusionConstraints
- FrontierCandidates
- ResearchTopics
- ExplorationPolicy
- AtlasHybridConfig

Regeln:
- Dieser Änderungsantrag definiert keine neuen Datenverträge. Alle Datenverträge kommen aus `CONTRACTS.md §6.10`.
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln.
- Questor erhält keine Schreibrechte in Atlas oder Archiv.
- HAL erhält keine wissenschaftliche Interpretation.
- Die bestehende CHARTER-Hierarchie bleibt unberührt.

<!-- @section id="0.2" title="Beziehung zu GREMIUM_STRATEGY.md" type="change-request" -->
### §0.2 Beziehung zu GREMIUM_STRATEGY.md

Dieses Dokument definiert die Pipeline-Mechanik des Gremiums:
- 9-Stufen-Pipeline
- Sicherheitsrat (Richter, Seher, Circuit-Breaker)
- Pipeline-Orchestrator (Bounded Queues, Deadlock-Erkennung)
- Atlas-Hybrid-System (Energiekonten, Kristallisation, Fractures, FrontierEngine)
- Event-Driven Architecture

`specs/GREMIUM_STRATEGY.md` definiert die strategische Steuerung:
- Kanzler & Königin (Briefing-Zyklus, StrategicDirective)
- 4-Achsen-Architektur (Safety, Resource, Research, Governance)
- ControlState und atomare Transitionen (SL-AX-ATOMIC)
- Intent-Verfügbarkeit und Blocklists
- Closure-Regeln (CT-1..CT-10)
- Symptom-Trigger und Vordenker-Ansteuerung

Konfliktregel zwischen beiden Dokumenten:
CHARTER > CONTRACTS > GREMIUM_STRATEGY.md > GREMIUM.md

Bei Konflikten in der Pipeline-Mechanik: GREMIUM.md ist autoritativ.
Bei Konflikten in der Strategie/Achsen-Steuerung: GREMIUM_STRATEGY.md ist autoritativ.

<!-- @section id="1" title="Gremium-Übersicht und Grundprinzipien" type="prose" -->
## §1 Gremium-Übersicht und Grundprinzipien

<!-- @section id="1.1" title="Position im System" type="prose" -->
### §1.1 Position im System

Das Gremium ist Schicht 4 im MYRMEX-System (→ CHARTER §1.1).

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHICHT 5: 👑 KÖNIGIN                        │
│  Langfristige Vision, Meta-Ziele, menschliche Führung           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    SCHICHT 4: 🏛️ GREMIUM                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  STRATEGISCHE STEUERUNG (→ GREMIUM_STRATEGY.md)          │   │
│  │  Kanzler · Briefing · 4-Achsen · ControlState · DTT      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  PIPELINE-MECHANIK (→ dieses Dokument)                   │   │
│  │  9-Stufen-Pipeline · Sicherheitsrat · Orchestrator        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ATLAS-HYBRID-SYSTEM                                     │   │
│  │  Evidence-Semantik · Energiekonten · Kristallisation      │   │
│  │  FrontierEngine · ResearchTopics · ExplorationPolicy      │   │
│  │  Digital-Twin-Loop (§6.14)                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│              SCHICHT 3: ⚖️ DISPATCH-KOORDINATION                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│              SCHICHT 2: 🧭 QUESTOR                               │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│              SCHICHT 1: 🔌 HAL & RESOURCE GOVERNOR               │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│              SCHICHT 0: ⚙️ PHYSIS / COMPUTE                      │
└─────────────────────────────────────────────────────────────────┘
```

<!-- @section id="1.2" title="Die sechs Gremium-Grundprinzipien" type="prose" -->
### §1.2 Die sechs Gremium-Grundprinzipien

<!-- @table schema="core_principles" -->
| # | Prinzip | Bedeutung | CHARTER-Referenz |
|---|---------|-----------|-----------------|
| 1 | Blackboard-Pattern | Alle Ränge des Gremiums kommunizieren ausschließlich über Atlas und Archiv. Keine direkten Aufrufe zwischen Rängen. | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §2 |
| 2 | Menschliche Königin wird niemals überstimmt | Bei Konflikt zwischen menschlicher und LLM-Königin gewinnt die menschliche Weisung. Nach 2 Konflikten fällt die LLM-Königin auf menschliche Entscheidung zurück. | <!-- @ref target="CHARTER §SR-11" type="security-rule" -->CHARTER §SR-11 |
| 3 | Fail-Closed | Wenn etwas nicht sicher geprüft werden kann: keine Freigabe, keine physische Ausführung, kontrollierter Abbruch oder Eskalation. | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->CHARTER §SR-10 |
| 4 | Seher schreibt niemals 🟥 | Der Seher (LLM-Komponente) darf niemals direkt rote Signale schreiben. Rote Signale dürfen nur durch deterministische Komponenten oder nach Sicherheitsprüfung entstehen. | <!-- @ref target="CHARTER §SR-13" type="security-rule" -->CHARTER §SR-13 |
| 5 | Operational ≠ Scientific | Operationale Fehler erzeugen keine wissenschaftlichen Signale. | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| 6 | Questor ist kein Gremium-Rang | Questor darf nicht in Atlas oder Archiv schreiben. | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |

<!-- @section id="1.3" title="Was das Gremium DARF" type="prose" -->
### §1.3 Was das Gremium DARF

<!-- @table schema="role_permissions" role="gremium" -->
| Erlaubt | Begründung |
|---------|-----------|
| Atlas und Archiv verwalten | Kernaufgabe des Gremiums |
| Ideen generieren und bewerten | Stufe 4–5b der Pipeline |
| Pakete bauen | Stufe 6 der Pipeline |
| Sicherheits-Gates durchführen | Stufe 7 der Pipeline |
| Dispatch koordinieren | Stufe 8 der Pipeline |
| Ergebnisse von Questor empfangen und verarbeiten | Stufe 1 der Pipeline |
| Kristalle und Signale schreiben | Aus validierten wissenschaftlichen Ergebnissen |
| Operational-Logs schreiben | Für Nachvollziehbarkeit |

<!-- @section id="1.4" title="Was das Gremium NICHT DARF" type="prose" -->
### §1.4 Was das Gremium NICHT DARF

<!-- @table schema="role_permissions" role="gremium" -->
| Verboten | CHARTER-Referenz |
|----------|-----------------|
| QuestorBlackbox lesen | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |
| Questor-interne Trails interpretieren | — |
| Wissenschaftliche Signale aus operationalen Fehlern erzeugen | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| ESTOP zurücksetzen | <!-- @ref target="CHARTER §SR-05" type="security-rule" -->CHARTER §SR-05 |
| Leases vergeben | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| Hardware direkt ansprechen | <!-- @ref target="CHARTER §SR-12" type="security-rule" -->CHARTER §SR-12 |
| Menschliche Königin überstimmen | <!-- @ref target="CHARTER §SR-11" type="security-rule" -->CHARTER §SR-11 |

<!-- @section id="2" title="Die 9-Stufen-Pipeline" type="prose" -->
## §2 Die 9-Stufen-Pipeline

<!-- @section id="2.1" title="Übersicht" type="prose" -->
### §2.1 Übersicht

Die Pipeline verarbeitet wissenschaftliche Ideen von der Entstehung bis zur Ausführung:

<!-- @table schema="pipeline_stages" -->
| Stufe | Name | Verantwortlich | Beschreibung |
|-------|------|----------------|--------------|
| 1 | Wissens-Aufnahme | <!-- @role-ref id="archivar" -->Archivar | Empfängt `questor_ergebnis_paket`, schreibt Kristalle und Signale |
| 2 | Atlas-Strukturierung | <!-- @role-ref id="kartograph" -->Kartograph | Strukturiert Wissen in Zonen, Cluster, Signale |
| 3 | Strategische Review | <!-- @role-ref id="kanzler" -->Kanzler ↔ Königin | Langfristige Ausrichtung, Realitäts-Check |
| 4 | Ideen-Generierung | <!-- @role-ref id="vordenker" -->Vordenker | Erzeugt Roh-Ideen aus Atlas-Mustern |
| 5a | Pre-Filter | Deterministischer Fast-Path | Filtert offensichtliche Probleme |
| 5b | Ideen-Erdung | <!-- @role-ref id="lotse" -->Lotse | Platziert Wegmarken im Atlas |
| 6 | Paket-Bau | <!-- @role-ref id="quartiermeister" -->Quartiermeister | Baut `ResearchPackage` aus Wegmarke |
| 7 | Sicherheits-Gate | <!-- @role-ref id="richter" -->Richter + <!-- @role-ref id="seher" -->Seher | Sicherheitsprüfung |
| 8 | Dispatch & Execution | <!-- @role-ref id="dispatcher" -->Dispatcher → Questor → <!-- @role-ref id="receiver" -->Receiver | Ausführung über `QuestorDispatchEnvelope` |

<!-- @section id="2.2" title="Datenfluss zwischen den Stufen" type="dataflow" dataflow="ergebnis_rueckfluss" -->
### §2.2 Datenfluss zwischen den Stufen

<!-- @dataflow id="ergebnis_rueckfluss" trigger="QUESTOR_COMPLETED" source_role="receiver" target_role="archivar" -->
```
Stufe 1 ← Stufe 8 (Ergebnis-Rückfluss)
  ↓
Stufe 2
  ↓
Stufe 3
  ↓
Stufe 4
  ↓
Stufe 5a → 5b
  ↓
Stufe 6
  ↓
Stufe 7
  ↓
Stufe 8
```

<!-- @section id="2.3" title="Der vollständige Datenfluss" type="prose" -->
### §2.3 Der vollständige Datenfluss

```
┌─────────────────────────────────────────────────────────────────┐
│                    IDEEN-PIPELINE (Stufen 4, 5a, 5b)             │
│                                                                   │
│  Vordenker → Pre-Filter → Lotse                                 │
│  (RohIdee)   (deterministisch)  (Wegmarke im Atlas)             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    PAKET-PIPELINE (Stufen 6, 7, 8)               │
│                                                                   │
│  Quartiermeister → Sicherheits-Gate → Dispatcher                 │
│  (ResearchPackage)  (Richter + Seher)  (QuestorDispatchEnvelope) │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    QUESTOR-ANBINDUNG                              │
│                                                                   │
│  QuestorDispatchEnvelope → Questor → questor_ergebnis_paket      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    WISSENS-PIPELINE (Stufen 1, 2)                │
│                                                                   │
│  Archivar → Kartograph → Atlas                                   │
│  (Kristalle, Signale)  (Zonen, Cluster, fracture_score)          │
└─────────────────────────────────────────────────────────────────┘
```

<!-- @section id="3" title="Gremium-Komponenten" type="prose" -->
## §3 Gremium-Komponenten

<!-- @section id="3.1" title="Archivar (Stufe 1)" type="role-definition" role="archivar" -->
<!-- @role id="archivar" layer="4" llm="false" pipeline_stage="1" writes_to="archiv" reads_from="questor_ergebnis_paket" -->
### §3.1 Archivar (Stufe 1)

Verantwortung: Empfängt `questor_ergebnis_paket` von Questor und verarbeitet es.

<!-- @table schema="role_permissions" role="archivar" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| `questor_ergebnis_paket` empfangen | QuestorBlackbox lesen | SR-07 |
| Kristalle und Signale an Kartograph übergeben | Wissenschaftliche Signale aus operationalen Fehlern erzeugen | SR-08 |
| SAFETY-Governance-Ereignisse protokollieren | Questor-interne Trails interpretieren | — |
| `operational_metrics` in `operational_event_log` übernehmen | Atlas-Zustände eigenmächtig ändern | SR-04 |

<!-- @table schema="role_inputs" role="archivar" -->
| Quelle | Daten | Vertrag | Bedingung |
|--------|-------|---------|-----------|
| Receiver (Stufe 8) | `questor_ergebnis_paket` | CONTRACTS §2.1 | Immer nach Paketverarbeitung |

<!-- @table schema="role_outputs" role="archivar" -->
| Ziel | Daten | Vertrag | Bedingung |
|------|-------|---------|-----------|
| Kartograph (Stufe 2) | Kristallkandidaten + Signale | CONTRACTS §5.5, §5.6 | Immer |
| Operational-Log | `operational_event_log` | — | Bei operationalen Ereignissen |
| Sicherheits-Governance | SAFETY-Governance-Ereignis | — | Bei SAFETY-Abbruch |

<!-- @table schema="role_rules" role="archivar" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Prüft `idempotency_key` | SR-54 | Duplikat wird verworfen |
| Prüft `sequence_number` pro `questor_instance_id` | SR-20 | Rückläufige Sequence wird abgelehnt |
| Prüft `vollstaendig_flag` | SR-20 | Unvollständiges Ergebnis wird nicht verarbeitet |
| Trennt `abbruch_klasse` | SR-08 | OPERATIONAL → kein wissenschaftliches Signal |
| Bei SAFETY: keine Kristalle/Signale aus Questor-Ergebnis | SR-19 | Kristalle und Signale bleiben leer |
| Liest keine QuestorBlackbox | SR-07 | Zugriff verweigert |

Atlas-Hybrid-Sonderregeln:
- Wenn `kristall_kandidaten` vorhanden sind, übergibt der Archivar sie zusammen mit: `expectation_ref`, `confirms_expectation`, `evidence_class`, `metric_vector`, `evidence_quality`, `reproducibility_ref` sofern vorhanden.
- Wenn `signale_fuer_atlas` vorhanden sind, übergibt der Archivar sie zusammen mit: `evidence_kind`, `evidence_class`, `expectation_ref`, `observation_direction`, `is_diagnostic`, `is_policy`, `quality`, `validity`, `physical_time_s`, `node_ref` sofern vorhanden.
- Wenn `abbruch_klasse = OPERATIONAL`, dürfen keine wissenschaftlichen Atlas-Ereignisse erzeugt werden.
- Wenn `abbruch_klasse = SAFETY`, dürfen keine wissenschaftlichen Kristalle oder Signale aus dem Questor-Ergebnis erzeugt werden.

<!-- @section id="3.2" title="Kartograph (Stufe 2)" type="role-definition" role="kartograph" -->
<!-- @role id="kartograph" layer="4" llm="false" pipeline_stage="2" writes_to="atlas" reads_from="archivar" -->
### §3.2 Kartograph (Stufe 2)

Verantwortung: Strukturiert das Wissen im Atlas und führt das Atlas-Hybrid-System.

<!-- @table schema="role_permissions" role="kartograph" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Atlas schreiben (Zonen, Knoten, Kanten, Energiekonten) | QuestorBlackbox lesen | SR-07 |
| Signale strukturieren | ESTOP zurücksetzen | SR-05 |
| FrontierCandidates aktualisieren | Eigenmächtige Aufhebung von SafetyConstraints | — |
| TwinDivergenceReport berechnen | LLM-Endentscheidung über Atlas-Zustände | SR-13 |
| DIGITAL_TWIN-Knoten aktualisieren | Eigenmächtige Auflösung von Quarantäne ohne DiagnosticResolution | — |
| SymptomEvent(TWIN_DRIFT) erzeugen | Wissenschaftliche Interpretation von operationalen Fehlern | SR-08 |

<!-- @table schema="role_inputs" role="kartograph" -->
| Quelle | Daten | Vertrag | Bedingung |
|--------|-------|---------|-----------|
| Archivar (Stufe 1) | Kristallkandidaten + Signale | CONTRACTS §5.5, §5.6 | Immer nach Paketverarbeitung |
| Archivar (Stufe 1) | TwinDivergence-Referenzen | CONTRACTS §6.10.20 | Bei Sim/Real-Paarung |
| FrontierEngine | Zone-Update-Anfragen | CONTRACTS §6.10.14 | Nach jeder Atlas-Änderung |

<!-- @table schema="role_outputs" role="kartograph" -->
| Ziel | Daten | Vertrag | Bedingung |
|------|-------|---------|-----------|
| Atlas | Zone-Health-Updates | CONTRACTS §6.10.7 | Immer |
| Atlas | AtlasNode / AtlasEdge | CONTRACTS §6.10.8, §6.10.9 | Bei neuen Kristallen/Hypothesen |
| Atlas | TwinDivergenceReport | CONTRACTS §6.10.20 | Bei tolerance_breached |
| Strategic Layer | SymptomEvent(TWIN_DRIFT) | CONTRACTS §6.11.9 | Bei Drift-Erkennung |
| FrontierEngine | Frontier-Update-Trigger | CONTRACTS §6.10.14 | Nach jeder Änderung |

<!-- @table schema="role_rules" role="kartograph" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Keine Evidenz löschen | SR-17 | Append-Only-Verletzung |
| Keine Kante ohne evidence_refs | — | Ungültige Atlas-Kante |
| EXPLAINS erfordert review_authority | SR-13 | Validierungsfehler |
| Sim bestätigt keinen Real-Kristall | SR-08 | Kristallisation blockiert |
| LOCKED überschreibt Frontier | — | Keine normale Exploration |
| Bestimmt Zone/Subzone für jedes Signal | — | Deterministische Zuordnung |
| Darf keine Kante ohne evidence_refs erzeugen | — | Ungültige Kante |

Digital-Twin-Pflichten:
- Vergleicht Sim-Kristalle mit Real-Kristallen (gleicher `digital_twin_ref`)
- Berechnet TwinDivergenceReport deterministisch
- Aktualisiert `drift_score` des DIGITAL_TWIN-Knotens
- Erzeugt SymptomEvent(TWIN_DRIFT) bei `tolerance_breached`
- Verarbeitet DiagnosticResolution mit `outcome = TWIN_CALIBRATED`
- Markiert DIGITAL_TWIN-Knoten als DEGRADED bei `drift_score > threshold`
- Prüft ValidityWindow des Twin-Modells

<!-- @section id="3.3" title="Kanzler (Stufe 3)" type="role-definition" role="kanzler" -->
<!-- @role id="kanzler" layer="4" llm="false" pipeline_stage="3" writes_to="governance" reads_from="atlas" -->
### §3.3 Kanzler (Stufe 3)

Verantwortung: Strategische Review und Realitäts-Check.

<!-- @table schema="role_permissions" role="kanzler" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Lagebericht erstellen | QuestorBlackbox lesen | SR-07 |
| SAFE_MODE verwalten | Menschliche Königin überstimmen | SR-11 |
| Policy-Veto-Review durchführen | Sicherheitsfreigaben durch LLM ersetzen | SR-13 |
| ExplorationPolicy setzen/bestätigen | — | — |
| SafetyConstraints bestätigen/aufheben (autorisiert) | — | — |
| ResearchTopic priorisieren/blockieren/archivieren | — | — |
| Zonen manuell auf LOCKED setzen | — | — |

<!-- @table schema="role_inputs" role="kanzler" -->
| Quelle | Daten | Vertrag | Bedingung |
|--------|-------|---------|-----------|
| Kartograph (Stufe 2) | Atlas-Zustand | CONTRACTS §6.10.7 | Immer |
| Strategic Layer | StrategicBriefing | CONTRACTS §6.11.4 | Periodisch |
| Menschliche Königin | Weisungen | — | Bei Konflikten |

<!-- @table schema="role_outputs" role="kanzler" -->
| Ziel | Daten | Vertrag | Bedingung |
|------|-------|---------|-----------|
| Königin | Lagebericht | — | Periodisch |
| ExplorationPolicy | Policy-Update | CONTRACTS §6.10.17 | Bei Änderung |
| Vordenker | SymptomEvents | CONTRACTS §6.11.9 | Bei Trigger |

<!-- @table schema="role_rules" role="kanzler" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Keine Sicherheitsfreigaben durch LLM ersetzen | SR-13 | VETO |
| Menschliche Königin nicht überstimmen | SR-11 | Weisung wird zurückgesetzt |
| Keine QuestorBlackbox lesen | SR-07 | Zugriff verweigert |

<!-- @section id="3.4" title="Vordenker (Stufe 4)" type="role-definition" role="vordenker" -->
<!-- @role id="vordenker" layer="4" llm="true" pipeline_stage="4" writes_to="ideen" reads_from="atlas" -->
### §3.4 Vordenker (Stufe 4)

Verantwortung: Erzeugt Roh-Ideen aus Atlas-Mustern.

<!-- @table schema="role_permissions" role="vordenker" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Atlas-Muster analysieren | Wegmarken direkt platzieren | — |
| Roh-Ideen generieren | Sicherheitsfreigaben erteilen | SR-13 |
| FrontierCandidates als Quelle nutzen | FrontierCandidates als ausführbar markieren | — |
| SymptomEvents empfangen | Direkt in Atlas schreiben | SR-04 |

<!-- @table schema="role_inputs" role="vordenker" -->
| Quelle | Daten | Vertrag | Bedingung |
|--------|-------|---------|-----------|
| Kartograph (Stufe 2) | SymptomEvents | CONTRACTS §6.11.9 | Bei Trigger |
| FrontierEngine | FrontierCandidates | CONTRACTS §6.10.14 | Nach Atlas-Änderung |
| Atlas | Zone-Health, uncertainty_score | CONTRACTS §6.10.7 | Immer |

<!-- @table schema="role_outputs" role="vordenker" -->
| Ziel | Daten | Vertrag | Bedingung |
|------|-------|---------|-----------|
| Pre-Filter (Stufe 5a) | RohIdee + prozess_skizze | — | Immer |
| Hypothesen-Archiv | ScientificHypothesis | CONTRACTS §6.11.9 | Bei neuer Hypothese |

<!-- @table schema="role_rules" role="vordenker" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Liefert prozess_skizze mit jeder Idee | — | Idee wird verworfen |
| Nutzt FrontierCandidates als Quelle | — | — |
| Erwartungsreferenz bei Hypothese-Tests | — | Fail-Closed |

Digital-Twin-Pflichten:
- Erhält SymptomEvent(TWIN_DRIFT) bei Modell-Drift
- Schlägt Kalibrierungs-Hypothesen vor
- Nutzt TwinStatusSummary im Briefing für Drift-Erkennung
- Liefert Schatten-Variablen-Check bei TWIN_DRIFT

<!-- @section id="3.5" title="Pre-Filter (Stufe 5a)" type="role-definition" role="pre_filter" -->
<!-- @role id="pre_filter" layer="4" llm="false" pipeline_stage="5a" writes_to="ideen" reads_from="atlas" -->
### §3.5 Pre-Filter (Stufe 5a)

Verantwortung: Deterministischer Fast-Path für offensichtliche Probleme.

<!-- @table schema="role_permissions" role="pre_filter" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Dimension-Freigabe prüfen | LLM-Endentscheidung treffen | SR-13 |
| Quarantäne-Zonen prüfen | Sicherheitsfreigaben ersetzen | SR-13 |
| Sättigungs-Zustände prüfen | Wegmarke platzieren | — |
| SafetyConstraints prüfen | — | — |

<!-- @table schema="role_rules" role="pre_filter" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Dimension nicht freigegeben → Idee verwerfen | — | Fail-Closed |
| Zone LOCKED → Idee verwerfen | — | Fail-Closed |
| full_rebuild_required → Idee verwerfen (außer Recovery/Diagnose) | — | Fail-Closed |
| Aktive harte SafetyConstraint → Idee verwerfen | — | Fail-Closed |
| Diagnose-Idee ohne Diagnose-Budget → Idee verwerfen | — | Fail-Closed |
| VALIDATE/DIAGNOSE ohne Erwartungsreferenz → Idee verwerfen oder auf EXPLORE reduzieren | — | Fail-Closed |

<!-- @section id="3.6" title="Lotse (Stufe 5b)" type="role-definition" role="lotse" -->
<!-- @role id="lotse" layer="4" llm="false" pipeline_stage="5b" writes_to="atlas" reads_from="atlas" -->
### §3.6 Lotse (Stufe 5b)

Verantwortung: Ideen-Erdung und Wegmarken-Platzierung.

<!-- @table schema="role_permissions" role="lotse" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Wegmarken im Atlas platzieren | Sicherheitsfreigaben erteilen | SR-13 |
| frontier_candidate_ref setzen | Pakete bauen | — |
| atlas_expectation_ref setzen | Quarantäne eigenmächtig aufheben | — |
| Diagnose-Wegmarken setzen | Wegmarke in gesperrter Frontier platzieren | — |

<!-- @table schema="role_rules" role="lotse" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Nur in Weißraum oder bestätigten grünen Zonen | — | Wegmarke wird verworfen |
| Diagnose-Wegmarken nur bei vorhandenem Diagnose-Budget | — | Wegmarke wird verworfen |
| Vermeidet LOCKED-Zonen | — | Wegmarke wird verworfen |
| Vermeidet aktive harte SafetyConstraint-Regionen | — | Wegmarke wird verworfen |
| Vermeidet ExclusionConstraint-Regionen mit hard_limit=true | — | Wegmarke wird verworfen |

<!-- @section id="3.7" title="Quartiermeister (Stufe 6)" type="role-definition" role="quartiermeister" -->
<!-- @role id="quartiermeister" layer="4" llm="false" pipeline_stage="6" writes_to="pakete" reads_from="atlas" -->
### §3.7 Quartiermeister (Stufe 6)

Verantwortung: Baut `ResearchPackage` aus Wegmarke.

<!-- @table schema="role_permissions" role="quartiermeister" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| ResearchPackage bauen | Gate-Freigaben vorwegnehmen | SR-39 |
| questor_spec setzen | Leases vergeben | SR-06 |
| planning_hints setzen | Sicherheitsfreigaben ersetzen | SR-13 |
| Atlas-Hybrid-Referenzen setzen | Atlas-Zustände eigenmächtig ändern | SR-04 |

<!-- @table schema="role_inputs" role="quartiermeister" -->
| Quelle | Daten | Vertrag | Bedingung |
|--------|-------|---------|-----------|
| Lotse (Stufe 5b) | Wegmarke | CONTRACTS §6.10.15 | Immer |
| FrontierEngine | ResourceContext | CONTRACTS §6.10.14 | Bei Frontier-Wegmarke |
| Atlas | SafetyConstraints, ExclusionConstraints | CONTRACTS §6.10.12, §6.10.13 | Immer |

<!-- @table schema="role_outputs" role="quartiermeister" -->
| Ziel | Daten | Vertrag | Bedingung |
|------|-------|---------|-----------|
| Sicherheitsrat (Stufe 7) | ResearchPackage | CONTRACTS §1.1 | Immer |

<!-- @table schema="role_rules" role="quartiermeister" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Setzt atlas_expectation_ref bei Hypothese-Tests | — | Fail-Closed |
| Setzt objective_family_ref bei Multi-Objective | — | — |
| Setzt frontier_candidate_ref bei Frontier-Wegmarke | — | — |
| autonomy_level = STRICT bei Diagnose/Quarantäne/FRACTURE_DIAGNOSIS | — | Fail-Closed |
| Berücksichtigt ResourceContext aus FrontierCandidates | — | — |
| Berücksichtigt ExclusionConstraint und SafetyConstraint | — | Fail-Closed |

<!-- @section id="4" title="Sicherheitsrat (Stufe 7)" type="prose" -->
## §4 Sicherheitsrat (Stufe 7)

<!-- @section id="4.1" title="Übersicht" type="prose" -->
### §4.1 Übersicht

Der Sicherheitsrat besteht aus:
- Richter (deterministisch)
- Seher (LLM)
- Circuit-Breaker (Zustandsmaschine)
- Appeal (Berufung)
- Policy-Veto-Review (Audit)

<!-- @section id="4.2" title="Richter (deterministisch)" type="role-definition" role="richter" -->
<!-- @role id="richter" layer="4" llm="false" pipeline_stage="7" writes_to="gate_records" reads_from="pakete" -->
### §4.2 Richter (deterministisch)

Verantwortung: Regelprüfung, Policy-Enforcement, Fail-Closed.

<!-- @table schema="role_rules" role="richter" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Prüft deterministisch gegen definierte Regeln | — | FAIL bei Regelverletzung |
| Fail-Closed: Wenn Regel nicht sicher prüfbar → FAIL | SR-10 | FAIL |

<!-- @section id="4.3" title="Seher (LLM)" type="role-definition" role="seher" -->
<!-- @role id="seher" layer="4" llm="true" pipeline_stage="7" writes_to="gate_records" reads_from="pakete" -->
### §4.3 Seher (LLM)

Verantwortung: Evidenz-Bewertung.

<!-- @table schema="role_permissions" role="seher" -->
| Erlaubt | Verboten | CHARTER-Ref |
|---------|----------|-------------|
| Evidenz bewerten | Direkt 🟥 schreiben | SR-13 |
| PASS, VETO, TEMP_SUSPENDED zurückgeben | Veto ohne Evidenz | SR-13 |

<!-- @table schema="role_rules" role="seher" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Veto nur mit Evidenz | SR-13 | SEHER_INVALID_VETO |
| Schreibt niemals direkt 🟥 | SR-13 | VETO wird ignoriert |

<!-- @section id="4.4" title="Circuit-Breaker" type="prose" -->
### §4.4 Circuit-Breaker (Zustandsmaschine)

<!-- @table schema="state_machine_states" machine="circuit_breaker" -->
| Zustand | Bedeutung |
|---------|-----------|
| NORMAL | Seher arbeitet normal |
| SHADOW_MODE | Seher wird überwacht, Entscheidungen nicht direkt umgesetzt |
| TEMP_SUSPENDED | Seher ist temporär suspendiert |
| PERMANENT_SUSPENDED | Seher ist permanent suspendiert (nur manuelle Rückkehr) |

<!-- @section id="4.5" title="Appeal (Berufung)" type="prose" -->
### §4.5 Appeal (Berufung)

Ablauf:
1. Richter gibt `PASS`
2. Seher gibt `VETO`
3. Appeal wird ausgelöst
4. Kanzler prüft den Appeal
5. Appeal wird `GRANTED` oder `DENIED`

<!-- @section id="4.6" title="Policy-Veto-Review" type="prose" -->
### §4.6 Policy-Veto-Review

Konfigurationsparameter: `policy_veto_review_interval_cycles = 20` (Wertebereich: 1–500, Default: 20)

<!-- @section id="4.7" title="Gate-Zustandsmaschine" type="state-machine" machine="gate_state" -->
### §4.7 Gate-Zustandsmaschine

<!-- @table schema="state_transitions" machine="gate_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| GATE_PENDING | RICHTER_PRUEFT | Start |
| RICHTER_PRUEFT | ABGELEHNT | Richter FAIL |
| RICHTER_PRUEFT | SEHER_PRUEFT | Richter PASS |
| SEHER_PRUEFT | FREIGEGEBEN | Seher PASS |
| SEHER_PRUEFT | DISPUTED | Seher VETO (startet Appeal) |
| DISPUTED | FREIGEGEBEN | Appeal GRANTED |
| DISPUTED | ABGELEHNT | Appeal DENIED |

<!-- @section id="5" title="Pipeline-Orchestrator" type="prose" -->
## §5 Pipeline-Orchestrator

<!-- @section id="5.1" title="Verantwortung" type="prose" -->
### §5.1 Verantwortung

Der Pipeline-Orchestrator koordiniert die Stufen-Übergänge und verwaltet die Bounded Queues.

<!-- @section id="5.2" title="Bounded Queues mit Watermarks" type="prose" -->
### §5.2 Bounded Queues mit Watermarks

Jede Pipeline-Stufe hat eine begrenzte Queue:
- `max_size`: maximale Größe
- `high_watermark`: Warnschwelle (z.B. 80%)
- `low_watermark`: Entwarnung (z.B. 50%)

<!-- @section id="5.3" title="Deadlock-Erkennung" type="prose" -->
### §5.3 Deadlock-Erkennung

Erkennung:
- Zyklische Abhängigkeiten zwischen Queues
- Timeouts bei State-Transitions
- Blockierte Leases ohne Fortschritt

Behandlung:
- Notventil-Zyklen initiieren
- Pakete in vorherige Stufe zurücksetzen
- Circuit-Breaker für betroffene Komponenten

<!-- @section id="5.4" title="Notventil-Zyklen" type="prose" -->
### §5.4 Notventil-Zyklen

Bei Deadlock oder kritischem Fehler:
1. Alle aktiven Transaktionen stoppen
2. Pakete in sichere Zustände zurücksetzen
3. Leases freigeben oder suspendieren
4. SAFE_MODE aktivieren (falls nötig)
5. Menschliche Königin benachrichtigen

<!-- @section id="6" title="Atlas-Hybrid-System" type="prose" -->
## §6 Atlas-Hybrid-System

<!-- @section id="6.1" title="Zweck" type="prose" -->
### §6.1 Zweck

Der Atlas ist die wissenschaftliche Landkarte des Gremiums. Er dient nicht nur der Ablage von Wissen, sondern ermöglicht:
- wissenschaftliche Orientierung,
- Erkennung von Wissenslücken,
- Bewertung von Widersprüchen,
- Isolation instabiler Wissensbereiche,
- gezielte Diagnose,
- autonome Auswahl sinnvoller nächster Forschungsschritte.

Regeln:
- Questor schreibt nicht in den Atlas (→ CHARTER §SR-04)
- HAL schreibt nicht in den Atlas
- LLM-Komponenten dürfen beraten, aber nicht final über Atlas-Zustände entscheiden
- Operationale Fehler erzeugen keine wissenschaftlichen Signale (→ CHARTER §SR-08)
- Bei SAFETY-Abbruch sind Kristalle und Signale aus Questor leer (→ CHARTER §SR-19)
- Fail-Closed gilt bei allen unklaren Atlas-Zuständen (→ CHARTER §SR-10)

<!-- @section id="6.2" title="Referenzen" type="prose" -->
### §6.2 Referenzen

Dieser Abschnitt referenziert folgende Verträge:
- `CONTRACTS §6.10.1` EvidenceQuality
- `CONTRACTS §6.10.2` ValidityWindow
- `CONTRACTS §6.10.3` ReproducibilityContext
- `CONTRACTS §6.10.4` TypedDimension
- `CONTRACTS §6.10.5` ConditionalRule
- `CONTRACTS §6.10.6` ZoneGeometry
- `CONTRACTS §6.10.7` AtlasZoneSummary
- `CONTRACTS §6.10.8` AtlasNode
- `CONTRACTS §6.10.9` AtlasEdge
- `CONTRACTS §6.10.10` ObjectiveFamily
- `CONTRACTS §6.10.11` DiagnosticResolution
- `CONTRACTS §6.10.12` SafetyConstraint
- `CONTRACTS §6.10.13` ExclusionConstraint
- `CONTRACTS §6.10.14` FrontierCandidate
- `CONTRACTS §6.10.15` DiagnosticWaypoint
- `CONTRACTS §6.10.16` ResearchTopic
- `CONTRACTS §6.10.17` ExplorationPolicy
- `CONTRACTS §6.10.18` AtlasHybridConfig
- `CONTRACTS §6.10.19` DigitalTwinModel
- `CONTRACTS §6.10.20` TwinDivergenceReport

<!-- @section id="6.3" title="Topologie" type="prose" -->
### §6.3 Topologie

Der Atlas besteht aus: Dimensionen, Zonen, Subzonen, Knoten, Kanten, Clustern.

<!-- @section id="6.4" title="Evidence-Semantik" type="prose" -->
### §6.4 Evidence-Semantik

<!-- @table schema="signal_semantics" -->
| Signal | evidence_kind / Behandlung | Energiekonto |
|--------|---------------------------|--------------|
| 🟩 | CONFIRMATION | support_energy |
| ⬜ | EXPLORATORY_COVERAGE | coverage_energy |
| 🟨 | CONTRADICTION | conflict_energy |
| 🟪 diagnostic | DIAGNOSTIC_CLARIFICATION | diagnostic_energy |
| 🟪 policy | POLICY_BLOCK | policy_energy |
| 🟥 | Sicherheits-Governance + optional conflict_energy | zusätzlich SafetyConstraint prüfen |

<!-- @section id="6.5" title="Energiekonten und Scores" type="prose" -->
### §6.5 Energiekonten und Scores

<!-- @table schema="energy_accounts" -->
| Konto | Formel |
|-------|--------|
| support_energy | Summe aller effektiven Bestätigungsenergien |
| conflict_energy | Summe aller effektiven Widerspruchsenergien |
| diagnostic_energy | Summe aller effektiven diagnostischen Energien |
| policy_energy | Summe aller effektiven Policy-Energien |
| coverage_energy | Summe aller effektiven Coverage-Energien |
| evidence_mass | support_energy + conflict_energy |

<!-- @section id="6.6" title="Zone-Health und Quarantäne" type="prose" -->
### §6.6 Zone-Health und Quarantäne

<!-- @table schema="state_machine_states" machine="zone_health" -->
| Zustand | Bedeutung |
|---------|-----------|
| UNEXPLORED | Zone wurde noch nicht erkundet |
| EXPLORED_INCONCLUSIVE | Zone wurde erkundet, aber ohne klare Evidenz |
| HEALTHY | Zone ist gesund |
| DEGRADED | Zone ist beeinträchtigt |
| CRITICAL | Zone ist kritisch |
| LOCKED | Zone ist gesperrt |

<!-- @section id="6.7" title="Kristallisation" type="prose" -->
### §6.7 Kristallisation

Kristallisation erfolgt nur, wenn alle folgenden Bedingungen erfüllt sind:
1. Der Knoten ist eine Hypothese.
2. `crystallization_progress >= 1.0`
3. Mindestens `min_confirmations` relevante Bestätigungen liegen vor.
4. `fracture_score < max_fracture_for_crystallization`
5. Kein starkes 🟨- oder 🟥-Ereignis innerhalb der `interrupt_window`
6. Die Zone ist nicht `LOCKED`
7. Die Zone ist nicht in `quarantine_mode`
8. Keine aktive Policy-Blockade verhindert die Kristallisation
9. Die Evidence-Class-Transferregeln sind erfüllt

Evidence-Class-Transferregel:
Wenn `evidence_class = SIMULATION` oder `SANDBOX`: darf kein physischer Kristall ohne physische Validierung erzeugt werden.

<!-- @section id="6.8" title="DiagnosticResolution" type="prose" -->
### §6.8 DiagnosticResolution

<!-- @table schema="diagnostic_outcomes" -->
| Outcome | Bedeutung |
|---------|-----------|
| CONFIRMS_CONTRADICTION | Diagnose bestätigt den Widerspruch |
| EXPLAINS_CONTRADICTION | Diagnose erklärt die Ursache des Widerspruchs |
| RESOLVES_CONTRADICTION | Diagnose löst den Widerspruch auf |
| INCONCLUSIVE | Diagnose ist unklar |
| TWIN_DRIFT_CONFIRMED | Twin weicht von der Realität ab |
| TWIN_CALIBRATED | Twin wurde neu kalibriert |

<!-- @section id="6.9" title="SafetyConstraint und ExclusionConstraint" type="prose" -->
### §6.9 SafetyConstraint und ExclusionConstraint

SafetyConstraint:
- Persistent, kein automatischer Decay
- Kann nur durch autorisierte Governance aufgehoben werden
- Überschreibt Frontier-Freigaben

<!-- @section id="6.10" title="FrontierEngine" type="prose" -->
### §6.10 FrontierEngine

Die FrontierEngine findet sinnvolle nächste Forschungsziele. Sie ist keine Ausführungsinstanz. Sie erzeugt nur FrontierCandidates.

<!-- @section id="6.11" title="ResearchTopic und ExplorationPolicy" type="prose" -->
### §6.11 ResearchTopic und ExplorationPolicy

<!-- @section id="6.12" title="Zugriffsmatrix" type="prose" -->
### §6.12 Zugriffsmatrix

<!-- @table schema="access_matrix" -->
| Komponente | Atlas lesen | Atlas schreiben | EvidenceEvents erzeugen | SafetyConstraint freigeben |
|------------|------------|----------------|------------------------|--------------------------|
| Archivar | ✅ | ❌ | ✅ via Übergabe | ❌ |
| Kartograph | ✅ | ✅ | ✅ abgeleitet | ❌ |
| Kanzler | ✅ | ❌ | ❌ | ✅ |
| Königin | ✅ | ❌ | ❌ | ✅ |
| Vordenker | ✅ | ❌ | ❌ | ❌ |
| Pre-Filter | ✅ | ❌ | ❌ | ❌ |
| Lotse | ✅ | ✅ Wegmarken | ❌ | ❌ |
| Quartiermeister | ✅ | ❌ | ❌ | ❌ |
| Richter | ✅ | ❌ | ❌ | ❌ |
| Seher | ✅ eingeschränkt | ❌ | ❌ niemals 🟥 | ❌ |
| Dispatcher | ✅ | ❌ | ❌ | ❌ |
| Receiver | ❌ | ❌ | ❌ | ❌ |
| Questor | ❌ | ❌ | ❌ | ❌ |
| HAL | ❌ | ❌ | ❌ | ❌ |

<!-- @section id="6.13" title="FULL_REBUILD, NEUAUSRICHTEN und Atlas-Versionierung" type="prose" -->
### §6.13 FULL_REBUILD, NEUAUSRICHTEN und Atlas-Versionierung

<!-- @section id="6.14" title="Digital-Twin-Loop" type="dataflow" dataflow="twin_drift_detection" -->
### §6.14 Digital-Twin-Loop

Dieser Abschnitt definiert die Integration des Digital-Twin-Systems in die Pipeline-Mechanik des Gremiums. Die strategische Steuerung des Twin-Loops (Twin-Drift-Erkennung, Kalibrierungs-Anforderung) ist in `GREMIUM_STRATEGY.md §14` (SL-TWIN-1..11) definiert.

<!-- @section id="6.14.1" title="Zweck" type="prose" -->
#### §6.14.1 Zweck

Der Digital-Twin-Loop ermöglicht:
- Vergleich von Simulations-Ergebnissen mit Real-Experimenten
- Erkennung von Modell-Drift (Sim-weicht-von-Real-ab)
- Automatische Kalibrierung des Twin-Modells
- Validierung der Modell-Güte über die Zeit

<!-- @section id="6.14.2" title="Verträge" type="prose" -->
#### §6.14.2 Verträge

Die Datenverträge für den Digital-Twin-Loop sind in `CONTRACTS.md §6.10.19` und `§6.10.20` definiert:
- `DigitalTwinModel` (CONTRACTS §6.10.19)
- `TwinDivergenceReport` (CONTRACTS §6.10.20)

<!-- @section id="6.14.3" title="Sim-Kristall vs. Real-Kristall" type="prose" -->
#### §6.14.3 Sim-Kristall vs. Real-Kristall

<!-- @table schema="evidence_class_rules" -->
| Typ | evidence_class | Erlaubte Knoten-Aktualisierung |
|-----|---------------|-------------------------------|
| Sim-Kristall | SIMULATION oder SANDBOX | Darf nur DIGITAL_TWIN-Knoten aktualisieren. Darf niemals einen CRYSTAL-Knoten erzeugen. |
| Real-Kristall | PHYSICAL_EXPERIMENT | Darf CRYSTAL, HYPOTHESIS und DIGITAL_TWIN-Knoten aktualisieren. |
| Kalibrierungs-Kristall | COMPUTE_EVALUATION | Darf nur DIGITAL_TWIN-Knoten aktualisieren. |

<!-- @section id="6.14.4" title="Divergenz-Berechnung (Kartograph)" type="dataflow" dataflow="twin_drift_detection" -->
#### §6.14.4 Divergenz-Berechnung (Kartograph)

<!-- @dataflow id="twin_drift_detection" trigger="TWIN_DIVERGENCE" source_role="kartograph" target_role="strategic_layer" -->
Der Kartograph berechnet den `TwinDivergenceReport`, wenn er zwei Kristallkandidaten mit demselben `objective_family_ref` und demselben `digital_twin_ref` empfängt:

<!-- @dataflow-step order="1" -->
1. Extrahiere metric_vector aus Sim-Kristall und Real-Kristall.

<!-- @dataflow-step order="2" -->
2. Berechne pro Metrik die relative Abweichung: `dev = abs(sim - real) / max(abs(real), epsilon)`

<!-- @dataflow-step order="3" -->
3. `overall_divergence_score = mean(dev)` über alle gemeinsamen Metriken.

<!-- @dataflow-step order="4" condition="overall_divergence_score > threshold" -->
4. Wenn `overall_divergence_score > twin_model.divergence_threshold`:
   → `tolerance_breached = true`
   → `calibration_required = true`
   → Erhöhe den `drift_score` des Twin-Knotens.
   → Erzeuge SymptomEvent(TWIN_DRIFT) an den Strategischen Layer.

<!-- @section id="6.14.5" title="Kalibrierungs-Loop" type="dataflow" dataflow="kalibrierungs_loop" -->
#### §6.14.5 Kalibrierungs-Loop

<!-- @dataflow id="kalibrierungs_loop" trigger="TWIN_DRIFT" source_role="frontier_engine" target_role="dispatcher" -->
Wenn `calibration_required = true`:

<!-- @dataflow-step order="1" -->
1. FrontierEngine erzeugt FrontierCandidate:
   - `frontier_type = DIAGNOSTIC_FRONTIER`
   - `suggested_objective_type = DIAGNOSE`
   - `suggested_gate_mode = FRACTURE_DIAGNOSIS`
   - `digital_twin_ref = twin_node_ref`

<!-- @dataflow-step order="2" -->
2. Quartiermeister baut ResearchPackage:
   - `objective_type = DIAGNOSE`
   - `digital_twin_ref = twin_node_ref`
   - `security_mode = SANDBOX` oder `DEV_SANDBOX_ONLY` (Kalibrierung ist Compute, keine Physik!)

<!-- @dataflow-step order="3" -->
3. Questor führt Kalibrierungs-Lauf aus.

<!-- @dataflow-step order="4" -->
4. Kartograph aktualisiert DIGITAL_TWIN-Knoten:
   - `model_version` wird erhöht.
   - `drift_score` wird reduziert.
   - `last_calibration_at` wird aktualisiert.
   - `DiagnosticResolution.outcome = TWIN_CALIBRATED`.

<!-- @section id="6.14.6" title="Validity-Regeln" type="prose" -->
#### §6.14.6 Validity-Regeln

- Ein DIGITAL_TWIN-Knoten mit `drift_score > divergence_threshold` wird als DEGRADED markiert.
- Ein DIGITAL_TWIN-Knoten in `quarantine_mode` darf nur für DIAGNOSE (Kalibrierung) verwendet werden.
- Wenn `validity.valid_until` abgelaufen ist, wird der Twin automatisch als DEGRADED markiert.

<!-- @section id="6.14.7" title="Pipeline-Integration" type="prose" -->
#### §6.14.7 Pipeline-Integration

<!-- @table schema="pipeline_integration" -->
| Pipeline-Stufe | Digital-Twin-Aktion |
|---------------|-------------------|
| Archivar (Stufe 1) | Übergibt `digital_twin_ref` und `twin_model_version` aus `ReproducibilityContext` an Kartograph |
| Kartograph (Stufe 2) | Berechnet TwinDivergenceReport, aktualisiert drift_score, erzeugt SymptomEvent(TWIN_DRIFT) |
| Vordenker (Stufe 4) | Erhält TWIN_DRIFT-Symptom, schlägt Kalibrierungs-Hypothese vor |
| Lotse (Stufe 5b) | Platziert Diagnose-Wegmarke mit `digital_twin_ref` |
| Quartiermeister (Stufe 6) | Baut SANDBOX-Paket für Kalibrierung |
| Sicherheitsrat (Stufe 7) | Prüft Kalibrierungs-Paket (gate_mode = FRACTURE_DIAGNOSIS) |
| Dispatcher (Stufe 8) | Sendet Kalibrierungs-Paket an Questor |

<!-- @section id="6.14.8" title="Sicherheitsregeln" type="prose" -->
#### §6.14.8 Sicherheitsregeln

- Questor darf `digital_twin_ref` nicht als LLM-Kontext verwenden (→ CHARTER §SR-24).
- Questor darf den Twin nicht eigenmächtig kalibrieren.
- Kalibrierung erfolgt ausschließlich über den definierten Pipeline-Pfad.
- Sim-Evidenz darf keine physischen Kristalle bestätigen (→ CHARTER §SR-08, GREMIUM §6.7 Evidence-Class-Transferregel).

<!-- @section id="7" title="Dispatch-Koordination (Stufe 8)" type="prose" -->
## §7 Dispatch-Koordination (Stufe 8)

<!-- @section id="7.1" title="Dispatcher" type="role-definition" role="dispatcher" -->
<!-- @role id="dispatcher" layer="4" llm="false" pipeline_stage="8" writes_to="questor_queue" reads_from="gate_records" -->
### §7.1 Dispatcher

Verantwortung: Erzeugt `QuestorDispatchEnvelope` und schreibt in die Queue.

<!-- @table schema="role_rules" role="dispatcher" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Kein produktiver Versand ohne gate_record_ref | SR-53 | PACKAGE_INVALID |
| Kein produktiver Versand ohne gültige Lease-Logik | SR-03 | FAIL |
| Keine direkte physische Ausführung ohne Envelope | SR-01 | FAIL |

<!-- @section id="7.2" title="Receiver" type="role-definition" role="receiver" -->
<!-- @role id="receiver" layer="4" llm="false" pipeline_stage="8" writes_to="archivar" reads_from="questor_queue" -->
### §7.2 Receiver

Verantwortung: Empfängt `questor_ergebnis_paket` von Questor.

<!-- @table schema="role_rules" role="receiver" -->
| Regel | CHARTER-Ref | Konsequenz bei Verstoß |
|-------|-------------|------------------------|
| Vertrag validieren | SR-20 | Unvollständiges Ergebnis wird nicht verarbeitet |
| Idempotenz prüfen | SR-54 | Duplikat wird verworfen |
| Sequence prüfen | SR-20 | Rückläufige Sequence wird abgelehnt |
| Blackbox nicht lesen | SR-07 | Zugriff verweigert |

<!-- @section id="8" title="Gremium-Auslagerungen" type="prose" -->
## §8 Gremium-Auslagerungen

<!-- @ref target="CHARTER §4" type="spec" -->
→ Siehe CHARTER §4 für die vollständige Liste aller 22 Gremium-Auslagerungen.

<!-- @table schema="gremium_delegations" -->
| # | Thema | Gremium-Komponente |
|---|-------|-------------------|
| G-1 | Template-Erstellung bei fehlendem Template | Quartiermeister + Domain-Experte |
| G-2 | Template-Korrektur nach Questor-Feedback | Domain-Experte (NICHT Kanzler) |
| G-3 | Template-Versionierung (alte Versionen im Archiv) | Archivar |
| G-4 | Ressourcen-Karte (Verbrauch pro Zone/Dimension) | Kartograph |
| G-5 | Vordenker liefert prozess_skizze mit Idee | Vordenker |
| G-6 | template_feedback operational protokollieren | Archivar |
| G-7 | Kosten-Schätzungen für Reagenzien | System-Integrator |
| G-8 | Kanzler erhält periodische Template-Zusammenfassung | Kanzler (nur Übersicht) |
| G-9 | Quartiermeister berücksichtigt template_feedback | Quartiermeister |
| G-10 | atlas_version_ref ist Pass-Through, kein LLM-Zugriff | Questor (intern) |
| G-11 | loop_selection_weights optional im QuestorSpec | Quartiermeister |
| G-12 | planning_hints als optionales Feld | Quartiermeister |
| G-13 | Pipeline-Orchestrator liest registry.json und aktualisiert Atlas | Pipeline-Orchestrator (Gremium) |
| G-14 | Archivar bereinigt completed/ und failed/ nach Archivierung | Archivar |
| G-15 | Gremium schreibt Löschanfragen in delete_requests/ | Kanzler / Quartiermeister |
| G-16 | Capability-Definitionen erstellen und pflegen | System-Integrator |
| G-17 | Health-Monitoring: Externer Monitor liest health.json | Pipeline-Orchestrator |
| G-18 | Health-Monitoring: Recovery-Aktionen auslösen | Kanzler / Pipeline-Orchestrator |
| G-19 | Shutdown-Signal senden (SIGTERM) | Kanzler / Orchestrator |
| G-20 | Trail-Map lesen (nur autorisierte Rollen) | Domain-Experte / Entwickler |
| G-21 | Test-Strategie: CI/CD einrichten | System-Integrator |
| G-22 | Implementierungsplan: Phasen freigeben | Kanzler / Architekt |

<!-- @section id="9" title="Zustandsmaschinen der Pipeline-Stufen" type="prose" -->
## §9 Zustandsmaschinen der Pipeline-Stufen

<!-- @section id="9.1" title="Stufe 5b" type="state-machine" machine="ideen_pipeline" -->
### §9.1 Stufe 5b: IDEE_OFFEN → IDEE_GEPRÜFT → WEGMARKE_PLATZIERT

<!-- @table schema="state_transitions" machine="ideen_pipeline" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| IDEE_OFFEN | IDEE_GEPRÜFT | Pre-Filter erfolgreich |
| IDEE_GEPRÜFT | WEGMARKE_PLATZIERT | Lotse platziert erfolgreich |
| IDEE_GEPRÜFT | IDEE_VERWORFEN | Lotse verwirft |
| IDEE_OFFEN | IDEE_VERWORFEN | Pre-Filter verwirft |

<!-- @section id="9.2" title="Stufe 6" type="state-machine" machine="paket_bau" -->
### §9.2 Stufe 6: WEGMARKE_RESERVIERT → ... → PAKET_FERTIG

<!-- @table schema="state_transitions" machine="paket_bau" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| WEGMARKE_RESERVIERT | PAKET_IM_BAU | Quartiermeister startet |
| PAKET_IM_BAU | PAKET_FERTIG | Paketbau erfolgreich |
| PAKET_IM_BAU | PAKET_FEHLGESCHLAGEN | Paketbau fehlgeschlagen |

<!-- @section id="9.3" title="Stufe 7" type="state-machine" machine="gate_state" -->
### §9.3 Stufe 7: GATE_PENDING → ... → FREIGEGEBEN / DISPUTED

→ Siehe §4.7 für die vollständige Gate-Zustandsmaschine.

<!-- @section id="9.4" title="Stufe 8" type="state-machine" machine="dispatch_state" -->
### §9.4 Stufe 8: RESOURCE_WAITING → ... → ABGESCHLOSSEN / ABORTED

<!-- @table schema="state_transitions" machine="dispatch_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| RESOURCE_WAITING | LEASE_GRANTED | Leases gewährt |
| RESOURCE_WAITING | ABORTED | LeaseDenied (kein ESTOP!) |
| LEASE_GRANTED | QUESTOR_DISPATCHED | Envelope gesendet |
| QUESTOR_DISPATCHED | QUESTOR_RUNNING | Questor startet |
| QUESTOR_RUNNING | ABGESCHLOSSEN | Erfolgreich |
| QUESTOR_RUNNING | ABORTED | Fehler/Abbruch |

<!-- @section id="10" title="Event-Driven Architecture" type="prose" -->
## §10 Event-Driven Architecture

<!-- @section id="10.1" title="Pipeline-Events" type="prose" -->
### §10.1 Pipeline-Events

Event-Typen:
- `IDEE_ERZEUGT`: Vordenker hat Idee generiert
- `IDEE_GEPRUEFT`: Pre-Filter erfolgreich
- `WEGMARKE_PLATZIERT`: Lotse hat Wegmarke gesetzt
- `PAKET_GEBAUT`: Quartiermeister fertig
- `GATE_FREIGEGEBEN`: Sicherheits-Gate passiert
- `QUESTOR_COMPLETED`: Questor fertig
- `KRISTALL_ERZEUGT`: Archivar hat Kristall geschrieben
- `SIGNAL_ERZEUGT`: Archivar hat Signal geschrieben

<!-- @section id="10.2" title="Bounded Queues mit Watermarks" type="prose" -->
### §10.2 Bounded Queues mit Watermarks

<!-- @section id="10.3" title="Deadlock-Erkennung" type="prose" -->
### §10.3 Deadlock-Erkennung

<!-- @section id="10.4" title="Notventil-Zyklen" type="prose" -->
### §10.4 Notventil-Zyklen

<!-- @section id="11" title="Sicherheitsregeln" type="prose" -->
## §11 Sicherheitsregeln

<!-- @ref target="CHARTER §3" type="security-rule" -->
→ Siehe CHARTER §3 für die vollständige Liste aller 58 Sicherheitsregeln.

<!-- @table schema="safety_rules" category="gremium" -->
| # | Regel | CHARTER-Referenz |
|---|-------|-----------------|
| 1 | Keine physische Ausführung ohne Envelope | SR-01 |
| 2 | Keine physische Ausführung ohne Gate | SR-02 |
| 3 | Keine physische Ausführung ohne Lease | SR-03 |
| 4 | Questor schreibt nicht in Atlas/Archiv | SR-04 |
| 5 | Questor setzt ESTOP nicht zurück | SR-05 |
| 6 | Questor vergibt keine Leases | SR-06 |
| 7 | Blackbox bleibt lokal | SR-07 |
| 8 | Operational ≠ Scientific | SR-08 |
| 9 | ESTOP ≠ LEASE_DENIED | SR-09 |
| 10 | Fail-Closed bei Unklarheit | SR-10 |
| 11 | Menschliche Königin wird niemals überstimmt | SR-11 |
| 12 | Hardwarezugriff nur über HAL | SR-12 |
| 13 | LLM nur Advisor, niemals final | SR-13 |
| 14 | Kein Dispatch ohne gate_record_ref | SR-53 |
| 15 | Keine Duplikate in der Queue | SR-54 |
| 16 | Atomare Schreiboperationen | SR-55 |
| 17 | Registry-Lock | SR-56 |
| 18 | Kein Löschen von processing/ | SR-57 |
| 19 | Queue-Fehler sind immer OPERATIONAL | SR-58 |

<!-- @section id="12" title="Implementierungsphasen" type="implementation-phase" -->
## §12 Implementierungsphasen

<!-- @table schema="phase_tasks" phase="gremium" -->
| Phase | Name | Dauer (Schätzung) |
|-------|------|-------------------|
| Phase 1 | Contracts & Datenmodelle | 3–5 Tage |
| Phase 2 | Atlas & Signal-System | 3–4 Tage |
| Phase 3 | Transaction (WAL, State Machine) | 2–3 Tage |
| Phase 4 | Resource Governor & HAL | 3–4 Tage |
| Phase 5 | Gremium Basis (Archivar, Kartograph) | 3–4 Tage |
| Phase 6 | Gremium Erweitert (Vordenker, Lotse) | 3–4 Tage |
| Phase 7 | Sicherheitsrat (Richter, Seher) | 3–4 Tage |
| Phase 8 | Questor-Interface | 2–3 Tage |
| Phase 9 | Pipeline-Orchestrierung | 3–4 Tage |
| Phase 10 | Integration & Regression | 5–7 Tage |

<!-- @section id="13" title="Zusammenfassung der Architektur-Entscheidungen" type="prose" -->
## §13 Zusammenfassung der Architektur-Entscheidungen

<!-- @table schema="architecture_decisions" -->
| Thema | Entscheidung | Quelle |
|-------|-------------|--------|
| Blackboard-Pattern | Alle Ränge kommunizieren über Atlas und Archiv | §1.2 |
| Menschliche Königin | Wird niemals überstimmt | §1.2 |
| Fail-Closed | Bei Unklarheit: keine Freigabe | §1.2 |
| Seher | Schreibt niemals direkt 🟥 | §1.2 |
| Operational ≠ Scientific | Strikte Trennung | §1.2 |
| Questor | Ist kein Gremium-Rang | §1.2 |
| 9-Stufen-Pipeline | Vollständig definiert | §2 |
| Sicherheitsrat | Richter + Seher + Circuit-Breaker + Appeal + Policy-Veto-Review | §4 |
| Circuit-Breaker | 4 Zustände, Messfenster, Hysterese | §4.4 |
| Policy-Veto-Review | Konfigurierbar, persistent, Audit-Event | §4.6 |
| Pipeline-Orchestrator | Bounded Queues, Deadlock-Erkennung, Notventil | §5 |
| Atlas-Hybrid | Evidenzbasierte, semantische und explorationsfähige Wissenschaftskarte | §6 |
| Evidence-Semantik | Signale werden über evidence_kind interpretiert | §6.4 |
| Energiekonten | Support, Conflict, Diagnostic, Policy, Coverage | §6.5 |
| FrontierEngine | Erzeugt FrontierCandidates, keine Ausführung | §6.10 |
| ResearchTopic | Themenautonomie mit Zustandsmaschine | §6.11 |
| SafetyConstraint | Persistent, kein Decay, manuelle Freigabe | §6.9 |
| DiagnosticResolution | Kann Widersprüche erklären oder auflösen | §6.8 |
| Dispatch | Envelope-basiert, Queue-Integration | §7 |
| Gremium-Auslagerungen | 22 Auslagerungen | §8 |
| Zustandsmaschinen | 4 Pipeline-Stufen | §9 |
| Event-Driven Architecture | Pipeline-Events, Bounded Queues | §10 |
| Sicherheitsregeln | 19 relevante Regeln | §11 |
| Implementierungsphasen | 10 Phasen | §12 |
| Strategische Steuerung | In GREMIUM_STRATEGY.md ausgelagert | §0.2 |
| Digital-Twin-Loop | Pipeline-Integration in §6.14, Strategie in GREMIUM_STRATEGY.md §14 | §6.14 |
| 4-Achsen-Architektur | In GREMIUM_STRATEGY.md definiert | §0.2 |

<!-- @section id="14" title="Dokumentenhierarchie" type="prose" -->
## §14 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `specs/` und referenziert:
- `foundation/CHARTER.md` für Sicherheitsregeln (CHARTER §SR-XX)
- `foundation/CONTRACTS.md` für Datenverträge (CONTRACTS §X.X)
- `specs/QUESTOR.md` für Questor-spezifische Details
- `specs/HAL.md` für HAL-spezifische Details
- `specs/GREMIUM_STRATEGY.md` für strategische Steuerung (Achsen, ControlState, Kanzler/Königin)

Regel: Änderungen an Gremium-Modulen in diesem Dokument erfordern eine Versionsänderung und eine Überprüfung der referenzierten Dokumente.

Aufteilung zwischen GREMIUM.md und GREMIUM_STRATEGY.md:

<!-- @table schema="document_split" -->
| Thema | GREMIUM.md (dieses Dokument) | GREMIUM_STRATEGY.md |
|-------|------------------------------|---------------------|
| 9-Stufen-Pipeline | ✅ | — |
| Sicherheitsrat (Richter/Seher) | ✅ | — |
| Pipeline-Orchestrator | ✅ | — |
| Atlas-Hybrid-System | ✅ | — |
| Digital-Twin-Loop (Pipeline) | ✅ (§6.14) | Strategie (§14) |
| Event-Driven Architecture | ✅ | — |
| Kanzler & Königin | — | ✅ |
| Briefing-Zyklus | — | ✅ |
| 4-Achsen-Architektur | — | ✅ |
| ControlState & SL-AX-ATOMIC | — | ✅ |
| Intent-Verfügbarkeit | — | ✅ |
| Closure-Regeln (CT-1..CT-10) | — | ✅ |
| Symptom-Trigger | — | ✅ |
| DTT (DirectiveTranslationTable) | — | ✅ |

<!-- @section id="A" title="Anhang A: Korrekturhinweis" type="prose" -->
## Anhang A: Korrekturhinweis für alte GREMIUM.md-Stellen

<!-- @table schema="corrections" -->
| # | Alte Annahme | Korrektur | Quelle |
|---|-------------|-----------|--------|
| 1 | SAFETY → Sicherheits-Signal | Bei SAFETY-Abbruch sind Kristalle und Signale aus Questor leer. Ein separates Sicherheits-Governance-Ereignis ist erlaubt. | CHARTER §SR-19 |
| 2 | Signal-Resolution nur nach Priorität | Signal-Resolution wird durch Energiekonten und Evidence-Semantik ergänzt. Priorität bleibt nur für Safety-Override relevant. | §6.4, §6.5 |
| 3 | Kristallisation nach 3 Bestätigungen | Kristallisation nutzt crystallization_progress, Mindestbestätigungen, Fracture-Grenze und Interrupt-Window. | §6.7 |
| 4 | fracture_score primär aus roten Signalen | fracture_score wird aus conflict_energy und support_energy berechnet. | §6.5 |
| 5 | Zone-Health: HEALTHY < 0.3, DEGRADED < 0.7, CRITICAL >= 0.7 | Zone-Health nutzt degraded_threshold, quarantine_threshold, full_rebuild_threshold, UNEXPLORED, EXPLORED_INCONCLUSIVE und LOCKED. | §6.6 |
| 6 | Weiß ist neutral, aber ohne Funktion | Weiß erzeugt coverage_energy und kann EXPLORED_INCONCLUSIVE unterstützen. | §6.4, §6.5, §6.6 |
| 7 | Leere Zone kann implizit als gesund gelten | Leere Zone ist UNEXPLORED oder EXPLORED_INCONCLUSIVE, niemals automatisch HEALTHY. | §6.6 |

<!-- @section id="B" title="Anhang B: Akzeptanzprüfung" type="acceptance" -->
## Anhang B: Akzeptanzprüfung für ATLAS-HYB-1.0.0

<!-- @table schema="acceptance_criteria" -->
| # | Kriterium | Status |
|---|-----------|--------|
| 1 | Kopfzeile enthält Version 2.0.0-strat.1 | ☐ |
| 2 | §0.1 Änderungsantrag ATLAS-HYB-1.0.0 ist vorhanden | ☐ |
| 3 | §0.2 Beziehung zu GREMIUM_STRATEGY.md ist vorhanden | ☐ |
| 4 | Archivar ist auf Atlas-Hybrid aktualisiert | ☐ |
| 5 | Archivar behandelt SAFETY gemäß CHARTER §SR-19 | ☐ |
| 6 | Kartograph ist auf Atlas-Hybrid aktualisiert | ☐ |
| 7 | Kartograph führt Energiekonten | ☐ |
| 8 | Kartograph aktualisiert FrontierEngine | ☐ |
| 9 | Kartograph enthält Digital-Twin-Pflichten | ☐ |
| 10 | Kanzler verwaltet ExplorationPolicy und Safety-Freigaben | ☐ |
| 11 | Vordenker nutzt FrontierCandidates | ☐ |
| 12 | Vordenker enthält Digital-Twin-Pflichten | ☐ |
| 13 | Pre-Filter prüft SafetyConstraints und ExclusionConstraints | ☐ |
| 14 | Lotse setzt Erwartungsreferenzen und Diagnose-Wegmarken | ☐ |
| 15 | Quartiermeister setzt Atlas-Hybrid-Referenzen | ☐ |
| 16 | §6 Atlas-Hybrid-System ersetzt das alte Atlas-Signal-System | ☐ |
| 17 | Energy-Formeln sind dokumentiert | ☐ |
| 18 | Zone-Health enthält UNEXPLORED und EXPLORED_INCONCLUSIVE | ☐ |
| 19 | Quarantäne ist als Modus beschrieben | ☐ |
| 20 | DiagnosticResolution ist beschrieben | ☐ |
| 21 | SafetyConstraint ist persistent und blockierend | ☐ |
| 22 | FrontierEngine erzeugt nur Empfehlungen | ☐ |
| 23 | ResearchTopic und ExplorationPolicy sind beschrieben | ☐ |
| 24 | Zugriffsmatrix enthält Questor ohne Atlas-Schreibrecht | ☐ |
| 25 | Zugriffsmatrix enthält HAL ohne Atlas-Schreibrecht | ☐ |
| 26 | Zugriffsmatrix enthält Seher ohne rote Signale | ☐ |
| 27 | §6.14 Digital-Twin-Loop ist definiert | ☐ |
| 28 | §14 Dokumentenhierarchie enthält GREMIUM_STRATEGY.md | ☐ |
| 29 | Keine neuen Datenverträge wurden definiert | ☐ |
| 30 | Keine neuen Sicherheitsregeln wurden definiert | ☐ |
| 31 | CHARTER-Hierarchie bleibt gewahrt | ☐ |
| 32 | Keine strategischen Inhalte (Achsen, ControlState) in diesem Dokument | ☐ |