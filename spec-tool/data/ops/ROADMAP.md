---
doc_id: ops/ROADMAP.md
doc_type: spec
version: 1.2.0-strat.1
status: BINDEND
schema_version: spec-format-1.0
layer: ops
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1-twin.1
  - specs/QUESTOR.md@1.1.0-atlas-hyb.1
  - specs/HAL.md@1.1.0-atlas-hyb.1
  - specs/GREMIUM.md@2.0.0-strat.1
  - specs/GREMIUM_STRATEGY.md@1.0.0
  - specs/CAROUSEL_TWIN.md@1.1.0-patch.1
  - ops/VALIDATION.md@1.2.0-strat.1
conflict_rule: [CHARTER, CONTRACTS, SPECS, VALIDATION, THIS_DOC]
roles_referenced:
  - systems_architect
  - senior_software_engineer
  - test_engineer
last_modified: 2026-08-21
---

<!-- @section id="0" title="Geltung und Änderungsregeln" type="meta" -->
# 🗺️ ROADMAP — IMPLEMENTIERUNGSPLAN UND PHASEN

## §0 Geltung und Änderungsregeln

Dieses Dokument definiert die vollständige Implementierungsplanung für das Gesamtsystem.

Regel: Dieses Dokument referenziert Verträge aus `CONTRACTS.md` und Sicherheitsregeln aus `CHARTER.md`.
Es definiert keine neuen Verträge und keine neuen Sicherheitsregeln.

Konfliktregel: Bei Widersprüchen gilt `CHARTER.md` > `CONTRACTS.md` > `specs/*` > `ops/VALIDATION.md` > dieses Dokument.

<!-- @section id="0.1" title="Änderungsantrag ATLAS-HYB-1.0.0" type="change-request" -->
### §0.1 Änderungsantrag ATLAS-HYB-1.0.0 — Atlas-Hybrid-Phasen

Dieser Änderungsantrag fügt die Implementierungsphasen für das Atlas-Hybrid-System in die Roadmap ein.
Das Atlas-Hybrid-System wird als eigener Phasen-Block (A1–A5) geführt, der auf den MYRMEX-Neubau-Phasen 1 bis 3 aufbaut und vor der finalen End-to-End-Integration (Phase 10) abgeschlossen sein muss.

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge (→ CONTRACTS.md).
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln (→ CHARTER.md).
- Die Atlas-Hybrid-Phasen respektieren das Blackboard-Pattern und die Trennung von Operational und Scientific.
- Questor erhält auch in der Implementierung keine Atlas-Schreibrechte.

<!-- @section id="0.2" title="Änderungsantrag STRAT-1.0.0" type="change-request" -->
### §0.2 Änderungsantrag STRAT-1.0.0 — Strategic-Layer-Phasen

Dieser Änderungsantrag fügt die Implementierungsphasen für den Gremium Strategic Layer (Cognitive Observatory) in die Roadmap ein.
Der Strategic Layer wird als eigener Phasen-Block (S1–S3) geführt, der auf den MYRMEX-Neubau-Phasen 1 bis 3 und den Atlas-Hybrid-Phasen A1–A2 aufbaut.

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge (→ CONTRACTS.md §6.11).
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln (→ CHARTER.md).
- Die Strategic-Layer-Phasen respektieren das Blackboard-Pattern und die Trennung von Operational und Scientific.
- Questor und HAL erhalten keine Kenntnis von Strategic-Layer-Verträgen (→ CHARTER §SR-04).
- Die strategische Steuerung ist in `specs/GREMIUM_STRATEGY.md` definiert.
- Die Pipeline-Mechanik bleibt in `specs/GREMIUM.md`.

<!-- @section id="1" title="Roadmap-Übersicht und Grundprinzipien" type="prose" -->
## §1 Roadmap-Übersicht und Grundprinzipien

<!-- @section id="1.1" title="Zweck" type="prose" -->
### §1.1 Zweck

Dieses Dokument definiert:
- Die vollständige Phasenplanung für MYRMEX v2.4.0 + Questor v0.2.3 + HAL v0.2.0
- Die Abhängigkeiten zwischen Phasen
- Die Meilensteine und Zeitplanung
- Die Akzeptanzkriterien pro Phase
- Die Risikobewertung
- Die Test-Gates pro Phase

<!-- @section id="1.2" title="Die sechs Roadmap-Grundprinzipien" type="prose" -->
### §1.2 Die sechs Roadmap-Grundprinzipien

<!-- @table schema="roadmap_principles" -->
| # | Prinzip | Bedeutung | CHARTER-Referenz |
|---|---------|-----------|-----------------|
| 1 | Phase-by-Phase | Arbeite eine Phase vollständig ab, bevor die nächste beginnt. | — |
| 2 | Kein Code ohne Freigabe | Schreibe keinen Code für Phasen, die nicht freigegeben sind. | — |
| 3 | Dry-Run-Modus | Wenn keine Implementierungsfreigabe vorliegt: kein Code, keine Dateiänderungen, nur mentale Simulation. | — |
| 4 | TDD | Tests werden vor oder parallel zum Code geschrieben. | — |
| 5 | Keine späteren Phasen vorziehen | Implementiere nur die explizit freigegebene Phase. | — |
| 6 | Status-Report nach jeder Phase | Nach jeder Phase ist ein Status-Report zu erstellen. | — |

<!-- @section id="1.3" title="Rolle der implementierenden KI" type="prose" -->
### §1.3 Rolle der implementierenden KI

Die implementierende KI handelt als:
- Senior Software Engineer
- Systems Architect
- Test Engineer für Systemintegration

<!-- @section id="1.4" title="Arbeitsregeln" type="prose" -->
### §1.4 Arbeitsregeln

<!-- @table schema="working_rules" -->
| Regel | Beschreibung |
|-------|-------------|
| AR-1 | Arbeite phase-by-phase. |
| AR-2 | Schließe eine Phase vollständig ab, bevor die nächste beginnt. |
| AR-3 | Schreibe keinen Code für Phasen, die nicht freigegeben sind. |
| AR-4 | Wenn keine Implementierungsfreigabe vorliegt: kein Code, keine Dateiänderungen, nur Dry-Run / mentale Simulation. |
| AR-5 | Wenn Implementierungsfreigabe vorliegt: nur die explizit freigegebene Phase implementieren. |
| AR-6 | Python 3.10+, Pydantic v2, pytest. |
| AR-7 | Keine späteren Phasen vorziehen. |
| AR-8 | Nach jeder Phase Status-Report schreiben. |
| AR-9 | Blocker und Nicht-Blocker immer getrennt melden. |

<!-- @section id="2" title="Phasen-Übersicht (alle Systeme)" type="prose" -->
## §2 Phasen-Übersicht (alle Systeme)

<!-- @section id="2.1" title="Gesamtsystem-Phasen" type="prose" -->
### §2.1 Gesamtsystem-Phasen

<!-- @table schema="system_phases" -->
| System | Phasen | Anzahl | Gesamtdauer (Schätzung) |
|--------|--------|--------|-------------------------|
| MYRMEX (Migration) | M0–M5 | 6 | 10–15 Tage |
| MYRMEX (Neubau) | Phase 1–10 | 10 | 25–35 Tage |
| Atlas-Hybrid | A1–A5 | 5 | 12–18 Tage |
| Strategic Layer | S1–S3 | 3 | 10–15 Tage |
| HAL | HAL-H0 bis HAL-H6 | 7 | 15–22 Tage |
| Questor | Q0–Q18 | 19 | 44–67 Tage |
| **Gesamt** | | **50** | **~116–172 Tage** |

<!-- @section id="2.2" title="Phasen-Typen" type="prose" -->
### §2.2 Phasen-Typen

<!-- @table schema="phase_types" -->
| Typ | Bedeutung |
|-----|-----------|
| Migration | Umbenennung und Vertragsmigration von v2.3.1 auf v2.4.0 |
| Neubau | Sauberer Neuaufbau ohne Bestand |
| Atlas-Hybrid | Evidenzbasierte, semantische und explorationsfähige Wissenschaftskarte |
| HAL | Hardware Abstraction Layer |
| Questor | Questor-Interna (Teile A–S) |
| Strategic Layer | 4-Achsen-Steuerung, Kanzler/Königin, Briefing-Zyklus, ControlState |

<!-- @section id="3" title="MYRMEX-Migrationsphasen (M0–M5)" type="prose" -->
## §3 MYRMEX-Migrationsphasen (M0–M5)

<!-- @section id="3.1" title="Phase M0: Archivierung und Schnitt" type="implementation-phase" -->
### §3.1 Phase M0: Archivierung und Schnitt

**Ziel:** Alte Referenz archivieren, neue Referenz aktivieren, keine Adapter einplanen.

**Aufgaben:**
- `structure_standalone_v2.3.1.md` als archiviert markieren
- Diese Strukturdatei als primäre Referenz bestätigen
- `structure_standalone_questor_v0.2.3.md` als unterstützend einordnen
- Sicherstellen, dass keine produktive Adapterlogik geplant ist

**Akzeptanzkriterien:**
- [ ] Keine aktive Doppelreferenz
- [ ] Keine produktiven Altbezeichnungen geplant
- [ ] Keine Adapter geplant
- [ ] Konflikthierarchie dokumentiert

<!-- @section id="3.2" title="Phase M1: Vertrags-Umbenennung" type="implementation-phase" -->
### §3.2 Phase M1: Vertrags-Umbenennung

**Ziel:** Neue Vertragswelt sauber einführen.

**Aufgaben:**
- Neue Ergebnis- und Instanzbezeichnungen einführen
- `QuestorDispatchEnvelope` einführen
- `QuestorMetadata`, `LocalAuditRef`, `OperationalMetrics` definieren
- Kanonischen `idempotency_key` implementieren (→ CONTRACTS §8.1)
- QuestorSpec-Defaults implementieren (→ CONTRACTS §1.2)
- Circuit-Breaker-Zustände explizit machen
- Policy-Veto-Review-Parameter konfigurierbar machen

**Akzeptanzkriterien:**
- [ ] Keine alten Bezeichnungen in aktiven Zielquellen
- [ ] Neue Pydantic-Modelle existieren
- [ ] `idempotency_key` ist kanonisch (→ CONTRACTS §8.1)
- [ ] `attempt_id` ist eingeschränkt (0–999999)
- [ ] Mindestens 25 Vertragstests

<!-- @section id="3.3" title="Phase M2: Archivar auf Questor-Ergebnis umstellen" type="implementation-phase" -->
### §3.3 Phase M2: Archivar auf Questor-Ergebnis umstellen

**Ziel:** Archivar verarbeitet ausschließlich das neue Ergebnis.

**Aufgaben:**
- Sequence-Prüfung auf `questor_instance_id`
- `questor_metadata` optional verarbeiten
- `operational_metrics` nur operational verwenden
- Keine Blackbox-Zugriffe (→ CHARTER §SR-07)

**Akzeptanzkriterien:**
- [ ] Valide Questor-Ergebnisse werden akzeptiert
- [ ] Duplikate werden verworfen
- [ ] OPERATIONALE Abbrüche erzeugen keine wissenschaftlichen Signale (→ CHARTER §SR-08)
- [ ] Mindestens 20 Archivar-Integrationstests

<!-- @section id="3.4" title="Phase M3: Dispatcher und Receiver umstellen" type="implementation-phase" -->
### §3.4 Phase M3: Dispatcher und Receiver umstellen

**Ziel:** Produktiver Envelope-basierter Dispatch, sauberer Empfang des neuen Ergebnisses.

**Aufgaben:**
- Dispatcher baut Envelope
- Dispatcher prüft Gate, Lease, Security-Mode
- Receiver empfängt neues Ergebnis
- Direkte Paketübergaben nur sandbox/dev

**Akzeptanzkriterien:**
- [ ] Dispatcher sendet keine nackten Produktivpakete
- [ ] Envelope enthält `gate_record_ref` (→ CHARTER §SR-53)
- [ ] Receiver validiert Vertrag
- [ ] Mindestens 20 Dispatcher/Receiver-Tests

<!-- @section id="3.5" title="Phase M4: Questor-Implementierung oder Questor-Dummy" type="implementation-phase" -->
### §3.5 Phase M4: Questor-Implementierung oder Questor-Dummy

**Ziel:** Questor oder vertragstreuer Dummy ist vorhanden.

**Aufgaben:**
- Entweder: vollständige Questor-Implementierung gemäß v0.2.3
- Oder für Integrationstests: `DummyQuestor`, der vertragstreu reagiert

**Akzeptanzkriterien:**
- [ ] Questor/Dummy empfängt Envelope
- [ ] Liefert neues Ergebnis
- [ ] Keine direkten Atlas-/Archivzugriffe (→ CHARTER §SR-04)
- [ ] Blackbox bleibt lokal (→ CHARTER §SR-07)
- [ ] ESTOP, LEASE_DENIED, ROUTING_LOOP_TIMEOUT, SCIENTIFIC/OPERATIONAL werden korrekt getrennt (→ CHARTER §SR-08, §SR-09)

<!-- @section id="3.6" title="Phase M5: Gesamtsystem-Tests" type="implementation-phase" -->
### §3.6 Phase M5: Gesamtsystem-Tests

**Ziel:** Vollständige Integrationstests ohne Adapter.

**Aufgaben:**
- Suite N, I, S, R, Z aus der aktuellen Testdatei
- Questor-spezifische Sicherheits- und Blackbox-Tests

**Akzeptanzkriterien:**
- [ ] Alle Tests bestehen
- [ ] Keine aktiven Altbezeichnungen
- [ ] Keine Adapter in finalen Tests
- [ ] Blackbox bleibt isoliert (→ CHARTER §SR-07)
- [ ] Operational bleibt ohne wissenschaftliches Signal (→ CHARTER §SR-08)

<!-- @section id="4" title="MYRMEX-Neubau-Phasen (Phase 1–10)" type="prose" -->
## §4 MYRMEX-Neubau-Phasen (Phase 1–10)

<!-- @section id="4.1" title="Phase 1: Projekt-Setup + Datenverträge" type="implementation-phase" -->
### §4.1 Phase 1: Projekt-Setup + Datenverträge

**Aufgaben:**
- Repository-Struktur anlegen
- Requirements und Konfiguration erstellen
- Alle Vertragsmodelle definieren (→ CONTRACTS §1–§6)

**Akzeptanzkriterien:**
- [ ] Alle Modelle sind Pydantic-v2-konform
- [ ] Alle Enums vorhanden
- [ ] Idempotenzregeln korrekt (→ CONTRACTS §8)
- [ ] Routing-Graph enthält Pflichtfelder
- [ ] Gate-Modi vollständig
- [ ] Mindestens 20 Unit-Tests

<!-- @section id="4.2" title="Phase 2: Event-Sourcing + Archiv + Archivar" type="implementation-phase" -->
### §4.2 Phase 2: Event-Sourcing + Archiv + Archivar

**Aufgaben:**
- Atlas-Event-Store
- Snapshots
- Recovery
- Archivar für neue Ergebnisse
- Signal-Registry
- Kristallisation und Verfall

**Akzeptanzkriterien:**
- [ ] Duplikate werden verworfen
- [ ] Unvollständige Pakete werden nicht als Kristalle übernommen
- [ ] OPERATIONALE Abbrüche erzeugen keine wissenschaftlichen Signale (→ CHARTER §SR-08)
- [ ] Signal-Resolution korrekt
- [ ] Mindestens 30 Unit-Tests

<!-- @section id="4.3" title="Phase 3: Atlas + Kartograph" type="implementation-phase" -->
### §4.3 Phase 3: Atlas + Kartograph

**Aufgaben:**
- DBSCAN/UMAP-Logik
- fracture_score
- Zone-Health
- FULL_REBUILD
- NEUAUSRICHTEN
- Seed-Zonen
- Atlas-Versionierung

**Akzeptanzkriterien:**
- [ ] Unbekannte Dimensionen werden nicht als null oder 0 behandelt
- [ ] FULL_REBUILD atomar
- [ ] Alte Atlas-Version bleibt für laufende Quests gültig
- [ ] Mindestens 40 Unit-Tests

<!-- @section id="4.4" title="Phase 4: Transaktions-Schicht" type="implementation-phase" -->
### §4.4 Phase 4: Transaktions-Schicht

**Aufgaben:**
- WAL
- State Machine
- Recovery
- Crash-Sicherheit

**Akzeptanzkriterien:**
- [ ] Recovery setzt Pakete in die korrekte Stufe zurück
- [ ] Keine übersprungenen Phasen
- [ ] Lease-TTL wird beachtet
- [ ] Mindestens 25 Unit-Tests

<!-- @section id="4.5" title="Phase 5: Resource Governor + HAL-Vertrag" type="implementation-phase" -->
### §4.5 Phase 5: Resource Governor + HAL-Vertrag

**Aufgaben:**
- Slot-Manager
- Governor
- ESTOP-Handler
- HAL-Interface
- Dummy-HAL

**Akzeptanzkriterien:**
- [ ] Zwei Pakete können nicht denselben Slot gleichzeitig belegen
- [ ] LEASE_DENIED löst keinen ESTOP aus (→ CHARTER §SR-09)
- [ ] ESTOP suspendiert betroffene Leases
- [ ] Pfad-Leases funktionieren
- [ ] Mindestens 30 Unit-Tests

<!-- @section id="4.6" title="Phase 6: Sicherheits-Gate" type="implementation-phase" -->
### §4.6 Phase 6: Sicherheits-Gate

**Aufgaben:**
- Richter
- Seher
- Circuit-Breaker
- Berufungsprozess
- Gate-Record

**Akzeptanzkriterien:**
- [ ] Richter fail-closed (→ CHARTER §SR-10)
- [ ] Seher ohne Evidenz → invalid veto
- [ ] Seher erzeugt niemals direkt rote Signale (→ CHARTER §SR-13)
- [ ] Circuit-Breaker greift
- [ ] Mindestens 35 Unit-Tests

<!-- @section id="4.7" title="Phase 7: Ideen-Pipeline" type="implementation-phase" -->
### §4.7 Phase 7: Ideen-Pipeline

**Aufgaben:**
- Vordenker
- Pre-Filter
- Lotse
- blocked_cache
- Pheromon-Gating
- QUARANTÄNE-Regeln

**Akzeptanzkriterien:**
- [ ] Adaptive Temperatur mit Obergrenze
- [ ] UNKNOWN-Dimensionen werden nicht hart verworfen
- [ ] Signal-Stack wird geprüft
- [ ] QUARANTÄNE erlaubt nur diagnostische Wegmarken
- [ ] Mindestens 35 Unit-Tests

<!-- @section id="4.8" title="Phase 8: Paket-Bau + Dispatch" type="implementation-phase" -->
### §4.8 Phase 8: Paket-Bau + Dispatch

**Aufgaben:**
- Quartiermeister
- Dispatcher
- Receiver
- Questor-Interface
- DummyQuestor

**Akzeptanzkriterien:**
- [ ] Korrekte Pakete aus Wegmarke
- [ ] Routing-Graph ist gerichtet
- [ ] Envelope wird gebaut
- [ ] Gate und Lease werden geprüft
- [ ] Keine produktiven nackten Paketübergaben
- [ ] Mindestens 25 Unit-Tests

<!-- @section id="4.9" title="Phase 9: Kanzler + Königin-Interface" type="implementation-phase" -->
### §4.9 Phase 9: Kanzler + Königin-Interface

**Aufgaben:**
- Lagebericht
- Weisungsprüfung
- SAFE_MODE
- policy_veto_review
- Audit-Log

**Akzeptanzkriterien:**
- [ ] Menschliche Königin wird niemals überstimmt (→ CHARTER §SR-11)
- [ ] SAFE_MODE funktioniert
- [ ] LLM-Königin-Fallback greift nach Konflikten
- [ ] Review nach definierten Zyklen
- [ ] Mindestens 20 Unit-Tests

<!-- @section id="4.10" title="Phase 10: Pipeline-Orchestrierung + End-to-End Integration" type="implementation-phase" -->
### §4.10 Phase 10: Pipeline-Orchestrierung + End-to-End Integration

**Aufgaben:**
- Orchestrator
- Event-Steuerung
- Bounded Queues
- Deadlock-Erkennung
- Alle Integrationstests

**Akzeptanzkriterien:**
- [ ] Alle Pflichttests bestehen
- [ ] Keine Endlosschleifen
- [ ] Keine Deadlocks
- [ ] Keine Blackbox im Gremium (→ CHARTER §SR-07)
- [ ] Mindestens 12 Integrationstests

<!-- @section id="4A" title="Atlas-Hybrid-Phasen (A1–A5)" type="prose" -->
## §4A Atlas-Hybrid-Phasen (A1–A5)

<!-- @section id="4A.1" title="Übersicht" type="prose" -->
### §4A.1 Übersicht

<!-- @table schema="atlas_milestones" -->
| Meilenstein | Phasen | Dauer (Schätzung) | Abhängigkeiten |
|-------------|--------|-------------------|----------------|
| Atlas-MS-1: Core & Topologie | A1–A2 | 5–7 Tage | MYRMEX Phase 1, Phase 3 |
| Atlas-MS-2: Governance & Frontier | A3–A4 | 4–6 Tage | Atlas-MS-1 |
| Atlas-MS-3: Domänen-Integration | A5 | 3–5 Tage | Atlas-MS-2, Questor MS-3 |

<!-- @section id="4A.2" title="Phase A1: Atlas-Core & Energiekonten" type="implementation-phase" -->
### §4A.2 Phase A1: Atlas-Core & Energiekonten

**Meilenstein:** Atlas-MS-1
**Dauer:** 2–3 Tage
**Abhängigkeiten:** MYRMEX Phase 1 (Verträge), Phase 3 (Atlas-Basis)

**Aufgaben:**
- `EvidenceEvent`-Verarbeitung im Kartographen implementieren
- Energiekonten (`support_energy`, `conflict_energy`, `coverage_energy`, `diagnostic_energy`) führen
- `fracture_score`, `support_confidence`, `uncertainty_score` berechnen
- Zone-Health-Zustandsmaschine (`UNEXPLORED`, `EXPLORED_INCONCLUSIVE`, `HEALTHY`, `DEGRADED`, `CRITICAL`, `LOCKED`) implementieren
- Sicherstellen, dass `OPERATIONAL` keine wissenschaftlichen Signale erzeugt
- Sicherstellen, dass `SAFETY` keine Kristalle/Signale aus Questor erzeugt

**Akzeptanzkriterien:**
- [ ] Leere Zone ist `UNEXPLORED` oder `EXPLORED_INCONCLUSIVE`, niemals automatisch `HEALTHY`
- [ ] ⬜ WEISS erzeugt `coverage_energy`, keine `support_energy`
- [ ] `fracture_score` ist `None`, wenn `evidence_mass < min_evidence_mass`
- [ ] Mindestens 30 Unit-Tests (Suite ATLAS-CTR, ATLAS-INT)

<!-- @section id="4A.3" title="Phase A2: Topologie & Semantik" type="implementation-phase" -->
### §4A.3 Phase A2: Topologie & Semantik

**Meilenstein:** Atlas-MS-1
**Dauer:** 3–4 Tage
**Abhängigkeiten:** Phase A1

**Aufgaben:**
- `TypedDimension` und `ZoneGeometry` implementieren (kontinuierlich, kategorisch, ordinal, conditional)
- `AtlasNode` und `AtlasEdge` (Wissensgraph) implementieren
- `ObjectiveFamily` und `MetricDefinition` für Multi-Objective-Forschung implementieren
- Kristallisationslogik (`crystallization_progress`, Bedingungen, Evidence-Class-Transfer) implementieren

**Akzeptanzkriterien:**
- [ ] Kategorische Dimensionen (z.B. Katalysator A/B) erzeugen keine falsche Fracture zwischen Zonen
- [ ] Multi-Objective Trade-offs (z.B. Yield vs. Purity) erzeugen keine automatische Fracture
- [ ] Sandbox-Evidenz (`evidence_class = SANDBOX`) bestätigt keine physischen Kristalle direkt
- [ ] Mindestens 30 Unit-Tests (Suite ATLAS-TOPO, ATLAS-SEM)

<!-- @section id="4A.4" title="Phase A3: DiagnosticResolution & SafetyConstraint" type="implementation-phase" -->
### §4A.4 Phase A3: DiagnosticResolution & SafetyConstraint

**Meilenstein:** Atlas-MS-2
**Dauer:** 2–3 Tage
**Abhängigkeiten:** Atlas-MS-1

**Aufgaben:**
- `DiagnosticResolution` implementieren (Outcomes: CONFIRMS, EXPLAINS, RESOLVES, INCONCLUSIVE)
- Auditierte Gewichtsanpassung bei `EXPLAINS_CONTRADICTION` (kein Löschen von Evidenz)
- `SafetyConstraint` implementieren (persistent, kein Decay, manuelle Freigabe)
- `ExclusionConstraint` implementieren (Negativ-Wissen, harte/weiche Grenzen)
- `LOCKED`-Zustand und Governance-Override implementieren

**Akzeptanzkriterien:**
- [ ] `SafetyConstraint` unterliegt keinem automatischen Decay
- [ ] Aktive `SafetyConstraint` setzt `frontier_score = 0`
- [ ] `DiagnosticResolution` mit `EXPLAINS` reduziert `conflict_energy` auditiert
- [ ] Mindestens 20 Unit-Tests (Suite ATLAS-DIAG, ATLAS-SAF)

<!-- @section id="4A.5" title="Phase A4: FrontierEngine & ExplorationPolicy" type="implementation-phase" -->
### §4A.5 Phase A4: FrontierEngine & ExplorationPolicy

**Meilenstein:** Atlas-MS-2
**Dauer:** 2–3 Tage
**Abhängigkeiten:** Atlas-MS-1, A3

**Aufgaben:**
- `FrontierEngine` implementieren (Trigger, harte Filter, Score-Berechnung)
- `FrontierCandidate` mit `FrontierRationale` (strukturierte Begründung) erzeugen
- `ResearchTopic` und Zustandsmaschine (PROPOSED, ACTIVE, SATURATED, BLOCKED, ARCHIVED) implementieren
- `ExplorationPolicy` (Exploitation/Exploration-Balance) implementieren

**Akzeptanzkriterien:**
- [ ] `LOCKED` oder harte `SafetyConstraint` verhindert jede Frontier
- [ ] Quarantäne ohne Diagnose-Budget erzeugt keine normalen Frontiers
- [ ] `FrontierCandidate` enthält zwingend eine maschinenlesbare `rationale`
- [ ] `ResearchTopic` wird deterministisch auf `SATURATED` gesetzt
- [ ] Mindestens 25 Unit-Tests (Suite ATLAS-FRNT, ATLAS-TOP)

<!-- @section id="4A.6" title="Phase A5: Domänen-Integration & Regression" type="implementation-phase" -->
### §4A.6 Phase A5: Domänen-Integration & Regression

**Meilenstein:** Atlas-MS-3
**Dauer:** 3–5 Tage
**Abhängigkeiten:** Atlas-MS-2, Questor MS-3 (Data & Results)

**Aufgaben:**
- Integration der Chemie-Domäne (Katalysator-Temperatur-Optimierung)
- Integration der Biologie-Domäne (Zellkultur, Batch-Effekte, Inkubation)
- Integration der Physik-Domäne (Sensor-Kalibrierung, Messunsicherheit, ValidityWindow)
- Integration der ML-Domäne (Hyperparameter, Dataset-Versionen, OOM als Operational)
- Anpassung der bestehenden Regressions-Tests (Suite R) an die neue Atlas-Logik

**Akzeptanzkriterien:**
- [ ] Alle 4 Domänen-Beispiele laufen korrekt mit Atlas-Hybrid
- [ ] Bestehende Regressions-Tests (Suite R) sind migriert und bestehen
- [ ] Keine Endlosschleifen in der Frontier-Engine
- [ ] Mindestens 15 Integrationstests (Suite ATLAS-DOM)

<!-- @section id="4B" title="Strategic-Layer-Phasen (S1–S3)" type="prose" -->
## §4B Strategic-Layer-Phasen (S1–S3)

<!-- @section id="4B.1" title="Übersicht" type="prose" -->
### §4B.1 Übersicht

<!-- @table schema="strat_milestones" -->
| Meilenstein | Phasen | Dauer (Schätzung) | Abhängigkeiten |
|-------------|--------|-------------------|----------------|
| Strat-MS-1: ControlState & Achsen | S1 | 3–5 Tage | MYRMEX Phase 1, CONTRACTS §6.11 |
| Strat-MS-2: Kanzler & DTT | S2 | 4–5 Tage | Strat-MS-1, Atlas-MS-1 |
| Strat-MS-3: Königin & Integration | S3 | 3–5 Tage | Strat-MS-2, Atlas-MS-2 |

<!-- @section id="4B.2" title="Phase S1: ControlState-Manager & Achsen-Zustandsmaschine" type="implementation-phase" -->
### §4B.2 Phase S1: ControlState-Manager & Achsen-Zustandsmaschine

**Meilenstein:** Strat-MS-1
**Dauer:** 3–5 Tage
**Abhängigkeiten:** MYRMEX Phase 1 (Verträge), CONTRACTS §6.11 (Strategic-Layer-Verträge)

**Aufgaben:**
- `ControlState`-Manager implementieren (CONTRACTS §6.11.1)
- 4-Achsen-Zustandsmaschine implementieren (SafetyAxis, ResourceAxis, ResearchAxis, GovernanceAxis)
- `AxisTransition`-Verwaltung (CONTRACTS §6.11.2)
- `ControlStateLog`-Persistenz (CONTRACTS §6.11.3)
- SL-AX-ATOMIC implementieren (GREMIUM_STRATEGY.md §34)
- Severity-Ordnung implementieren (GREMIUM_STRATEGY.md §34.1)
- Closure-Regeln CT-1..CT-10 implementieren (GREMIUM_STRATEGY.md §34.2)
- Parameter-Besitz-Matrix implementieren (GREMIUM_STRATEGY.md §31)
- Validitätsmatrix implementieren (GREMIUM_STRATEGY.md §30)
- Liveness-Watchdog implementieren (GREMIUM_STRATEGY.md §33)
- Speicherorte anlegen: `data/governance/control_state/`

**Akzeptanzkriterien:**
- [ ] ControlState-Tupel wird korrekt verwaltet
- [ ] SL-AX-ATOMIC: Simultane Transitionen werden atomar committet
- [ ] SL-AX-ATOMIC: Ungültige Ziel-Tupel werden verworfen (fail-closed)
- [ ] Alle 10 Closure-Regeln (CT-1..CT-10) feuern korrekt
- [ ] Parameter-Besitz-Matrix: Kein Achsen-Parameter wird von einer fremden Achse gesetzt
- [ ] Mindestens 40 Unit-Tests (Suite STRAT-AX)

<!-- @section id="4B.3" title="Phase S2: Kanzler-Implementierung (DTT, Blocklists, Validierung)" type="implementation-phase" -->
### §4B.3 Phase S2: Kanzler-Implementierung (DTT, Blocklists, Validierung)

**Meilenstein:** Strat-MS-2
**Dauer:** 4–5 Tage
**Abhängigkeiten:** Strat-MS-1, Atlas-MS-1 (Core & Topologie)

**Aufgaben:**
- Validierungspipeline v2 implementieren (GREMIUM_STRATEGY.md §7, 10 Stufen)
- DirectiveTranslationTable (DTT) implementieren (GREMIUM_STRATEGY.md §8)
- Intent-Verfügbarkeit implementieren (GREMIUM_STRATEGY.md §32)
- Konfliktdetektor & NO_ACTION implementieren (GREMIUM_STRATEGY.md §9)
- Briefing-Erzeugung implementieren (GREMIUM_STRATEGY.md §18)
- Mensch-Schnittstelle implementieren (GREMIUM_STRATEGY.md §17)
- SL-SAF-7 implementieren (SAFE_MODE-Exit-Pfad)
- Budget-Modell implementieren (GREMIUM_STRATEGY.md §23)
- Speicherorte anlegen: `data/governance/briefings/`, `data/governance/directives/`, `data/governance/budget/`, `data/human_inbox/`

**Akzeptanzkriterien:**
- [ ] Validierungspipeline: Alle 10 Stufen funktionieren in fester Reihenfolge
- [ ] DTT: Alle 14 Intents werden korrekt übersetzt
- [ ] Intent-Verfügbarkeit: UNLOCK_BUDGET nur bei BUDGET_EXHAUSTED verfügbar
- [ ] Briefing: Kein security_mode, keine Hybrid-Referenzen im Briefing
- [ ] SL-SAF-7: SAFE_MODE → NORMAL nur via HumanResponseFile.unlock_decision
- [ ] Mindestens 55 Unit-Tests (Suite STRAT-KANZ)

<!-- @section id="4B.4" title="Phase S3: Königin-Integration & End-to-End" type="implementation-phase" -->
### §4B.4 Phase S3: Königin-Integration & End-to-End

**Meilenstein:** Strat-MS-3
**Dauer:** 3–5 Tage
**Abhängigkeiten:** Strat-MS-2, Atlas-MS-2 (Governance & Frontier)

**Aufgaben:**
- Constitutional Anchor Protocol implementieren (GREMIUM_STRATEGY.md §3)
- StrategicDirective-Verarbeitung implementieren (CONTRACTS §6.11.5–§6.11.6)
- RoyalLog implementieren (CONTRACTS §6.11.8)
- Symptom-Trigger implementieren (GREMIUM_STRATEGY.md §10)
- Signal-Semantik implementieren (GREMIUM_STRATEGY.md §11)
- Missions-Bootstrap implementieren (GREMIUM_STRATEGY.md §6)
- Dimensions-Lebenszyklus implementieren (GREMIUM_STRATEGY.md §15)
- Capability-Gap & CAPEX implementieren (GREMIUM_STRATEGY.md §16)
- Digital-Twin-Loop (strategisch) implementieren (GREMIUM_STRATEGY.md §14)
- End-to-End-Integration mit Pipeline (GREMIUM.md)

**Akzeptanzkriterien:**
- [ ] Constitutional Anchor: Königin erhält exakt 3 Kontextblöcke
- [ ] StrategicDirective: Alle 14 Intent-Submodelle validieren korrekt
- [ ] Symptom-Trigger: Alle 10 SymptomTypes werden korrekt erzeugt
- [ ] Digital-Twin-Loop: TWIN_DRIFT erzeugt SymptomEvent
- [ ] End-to-End: Briefing → Directive → DTT → Policy-Wirkung funktioniert
- [ ] Mindestens 60 Unit-Tests + 15 Integrationstests (Suite STRAT-KOEN, STRAT-E2E)

<!-- @section id="5" title="HAL-Phasen (HAL-H0 bis HAL-H6)" type="prose" -->
## §5 HAL-Phasen (HAL-H0 bis HAL-H6)

<!-- @table schema="hal_phases" -->
| Phase | Name | Aufgaben (Kurz) | Akzeptanzkriterien (Kurz) |
|-------|------|-----------------|---------------------------|
| HAL-H0 | HAL-Vertrag bestätigen | Minimalvertrag abgleichen | Strukturversion 1.1.1 maßgeblich |
| HAL-H1 | Interface & Datenmodelle | `hal_interface.py`, Pydantic-Modelle | 40 Unit-Tests |
| HAL-H2 | Slot- & Lease-Logik | Slot-State, Mutex, Timeout | 25 Unit-Tests |
| HAL-H3 | Zonen-Mutex & Prozess-Logik | Zone-State, Langzeit-Prozess | 30 Unit-Tests |
| HAL-H4 | ESTOP & Hardware-Interlocks | ESTOP-Zustandsmaschine | 25 Unit-Tests |
| HAL-H5 | Compute-Modell & Parameter-Schema | Compute-Ressourcen, Schema-Registry | 20 Unit-Tests |
| HAL-H6 | Dummy-HAL & Integration | Vollständiger Dummy-HAL | 25 Integrationstests |

<!-- @section id="6" title="Questor-Phasen (Q0–Q18)" type="prose" -->
## §6 Questor-Phasen (Q0–Q18)

<!-- @section id="6.1" title="Übersicht" type="prose" -->
### §6.1 Übersicht

<!-- @table schema="questor_milestones" -->
| Meilenstein | Phasen | Dauer (Schätzung) | Abhängigkeiten |
|-------------|--------|-------------------|----------------|
| MS-1: Foundation | Q0–Q3 | 7–10 Tage | Keine |
| MS-2: Core Questor | Q4–Q8 | 12–18 Tage | MS-1, HAL-H1 |
| MS-3: Data & Results | Q9–Q10 | 5–7 Tage | MS-2 |
| MS-4: Operational | Q11–Q13 | 4–7 Tage | MS-3 |
| MS-5: Integration | Q14 | 3–5 Tage | MS-4, MYRMEX Phase 8 |
| MS-6: Tests | Q15–Q18 | 13–20 Tage | MS-5 |

*Hinweis: Die detaillierten Aufgaben und Akzeptanzkriterien für Q0–Q18 sind in der ursprünglichen Spezifikation definiert und umfassen Sanitization, Capability-Registry, Security-Mode, Facade, QuestCompass, Loop-Architektur, PolicyEvaluator, HAL-Bridge, Ledger, WAL, Result-Builder, Shutdown, Health-Monitoring, Trail-Map, Queue-Integration und die Testphasen.*

<!-- @section id="7" title="Meilensteine und Abhängigkeiten" type="prose" -->
## §7 Meilensteine und Abhängigkeiten

<!-- @section id="7.1c" title="Strategic-Layer-Meilensteine" type="prose" -->
### §7.1c Strategic-Layer-Meilensteine

<!-- @table schema="strat_milestones_deps" -->
| Meilenstein | Phasen | Dauer | Abhängigkeiten |
|-------------|--------|-------|----------------|
| Strat-MS-1: ControlState & Achsen | S1 | 3–5 Tage | MYRMEX Phase 1, CONTRACTS §6.11 |
| Strat-MS-2: Kanzler & DTT | S2 | 4–5 Tage | Strat-MS-1, Atlas-MS-1 |
| Strat-MS-3: Königin & Integration | S3 | 3–5 Tage | Strat-MS-2, Atlas-MS-2 |

<!-- @section id="7.2b" title="Strategic-Layer-Abhängigkeiten" type="prose" -->
### §7.2b Strategic-Layer-Abhängigkeiten

<!-- @table schema="strat_deps" -->
| Strat-Meilenstein | MYRMEX-Phase | Atlas-Phase | Questor-Phase | Bedingung |
|-------------------|--------------|-------------|---------------|-----------|
| Strat-MS-1 | Phase 1 (Verträge) | — | — | CONTRACTS §6.11 muss definiert sein |
| Strat-MS-2 | — | Atlas-MS-1 | — | ControlState muss funktionieren |
| Strat-MS-3 | — | Atlas-MS-2 | — | Kanzler muss funktionieren |

<!-- @section id="8" title="Kritischer Pfad" type="prose" -->
## §8 Kritischer Pfad

<!-- @section id="8.4" title="Strategic-Layer-Pfad" type="prose" -->
### §8.4 Strategic-Layer-Pfad

Der Strategic-Layer-Pfad ist:
`MYRMEX Phase 1 → S1 → S2 → S3 → MYRMEX Phase 10 (E2E)`

**Parallelisierung:**
- S1 kann parallel zu Atlas A1-A2 entwickelt werden (beide hängen nur von MYRMEX Phase 1 ab).
- S2 erfordert Atlas-MS-1 (A1-A2 abgeschlossen).
- S3 erfordert Atlas-MS-2 (A3-A4 abgeschlossen).
- S3 kann parallel zu Questor Q9-Q13 (MS-3 und MS-4) entwickelt werden.

<!-- @section id="9" title="Risikobewertung" type="prose" -->
## §9 Risikobewertung

<!-- @table schema="risk_matrix" -->
| # | Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|--------|--------------------|------------|------------|
| R13 | ControlState-Achsen erzeugen unerwartete Closure-Kaskaden | Mittel | Hoch | SL-AX-ATOMIC mit closure_max_iterations=5. Fail-Closed bei ungültigem Ziel-Tupel. Suite STRAT-AX. |
| R14 | Königin-LLM erzeugt Direktiven, die nicht zur Achsen-Situation passen | Mittel | Mittel | Intent-Verfügbarkeit (§32) blockiert unpassende Intents deterministisch. DTT validiert gegen ControlState. |

<!-- @section id="11" title="Test-Gates pro Phase" type="prose" -->
## §11 Test-Gates pro Phase

<!-- @section id="11.1" title="Test-Gates" type="prose" -->
### §11.1 Test-Gates

<!-- @table schema="test_gates" -->
| Gate | Bedingung |
|------|-----------|
| GATE-STRAT | Alle Strategic-Layer-Tests bestehen (Suite STRAT) |

<!-- @section id="11.2" title="Teststrategie pro Phase" type="prose" -->
### §11.2 Teststrategie pro Phase

<!-- @table schema="test_strategy" -->
| Phase | Test-Typ | Anzahl | Coverage-Ziel |
|-------|----------|--------|---------------|
| S1 | Unit-Tests (ControlState, Achsen) | 40 | 95% |
| S2 | Unit-Tests (Kanzler, DTT, Blocklists) | 55 | 90% |
| S3 | Unit-Tests + Integration (Königin, E2E) | 75 | 85% |
| Strategic Gesamt | | ~170 | ≥ 90% |

<!-- @section id="12" title="Akzeptanzkriterien für das Gesamtsystem" type="prose" -->
## §12 Akzeptanzkriterien für das Gesamtsystem

<!-- @table schema="acceptance_criteria" -->
| # | Kriterium | CHARTER-Referenz |
|---|-----------|-----------------|
| 37 | Alle Strategic-Layer-Tests bestehen (Suite STRAT) | — |
| 38 | Strategic-Layer-Phasen S1–S3 abgeschlossen | — |
| 39 | ControlState wird atomar verwaltet (SL-AX-ATOMIC) | CHARTER §SR-55 |
| 40 | Alle 10 Closure-Regeln (CT-1..CT-10) funktionieren | — |
| 41 | Intent-Verfügbarkeit wird korrekt durch Blocklists gesteuert | — |
| 42 | SAFE_MODE → NORMAL nur via menschliche Freigabe (SL-SAF-7) | CHARTER §SR-11 |
| 43 | ESTOP_LOCKED → NORMAL nur via autorisierten Sicherheitsprozess | CHARTER §SR-05 |
| 44 | Königin erhält exakt 3 Kontextblöcke (Constitutional Anchor) | CHARTER §SR-13 |
| 45 | Kein security_mode im Briefing | CHARTER §SR-29 |
| 46 | Questor und HAL kennen keine Strategic-Layer-Verträge | CHARTER §SR-04 |

<!-- @section id="14" title="Sicherheitsregeln für die Implementierung" type="prose" -->
## §14 Sicherheitsregeln für die Implementierung

<!-- @section id="14.1" title="Implementierungsregeln" type="prose" -->
### §14.1 Implementierungsregeln

<!-- @table schema="implementation_rules" -->
| # | Regel | CHARTER-Referenz |
|---|-------|-----------------|
| IR-16 | Strategic-Layer-Implementierung erzeugt keine neuen Sicherheitsregeln | CHARTER §3 |
| IR-17 | Strategic-Layer-Implementierung definiert keine neuen Datenverträge | CONTRACTS §6.11 |
| IR-18 | ControlState-Parameter werden nur über die Besitzer-Achse gesetzt | GREMIUM_STRATEGY §31 |
| IR-19 | Königin-LLM ist stateless (kein persistenter Gesprächsverlauf) | GREMIUM_STRATEGY §3 |

<!-- @section id="14.2" title="Verbotene Patterns" type="prose" -->
### §14.2 Verbotene Patterns

<!-- @table schema="forbidden_patterns" -->
| # | Pattern | CHARTER-Referenz |
|---|---------|-----------------|
| VP-21 | Königin-LLM mit persistentem Gesprächsverlauf | GREMIUM_STRATEGY §27 |
| VP-22 | LLM-Einsatz im Kanzler | GREMIUM_STRATEGY §27 |
| VP-23 | Direkter Atlas-Zugriff der Königin | GREMIUM_STRATEGY §27 |
| VP-24 | Achsen-Parameter direkt setzen statt über ControlState | GREMIUM_STRATEGY §27 |
| VP-25 | security_mode im strategischen Briefing | CHARTER §SR-29 |

<!-- @section id="15" title="Zusammenfassung der Spezifikation" type="prose" -->
## §15 Zusammenfassung der Spezifikation

<!-- @table schema="summary" -->
| Aspekt | Definition |
|--------|-----------|
| Phasen | Q0–Q18 (19 Questor), M0–M5 (6 MYRMEX-Migration), Phase 1–10 (10 MYRMEX-Neubau), A1–A5 (5 Atlas-Hybrid), S1–S3 (3 Strategic Layer), HAL-H0 bis HAL-H6 (7 HAL) |
| Meilensteine | MS-1 bis MS-6 (6 Questor), Atlas-MS-1 bis Atlas-MS-3 (3 Atlas), Strat-MS-1 bis Strat-MS-3 (3 Strategic) |
| Gesamtdauer | ~44–67 Tage (Questor), ~12–18 Tage (Atlas), ~10–15 Tage (Strategic), ~22–30 Tage (3 Entwickler) |
| Test-Anzahl | ~541 + ~170 Strategic = ~711 Tests |
| Coverage-Ziel | ≥ 88% gesamt, ≥ 95% sicherheitskritisch |
| Kritischer Pfad | Q0 → Q1 → Q5 → Q7 → Q8 → Q9 → Q10 → Q11 → Q14 → Q15 → Q16 → Q17 → Q18 |
| Atlas-Pfad | MYRMEX Phase 3 → A1 → A2 → A3 → A4 → A5 → MYRMEX Phase 10 |
| Strategic-Pfad | MYRMEX Phase 1 → S1 → S2 → S3 → MYRMEX Phase 10 |
| Externe Abhängigkeiten | MYRMEX Phase 1, 2, 3, 5, 8; HAL Phase HAL-H1, HAL-H6; Questor MS-3; CONTRACTS §6.11 |
| Risiken | 12 + 2 Strategic = 14 identifizierte Risiken |
| Akzeptanzkriterien | 36 + 10 Strategic = 46 Kriterien |
| Test-Gates | 9 + GATE-STRAT = 10 Gates |

<!-- @section id="16" title="Dokumentenhierarchie" type="prose" -->
## §16 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `ops/` und referenziert:
- `foundation/CHARTER.md` für Sicherheitsregeln (CHARTER §SR-XX)
- `foundation/CONTRACTS.md` für Datenverträge (CONTRACTS §X.X)
- `specs/QUESTOR.md` für Questor-spezifische Details
- `specs/HAL.md` für HAL-spezifische Details
- `specs/GREMIUM.md` für Gremium-spezifische Details (inkl. Atlas-Hybrid-System §6)
- `ops/VALIDATION.md` für Teststrategie und Akzeptanzkriterien
- `specs/GREMIUM_STRATEGY.md` für Strategic-Layer-Regeln (Achsen, ControlState, Kanzler/Königin)

Regel: Änderungen an Phasen in diesem Dokument erfordern eine Versionsänderung und eine Überprüfung der referenzierten Dokumente.