---
doc_id: specs/HAL.md
doc_type: spec
version: 1.1.0-atlas-hyb.1
status: BINDEND
schema_version: spec-format-1.0
layer: specs
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1-twin.1
conflict_rule: [CHARTER, CONTRACTS, THIS_DOC]
roles_defined:
  - hal_interface
  - device_adapter
  - slot_state_store
  - process_state_store
  - zone_lock_manager
  - estop_handler
  - operational_audit_writer
  - dummy_hal
roles_referenced:
  - questor
  - resource_governor
dataflows_defined:
  - hal_command_flow
  - process_lifecycle_flow
  - estop_response_flow
last_modified: 2026-08-21
---

<!-- @section id="0" title="Geltung und Änderungsregeln" type="meta" -->
# 🔌 HAL — HARDWARE ABSTRACTION LAYER

## §0 Geltung und Änderungsregeln

Dieses Dokument definiert die vollständige HAL-Spezifikation.

Regel: Dieses Dokument referenziert Verträge aus `CONTRACTS.md` und Sicherheitsregeln aus `CHARTER.md`.
Es definiert keine neuen Verträge und keine neuen Sicherheitsregeln.

Konfliktregel: Bei Widersprüchen gilt `CHARTER.md` > `CONTRACTS.md` > dieses Dokument.

<!-- @section id="0.1" title="Änderungsantrag ATLAS-HYB-1.0.0 — HAL-Kompatibilitätsbestätigung" type="change-request" -->
### §0.1 Änderungsantrag ATLAS-HYB-1.0.0 — HAL-Kompatibilitätsbestätigung

Dieser Änderungsantrag bestätigt die Kompatibilität von HAL mit dem Atlas-Hybrid-System.

HAL erfordert keine funktionalen Änderungen durch das Atlas-Hybrid-System.

Begründung:
- Das Atlas-Hybrid-System ist eine Erweiterung des Gremiums (Schicht 4) und des Atlas.
- HAL ist Schicht 1 und interpretiert keine wissenschaftlichen Ziele (→ CHARTER §SR-08).
- HAL schreibt nicht in den Atlas (→ CHARTER §SR-04).
- HAL schreibt nicht in das Archiv (→ CHARTER §SR-04).
- Die Atlas-Hybrid-Felder (`atlas_expectation_ref`, `objective_family_ref`, `frontier_candidate_ref`, `evidence_kind`, `evidence_class` usw.) existieren ausschließlich auf der Paket- und Gremium-Ebene.
- Diese Felder werden von der HAL-Bridge (→ specs/QUESTOR.md §8) nicht in `HALCommand.parameters` oder `ProcessCommand.parameters` übersetzt.

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge.
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln.
- Dieser Änderungsantrag fügt keine neuen HAL-Funktionen hinzu.
- Die bestehende HAL-Schnittstelle (16 Funktionen) bleibt unverändert.
- Die bestehende Fehlerklassentrennung (OPERATIONAL / SAFETY) bleibt unverändert.

<!-- @section id="1" title="HAL-Übersicht und Grundprinzipien" type="prose" -->
## §1 HAL-Übersicht und Grundprinzipien

<!-- @section id="1.1" title="Position im System" type="prose" -->
### §1.1 Position im System

<!-- @role id="hal_interface" layer="1" llm="false" writes_to="operational_logs" reads_from="questor_commands" -->
HAL ist Schicht 1 im MYRMEX-System (→ CHARTER §1.1).

```
┌─────────────────────────────────────────────────────────────────┐
│                        QUESTOR (Schicht 2)                       │
│  QuestCompass → PolicyEvaluator → HAL-Bridge                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HALCommand / ProcessCommand
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     HAL INTERFACE (Schicht 1)                    │
│  get_environment_manifest() · execute_command() · ...           │
│  Slot State Store · Zone Lock Manager · ESTOP Handler           │
└───────────────────────────────┬─────────────────────────────────┘
                                │ DeviceCommand
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              DEVICE ADAPTER / COMPUTE ADAPTER / DUMMY            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PHYSIS / COMPUTE (Schicht 0)                  │
└─────────────────────────────────────────────────────────────────┘
```

<!-- @section id="1.2" title="Die sechs HAL-Grundprinzipien" type="prose" -->
### §1.2 Die sechs HAL-Grundprinzipien

<!-- @table schema="core_principles" -->
| # | Prinzip | Bedeutung | CHARTER-Referenz |
|---|---------|-----------|-----------------|
| 1 | Dünne Schicht | HAL bleibt bewusst dünn. Intelligenz bleibt bei Gremium, Questor und Resource Governor. | — |
| 2 | Deterministisch vor LLM | HAL enthält keine LLM-Logik. Alle HAL-Entscheidungen sind deterministisch. | <!-- @ref target="CHARTER §2" type="security-rule" -->CHARTER §2 |
| 3 | Fail-Closed | Wenn ein Zustand nicht sicher bestimmt werden kann: kein Kommando ausführen, keinen Slot freigeben, keine Lease akzeptieren. | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->CHARTER §SR-10 |
| 4 | Keine wissenschaftliche Interpretation | HAL erhält keine Forschungsziele. HAL meldet keine wissenschaftlichen Kategorien. | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| 5 | Keine Lease-Vergabe | HAL vergibt keine Leases. Leases kommen ausschließlich vom Resource Governor. | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| 6 | Keine Blackbox-Übergabe | HAL gibt keine Blackbox-Inhalte an das Gremium weiter. | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |

<!-- @section id="1.3" title="Was HAL DARF" type="prose" -->
### §1.3 Was HAL DARF

<!-- @table schema="role_permissions" role="hal_interface" -->
| Erlaubt | Begründung |
|---------|-----------|
| Hardware- oder Compute-Kommandos ausführen | Kernaufgabe |
| Slot-Zustände melden | Zustandsprüfung |
| Lease-Referenzen formal prüfen oder durch den Resource Governor prüfen lassen | Lease-Validierung |
| ESTOP melden und ESTOP-Zustände verwalten | Sicherheitsfunktion |
| Hardware-Interlocks erkennen und melden | Sicherheitsfunktion |
| Zonen-Locks anfragen und verwalten | Kollisionsvermeidung |
| Langzeit-Prozesse verwalten (Start, Hold, Resume, Abort) | Prozessmanagement |
| Technische Fehler operational melden | Fehlerbehandlung |
| Sicherheitsfehler als SAFETY melden | Fehlerbehandlung |
| Kommandos idempotent behandeln | Crash-Sicherheit |
| Audit-Logs für Operationen schreiben | Nachvollziehbarkeit |
| Dummy-Modi für Tests bereitstellen | Testbarkeit |
| Unklare Zustände nach Crash als unsicher melden | Fail-Closed |

<!-- @section id="1.4" title="Was HAL NICHT DARF" type="prose" -->
### §1.4 Was HAL NICHT DARF

<!-- @table schema="role_permissions" role="hal_interface" -->
| Verboten | CHARTER-Referenz |
|----------|-----------------|
| Leases vergeben | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| Leases verlängern | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| Leases eigenmächtig erneuern | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| Wissenschaftliche Ziele interpretieren | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| Atlas-Signale schreiben | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Archiv-Einträge schreiben | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Kristalle erzeugen | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Wegmarken erzeugen | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Ideen bewerten | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Questor-Logik ersetzen | — |
| ESTOP eigenmächtig zurücksetzen | <!-- @ref target="CHARTER §SR-05" type="security-rule" -->CHARTER §SR-05 |
| Hardware-Interlocks eigenmächtig zurücksetzen | <!-- @ref target="CHARTER §SR-05" type="security-rule" -->CHARTER §SR-05 |
| Blackbox-Inhalte an das Gremium weitergeben | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |
| Finale Sicherheitsfreigaben erteilen | <!-- @ref target="CHARTER §SR-13" type="security-rule" -->CHARTER §SR-13 |
| LLM-Entscheidungen als sicherheitskritische Endentscheidung nutzen | <!-- @ref target="CHARTER §SR-13" type="security-rule" -->CHARTER §SR-13 |
| Zonen-Locks eigenmächtig vergeben | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| Atlas-Hybrid-Felder in HALCommand.parameters schreiben | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04, §SR-08 |
| Atlas-Hybrid-Felder in ProcessCommand.parameters schreiben | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04, §SR-08 |
| expectation_ref, frontier_candidate_ref oder evidence_kind interpretieren | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| FrontierCandidates oder ResearchTopics verarbeiten | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| DiagnosticResolution oder SafetyConstraint auflösen | <!-- @ref target="CHARTER §SR-05" type="security-rule" -->CHARTER §SR-05 |

<!-- @section id="2" title="HAL-Knoten und Architektur" type="prose" -->
## §2 HAL-Knoten und Architektur

<!-- @section id="2.1" title="HAL Interface" type="prose" -->
### §2.1 HAL Interface

<!-- @role id="hal_interface" layer="1" llm="false" writes_to="hal_results" reads_from="hal_commands" -->
Der zentrale Vertragsendpunkt. Bietet die 16 Funktionen aus → CONTRACTS §3.12.

<!-- @section id="2.2" title="Device Adapter" type="prose" -->
### §2.2 Device Adapter

<!-- @role id="device_adapter" layer="1" llm="false" writes_to="device_results" reads_from="device_commands" -->
Der Device Adapter ist die geräte- oder compute-spezifische Umsetzung.

Mögliche Adapter:
- `DummyAdapter`
- `SimulationAdapter`
- `ComputeAdapter`
- `LabHardwareAdapter`
- `SandboxAdapter`
- `LiquidHandlerAdapter`
- `ReactorAdapter`
- `IncubatorAdapter`
- `GPUClusterAdapter`

Regeln:
- Der Adapter darf keine Lease vergeben (→ CHARTER §SR-06).
- Der Adapter darf keine Sicherheitsregeln umgehen.

<!-- @section id="2.3" title="Slot State Store" type="prose" -->
### §2.3 Slot State Store

<!-- @role id="slot_state_store" layer="1" llm="false" writes_to="slot_states" reads_from="slot_commands" -->
Verwaltet Slot-Zustände (→ CONTRACTS §3.7).

Regel: Quelle der Wahrheit für Leases ist nicht HAL, sondern der Resource Governor.
HAL darf Slot-Zustände technisch führen, aber Lease-Gültigkeit nicht eigenmächtig erzeugen.

<!-- @section id="2.4" title="Process State Store" type="prose" -->
### §2.4 Process State Store

<!-- @role id="process_state_store" layer="1" llm="false" writes_to="process_states" reads_from="process_commands" -->
Verwaltet Langzeit-Prozess-Zustände (→ CONTRACTS §3.9).

Für jedes aktive Gerät oder Compute-Job wird ein Prozesszustand geführt:
- `process_id`
- `device_job_id`
- `process_state`
- `resume_token`
- `safe_hold_policy`
- `stage_release_policy`

<!-- @section id="2.5" title="Zone Lock Manager" type="prose" -->
### §2.5 Zone Lock Manager

<!-- @role id="zone_lock_manager" layer="1" llm="false" writes_to="zone_states" reads_from="zone_requests" -->
Verwaltet zonenbasierte Mutex-Locks (→ CONTRACTS §3.8).

Zonen können sein:
- Gemeinsame Schienen
- Kinematische Kollisionsräume
- Plattenpositionen
- Sicherheitsräume

Regel: HAL fragt Zonen-Locks beim Resource Governor an.
HAL verwaltet Zonen-Locks nicht eigenmächtig (→ CHARTER §SR-06).

<!-- @section id="2.6" title="ESTOP Handler" type="prose" -->
### §2.6 ESTOP Handler

<!-- @role id="estop_handler" layer="1" llm="false" writes_to="estop_states" reads_from="estop_events" -->
Verwaltet:
- ESTOP-Ereignisse
- ESTOP-Zustände
- Hardware-Interlock-Ereignisse
- Betroffene Slots
- Suspendierte Leases
- Audit-Events
- Reset-Anfragen

<!-- @section id="2.7" title="Operational Audit Writer" type="prose" -->
### §2.7 Operational Audit Writer

<!-- @role id="operational_audit_writer" layer="1" llm="false" writes_to="operational_logs" reads_from="hal_events" -->
Schreibt HAL-Ereignisse nach `data/operational_logs/`.

Regel: Diese Logs sind operational, nicht wissenschaftlich (→ CHARTER §SR-08).

<!-- @section id="3" title="Slot-Management" type="prose" -->
## §3 Slot-Management

<!-- @section id="3.1" title="Slot-Zustandsmaschine" type="state-machine" machine="slot_state" -->
### §3.1 Slot-Zustandsmaschine

<!-- @ref target="foundation/CONTRACTS.md §7.2" type="contract" -->
→ Siehe CONTRACTS §7.2 für die vollständige Zustandsmaschine.

<!-- @table schema="state_machine_states" machine="slot_state" -->
| Zustand | Bedeutung |
|---------|-----------|
| FREE | Slot verfügbar |
| RESERVED | Slot reserviert |
| ACTIVE | Slot aktiv |
| ERROR | Fehlerzustand |
| ESTOP_SUSPENDED | ESTOP aktiv |
| INTERLOCKED | Hardware-Interlock aktiv |
| MAINTENANCE | Wartung |
| OFFLINE | Nicht erreichbar |

<!-- @section id="3.2" title="Übergangstabelle" type="prose" -->
### §3.2 Übergangstabelle

<!-- @table schema="state_transitions" machine="slot_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| FREE | RESERVED | Gültige Lease-Reservierung |
| RESERVED | ACTIVE | Kommando akzeptiert |
| ACTIVE | FREE | Erfolgreiche Ausführung und Freigabe |
| ACTIVE | ERROR | Fehler oder unklarer Zustand |
| ACTIVE | ESTOP_SUSPENDED | ESTOP |
| ACTIVE | INTERLOCKED | Hardware-Interlock |
| RESERVED | FREE | Lease abgelaufen oder widerrufen |
| ERROR | FREE | Erfolgreiche Reconciliation |
| ESTOP_SUSPENDED | FREE | ESTOP zurückgesetzt und Lease gültig |
| INTERLOCKED | FREE | Hardware-Interlock zurückgesetzt, safe_state_verified, manuelle Bestätigung |
| MAINTENANCE | OFFLINE | Wartung beendet oder Gerät getrennt |
| OFFLINE | FREE | Gerät wieder verfügbar und geprüft |

<!-- @section id="3.3" title="Harte Regel für INTERLOCKED" type="prose" -->
### §3.3 Harte Regel für `INTERLOCKED`

<!-- @ref target="CHARTER §SR-09" type="security-rule" -->
→ Siehe CHARTER §SR-09 für die ESTOP/Interlock-Regel.

- Kein `execute_command()`
- Keine automatische Reconciliation auf `FREE`
- Keine Rückkehr in `FREE` ohne manuelle Bestätigung
- `safe_state_verified` muss `true` sein
- `physical_reset_required` muss erfüllt sein

<!-- @section id="4" title="Zonen-Mutex-Modellierung" type="prose" -->
## §4 Zonen-Mutex-Modellierung

<!-- @section id="4.1" title="Zweck" type="prose" -->
### §4.1 Zweck

Die zonenbasierte Mutex-Modellierung dient dazu, gemeinsame physische Räume zu schützen:
- Gemeinsame Schienen
- Fahrwege
- Kinematische Kollisionsräume
- Plattenpositionen
- Sicherheitsräume

<!-- @section id="4.2" title="Zonen-Lock-Anfrage" type="dataflow" dataflow="zone_lock_request" -->
### §4.2 Zonen-Lock-Anfrage

<!-- @dataflow id="zone_lock_request" trigger="ZONE_LOCK_REQUESTED" source_role="hal_interface" target_role="resource_governor" -->
HAL fragt Zonen-Locks beim Resource Governor an.

<!-- @ref target="foundation/CONTRACTS.md §3.8" type="contract" -->
→ Siehe CONTRACTS §3.8 für den ZoneState-Vertrag.

<!-- @section id="4.3" title="Zonen-Lock-Antwort" type="prose" -->
### §4.3 Zonen-Lock-Antwort

<!-- @table schema="zone_lock_response" -->
| Status | Bedeutung |
|--------|-----------|
| GRANTED | Zonen-Lock gewährt |
| DENIED | Zonen-Lock abgelehnt |
| TIMEOUT | Zonen-Lock-Anfrage hat zu lange gedauert |

<!-- @section id="4.4" title="Fehlercodes" type="prose" -->
### §4.4 Fehlercodes

<!-- @table schema="error_codes" category="zone_lock" -->
| Fehler | Bedeutung | Fehlerklasse |
|--------|-----------|-------------|
| ZONE_LOCK_UNAVAILABLE | Zonen-Lock ist nicht verfügbar | OPERATIONAL |
| ZONE_LOCK_TIMEOUT | Zonen-Lock-Anfrage hat zu lange gedauert | OPERATIONAL |
| ZONE_LOCK_DENIED | Zonen-Lock wurde abgelehnt | OPERATIONAL |
| ZONE_LOCK_EXPIRED | Zonen-Lock ist abgelaufen | OPERATIONAL |

<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08 für die Operational/Scientific-Trennung.

<!-- @section id="5" title="ESTOP und Hardware-Interlocks" type="prose" -->
## §5 ESTOP und Hardware-Interlocks

<!-- @section id="5.1" title="Auslösung" type="prose" -->
### §5.1 Auslösung

ESTOP darf ausgelöst werden durch:
- Physische Gefahr
- Sicherheitsgrenzwertverletzung
- Hardware-Interlock
- Externe Sicherheitskette
- Manuelle Sicherheitsauslösung
- Testauslösung im TEST-Modus

ESTOP darf nicht ausgelöst werden durch:
- Ressourcenkonflikt (→ CHARTER §SR-09)
- Lease-Konflikt (→ CHARTER §SR-09)
- Timeout ohne Sicherheitsbezug
- OOM ohne Sicherheitsbezug
- CUDA-OOM (→ CHARTER §SR-08)
- Wissenschaftlichen Fehlschlag (→ CHARTER §SR-08)

<!-- @section id="5.2" title="Hardware-Interlock vs Software-ESTOP" type="prose" -->
### §5.2 Hardware-Interlock vs Software-ESTOP

<!-- @table schema="estop_comparison" -->
| Merkmal | Software-ESTOP | Hardware-Interlock |
|---------|---------------|-------------------|
| origin | SOFTWARE | HARDWARE_INTERLOCK |
| Auslösung | Software entscheidet | Hardware zieht Stecker |
| Kommunikation | HAL kann antworten | HAL kann nicht antworten |
| Reset | Software-Reset möglich | Physischer Reset erforderlich |
| physical_reset_required | false | true |
| device_reachable | true | oft false |
| safe_state_verified | oft true | oft false |
| inspection_required | false | oft true |

<!-- @ref target="foundation/CONTRACTS.md §3.10" type="contract" -->
→ Siehe CONTRACTS §3.10 für den EstopState-Vertrag.
<!-- @ref target="foundation/CONTRACTS.md §3.11" type="contract" -->
→ Siehe CONTRACTS §3.11 für den HardwareInterlockEvent-Vertrag.

<!-- @section id="5.3" title="Wirkung" type="dataflow" dataflow="estop_response" -->
### §5.3 Wirkung

<!-- @dataflow id="estop_response" trigger="ESTOP_TRIGGERED" source_role="estop_handler" target_role="questor" -->
Bei `ACTIVE` oder `LATCHED`:
- Keine neuen Kommandos ausführen
- Aktive Kommandos kontrolliert stoppen
- Betroffene Slots auf `ESTOP_SUSPENDED` oder `INTERLOCKED`
- Betroffene Zonen auf `ESTOP_SUSPENDED` oder `INTERLOCKED`
- Betroffene Leases dem Resource Governor als suspendiert melden
- Questor erhält Sicherheitsabbruch
- Audit-Log wird geschrieben

<!-- @ref target="CHARTER §SR-09" type="security-rule" -->
→ Siehe CHARTER §SR-09 für die ESTOP-Regel.

<!-- @section id="5.4" title="Rücksetzung" type="prose" -->
### §5.4 Rücksetzung

ESTOP darf nicht zurückgesetzt werden durch:
- Questor (→ CHARTER §SR-05)
- LLM (→ CHARTER §SR-13)
- Automatischen Retry
- Device Adapter

ESTOP darf zurückgesetzt werden durch:
- Autorisierten Sicherheitsprozess
- Menschliche Freigabe
- Definierten Audit-Prozess
- Optional Kanzler-/Sicherheitsfreigabe, falls konfiguriert

Für Hardware-Interlocks gilt zusätzlich:
- `physical_reset_required` muss erfüllt sein
- `safe_state_verified` muss `true` sein
- `inspection_required` muss erfüllt sein
- Manuelle Bestätigung ist zwingend

<!-- @section id="5.5" title="ESTOP-Zustandsmaschine" type="state-machine" machine="estop_state" -->
### §5.5 ESTOP-Zustandsmaschine

<!-- @ref target="foundation/CONTRACTS.md §7.5" type="contract" -->
→ Siehe CONTRACTS §7.5 für die vollständige Zustandsmaschine.

<!-- @table schema="state_machine_states" machine="estop_state" -->
| Zustand | Bedeutung |
|---------|-----------|
| NORMAL | Kein aktiver ESTOP |
| ACTIVE | ESTOP ausgelöst, Ausführung gestoppt |
| LATCHED | ESTOP bleibt aktiv bis manueller Quittierung |
| TEST | ESTOP-Testmodus ohne echte physische Auslösung |

<!-- @section id="6" title="Langzeit-Prozessmodell" type="prose" -->
## §6 Langzeit-Prozessmodell

<!-- @section id="6.1" title="Zweck" type="prose" -->
### §6.1 Zweck

Das Langzeit-Prozessmodell dient dazu, geräteautonome Prozesse zu verwalten, die länger dauern als ein einzelner RPC-Aufruf.

Beispiele:
- 72-Stunden-Inkubation
- Lange Temperprozesse
- Lange Materialtests
- Lange Compute-Jobs

<!-- @section id="6.2" title="Trennung von Kommando und Prozess" type="prose" -->
### §6.2 Trennung von Kommando und Prozess

<!-- @ref target="foundation/CONTRACTS.md §3.3" type="contract" -->
<!-- @ref target="foundation/CONTRACTS.md §3.4" type="contract" -->
→ Siehe CONTRACTS §3.3 und §3.4 für die HALCommand- und ProcessCommand-Verträge.

```
timeout_s:                   Kommando-Timeout (RPC-Aufruf, Sekunden)
expected_process_duration_s: Prozess-Dauer (physikalisch, Sekunden bis Tage)
```

Diese sind STRIKT getrennt.
Beispiel: `timeout_s = 60.0`, `expected_process_duration_s = 259200.0` (72h)

<!-- @section id="6.3" title="Prozess-Modi" type="prose" -->
### §6.3 Prozess-Modi

<!-- @table schema="process_modes" -->
| Modus | Bedeutung |
|-------|-----------|
| START | Prozess starten |
| MONITOR | Prozess überwachen |
| RESUME | Prozess fortsetzen |
| HOLD | Prozess anhalten |
| ABORT | Prozess abbrechen |
| RELEASE_STAGE | Nächste Stufe freigeben |

<!-- @section id="6.4" title="Prozess-Zustandsmaschine" type="state-machine" machine="process_state" -->
### §6.4 Prozess-Zustandsmaschine

<!-- @ref target="foundation/CONTRACTS.md §7.3" type="contract" -->
→ Siehe CONTRACTS §7.3 für die vollständige Zustandsmaschine.

<!-- @table schema="state_machine_states" machine="process_state" -->
| Zustand | Bedeutung |
|---------|-----------|
| PENDING | Prozess wartet |
| RUNNING | Prozess läuft |
| PAUSED | Prozess pausiert |
| SAFE_HOLD | Prozess sicher angehalten |
| WAITING_FOR_RELEASE | Wartet auf manuelle Freigabe |
| COMPLETED | Erfolgreich abgeschlossen |
| ABORTED | Abgebrochen |
| FAULT | Fehler |
| UNKNOWN | Zustand unklar (nach Crash) |

<!-- @section id="6.5" title="Lease-Expiry-Policy" type="prose" -->
### §6.5 Lease-Expiry-Policy

<!-- @table schema="lease_expiry_policies" -->
| Policy | Bedeutung |
|--------|-----------|
| SAFE_HOLD | Prozess sicher anhalten, aber nicht zerstören |
| ABORT_TO_SAFE_STATE | Prozess in sicheren Zustand abbrechen |
| CONTINUE_PASSIVE_SAFE | Prozess passiv weiterlaufen lassen (z.B. Inkubator hält Temperatur) |
| REQUIRES_RECONCILE | Zustand muss geklärt werden |

<!-- @section id="6.6" title="Stage-Release-Policy" type="prose" -->
### §6.6 Stage-Release-Policy

Für mehrstufige Prozesse mit sicherheitskritischen Stufen:

<!-- @ref target="foundation/CONTRACTS.md §4.5" type="contract" -->
→ Siehe CONTRACTS §4.5 für den StageReleasePolicy-Vertrag.

Beispiel:
```yaml
stages:
  - stage_id: incubation_72h
    release_required: false
    auto_start_allowed: true
  - stage_id: uv_exposure
    release_required: true
    release_authority: SAFETY_PROCESS_OR_HUMAN
    auto_start_allowed: false
```

<!-- @section id="6.7" title="Resume-Token" type="prose" -->
### §6.7 Resume-Token

Für idempotentes Fortsetzen nach Restart:

Regeln:
- `resume_token` wird bei jedem Zustandswechsel aktualisiert
- `resume_token` ist erforderlich für `RESUME`
- Wenn `resume_token` ungültig ist: `RECOVERY_UNSAFE`

<!-- @section id="7" title="Compute-Ressourcenmodell" type="prose" -->
## §7 Compute-Ressourcenmodell

<!-- @section id="7.1" title="Zweck" type="prose" -->
### §7.1 Zweck

Das Compute-Ressourcenmodell unterscheidet Labor-Aktuatorik von Compute-Ressourcen.

<!-- @section id="7.2" title="Resource-Class" type="prose" -->
### §7.2 Resource-Class

<!-- @table schema="resource_classes" -->
| Klasse | Bedeutung |
|--------|-----------|
| LAB_ACTUATOR | Physischer Laboraktuator (Roboterarm, Pipettierroboter, Inkubator) |
| COMPUTE_NODE | Compute-Ressource (GPU-Cluster, CPU-Node) |
| SIMULATION_ENVIRONMENT | Simulationsumgebung |
| SANDBOX_ENVIRONMENT | Sandbox-Umgebung |
| HYBRID_SLOT | Kombination aus Labor und Compute |

<!-- @ref target="foundation/CONTRACTS.md §3.2" type="contract" -->
→ Siehe CONTRACTS §3.2 für den SlotDescriptor-Vertrag.

<!-- @section id="7.3" title="Compute-spezifische Fehlercodes" type="prose" -->
### §7.3 Compute-spezifische Fehlercodes

<!-- @table schema="error_codes" category="compute" -->
| Fehler | Bedeutung | Fehlerklasse |
|--------|-----------|-------------|
| COMPUTE_OOM | Host-RAM-OOM | OPERATIONAL |
| CUDA_OOM | GPU-Speicher-OOM | OPERATIONAL |
| GPU_LOST | GPU nicht erreichbar | OPERATIONAL |
| SCHEDULER_REJECTED | Scheduler hat Job abgelehnt | OPERATIONAL |
| NODE_UNAVAILABLE | Node nicht erreichbar | OPERATIONAL |
| CONTAINER_OOM_KILLED | Container wurde wegen OOM getötet | OPERATIONAL |
| CONTAINER_CRASHED | Container ist abgestürzt | OPERATIONAL |

<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08 für die Operational/Scientific-Trennung.

Ausnahme: Wenn ein Compute-Fehler tatsächlich eine physische Gefahr verursacht (z.B. Brand oder Kühlungsausfall), dann ist es nicht der CUDA-Fehler selbst, sondern ein physischer Sensor, der `SAFETY` auslöst.

<!-- @section id="7.4" title="Compute-spezifische Slot-Felder" type="prose" -->
### §7.4 Compute-spezifische Slot-Felder

<!-- @ref target="foundation/CONTRACTS.md §3.2" type="contract" -->
→ Siehe CONTRACTS §3.2 für die vollständigen SlotDescriptor-Felder.

```
accelerator_type: Optional[str]
accelerator_count: int
accelerator_memory_gb: Optional[float]
supported_runtimes: list[str]
```

<!-- @section id="8" title="Parameter-Schema-Registry" type="prose" -->
## §8 Parameter-Schema-Registry

<!-- @section id="8.1" title="Zweck" type="prose" -->
### §8.1 Zweck

Die Parameter-Schema-Registry dient dazu, komplexe Geräteprofile sicher zu validieren.

<!-- @section id="8.2" title="Felder" type="prose" -->
### §8.2 Felder

<!-- @ref target="foundation/CONTRACTS.md §3.3" type="contract" -->
<!-- @ref target="foundation/CONTRACTS.md §3.4" type="contract" -->
→ Siehe CONTRACTS §3.3 und §3.4 für die HALCommand- und ProcessCommand-Verträge.

<!-- @table schema="parameter_schema_fields" -->
| Feld | Bedeutung |
|------|-----------|
| parameter_schema_ref | Referenz auf das Schema der Parameter |
| parameter_schema_version | Version des Schemas |
| parameter_checksum | Prüfsumme der Parameter |
| payload_artifact_ref | Referenz auf ein externes Artifact |

<!-- @section id="8.3" title="Regeln" type="prose" -->
### §8.3 Regeln

<!-- @table schema="parameter_schema_rules" -->
| Regel | Bedeutung |
|-------|-----------|
| Wenn eine Capability komplexe Profile erwartet, muss `parameter_schema_ref` gesetzt sein. | Schema-Pflicht |
| Wenn `parameter_schema_ref` gesetzt ist, muss `parameter_checksum` gesetzt sein. | Checksum-Pflicht |
| Wenn Schema unbekannt oder Checksumme falsch: `PARAMETER_INVALID`. | Fail-Closed |
| HAL interpretiert die Parameter nicht wissenschaftlich. | Keine wissenschaftliche Interpretation (→ CHARTER §SR-08) |
| HAL prüft nur formal: Schema bekannt, Version erlaubt, Checksumme korrekt, Größe erlaubt. | Formale Prüfung |

<!-- @section id="8.4" title="Fehlercodes" type="prose" -->
### §8.4 Fehlercodes

<!-- @table schema="error_codes" category="parameter_schema" -->
| Fehler | Bedeutung | Fehlerklasse |
|--------|-----------|-------------|
| PARAMETER_SCHEMA_UNKNOWN | Schema ist unbekannt | OPERATIONAL |
| PARAMETER_CHECKSUM_MISMATCH | Checksumme stimmt nicht | OPERATIONAL |
| PARAMETER_INVALID | Parameter ist ungültig | OPERATIONAL |

<!-- @section id="9" title="HAL-Schnittstellen" type="prose" -->
## §9 HAL-Schnittstellen

<!-- @ref target="foundation/CONTRACTS.md §3.12" type="contract" -->
→ Siehe CONTRACTS §3.12 für die vollständige HAL-Interface-Definition.

Die folgenden 16 Funktionen sind verbindlich:

<!-- @table schema="hal_interface_functions" -->
| # | Funktion | Zweck |
|---|----------|-------|
| 1 | get_environment_manifest() | Umgebungsinformationen abrufen |
| 2 | get_slot_state(slot_id) | Slot-Zustand abrufen |
| 3 | get_zone_state(zone_id) | Zonen-Zustand abrufen |
| 4 | execute_command(command) | Kommando ausführen |
| 5 | start_process(process_command) | Langzeit-Prozess starten |
| 6 | monitor_process(process_id) | Prozess überwachen |
| 7 | hold_process(process_id) | Prozess anhalten |
| 8 | resume_process(process_id, resume_token) | Prozess fortsetzen |
| 9 | abort_process(process_id) | Prozess abbrechen |
| 10 | release_stage(process_id, stage_id, release_authority) | Stufe freigeben |
| 11 | report_estop(reason, trigger_source) | ESTOP melden |
| 12 | report_hardware_interlock(interlock_event) | Hardware-Interlock melden |
| 13 | get_estop_state() | ESTOP-Zustand abrufen |
| 14 | reconcile_slot_state(slot_id) | Slot-Zustand nach Crash klären |
| 15 | reconcile_process_state(process_id) | Prozess-Zustand nach Crash klären |
| 16 | get_command_status(command_id) | Kommando-Status abrufen |

<!-- @section id="10" title="Fehlermodell und Fehlerbehandlung" type="prose" -->
## §10 Fehlermodell und Fehlerbehandlung

<!-- @section id="10.1" title="Fehlerklassen" type="prose" -->
### §10.1 Fehlerklassen

<!-- @ref target="foundation/CONTRACTS.md §9.1" type="contract" -->
→ Siehe CONTRACTS §9.1 für die vollständige Fehlerklassen-Definition.
<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08 für die Operational/Scientific-Trennung.

<!-- @table schema="error_classes" -->
| Klasse | Bedeutung | Wissenschaftliches Signal? |
|--------|-----------|---------------------------|
| OPERATIONAL | Prozessfehler, Crash, Timeout, Lease-Problem | Nein |
| SAFETY | Sicherheitsverletzung, ESTOP | Ja, mit Sicherheitsprüfung |

HAL darf keine wissenschaftliche Fehlerklasse verwenden.

<!-- @section id="10.2" title="Operationale Fehler (HAL)" type="prose" -->
### §10.2 Operationale Fehler (HAL)

<!-- @ref target="foundation/CONTRACTS.md §9.2" type="contract" -->
→ Siehe CONTRACTS §9.2 für die vollständige Liste der operationalen Fehler.

```
LEASE_INVALID, LEASE_EXPIRED, LEASE_REVOKED, LEASE_SLOT_MISMATCH,
LEASE_VALIDATION_UNSAFE, SLOT_BUSY, SLOT_UNAVAILABLE,
ZONE_LOCK_UNAVAILABLE, ZONE_LOCK_TIMEOUT, ZONE_LOCK_DENIED,
ZONE_LOCK_EXPIRED, COMMAND_TIMEOUT, PROCESS_TIMEOUT,
DEVICE_UNAVAILABLE, OOM, COMPUTE_OOM, CUDA_OOM, GPU_LOST,
SCHEDULER_REJECTED, NODE_UNAVAILABLE, CONTAINER_OOM_KILLED,
CONTAINER_CRASHED, HAL_INTERNAL_ERROR, DUPLICATE_COMMAND_BLOCKED,
DUPLICATE_PROCESS_BLOCKED, COMMAND_INVALID, PROCESS_INVALID,
PARAMETER_INVALID, PARAMETER_SCHEMA_UNKNOWN, PARAMETER_CHECKSUM_MISMATCH,
TIMEOUT_EXCEEDS_LIMIT, PROCESS_DURATION_EXCEEDS_LIMIT,
PHYSICAL_EXECUTION_FORBIDDEN, COMPUTE_EXECUTION_FORBIDDEN,
RECOVERY_UNSAFE, RESUME_TOKEN_INVALID, STAGE_RELEASE_DENIED
```

Alle diese Fehler sind `OPERATIONAL`.

<!-- @section id="10.3" title="Sicherheitsfehler (HAL)" type="prose" -->
### §10.3 Sicherheitsfehler (HAL)

<!-- @ref target="foundation/CONTRACTS.md §9.3" type="contract" -->
→ Siehe CONTRACTS §9.3 für die vollständige Liste der Sicherheitsfehler.

```
ESTOP_RECEIVED, HARDWARE_INTERLOCK_TRIGGERED,
EXTERNAL_SAFETY_CHAIN_TRIGGERED, SAFETY_LIMIT_VIOLATION,
UNSAFE_SLOT_STATE, UNSAFE_ZONE_STATE,
PHYSICAL_INTERLOCK_TRIGGERED, SAFETY_RESET_REQUIRED
```

Alle diese Fehler sind `SAFETY`.

<!-- @section id="10.4" title="HAL-Fehlerregeln" type="prose" -->
### §10.4 HAL-Fehlerregeln

<!-- @table schema="hal_error_rules" -->
| Regel | Bedeutung | CHARTER-Referenz |
|-------|-----------|-----------------|
| HAL behandelt CUDA_OOM als OPERATIONAL, nicht als SAFETY | Compute-Fehler sind operational | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| HAL behandelt LEASE_DENIED als OPERATIONAL, nicht als ESTOP | Ressourcenkonflikte sind operational | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->CHARTER §SR-09 |
| HAL behandelt Hardware-Interlock als SAFETY | Hardware-Interlocks sind sicherheitsrelevant | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->CHARTER §SR-09 |
| HAL behandelt Software-ESTOP als SAFETY | ESTOP ist sicherheitsrelevant | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->CHARTER §SR-09 |
| HAL meldet keine wissenschaftlichen Fehlerklassen | Keine wissenschaftliche Interpretation | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |

<!-- @section id="11" title="Timeout-Semantik" type="prose" -->
## §11 Timeout-Semantik

<!-- @section id="11.1" title="Kommando-Timeout" type="prose" -->
### §11.1 Kommando-Timeout

Jedes Kommando hat `timeout_s` (→ CONTRACTS §3.3).

Regeln:
- `timeout_s` muss positiv sein
- `timeout_s` darf `max_command_timeout_s` aus dem Manifest nicht überschreiten
- Wenn `timeout_s` fehlt oder ungültig ist: `COMMAND_INVALID`
- Wenn `timeout_s` zu groß ist: `TIMEOUT_EXCEEDS_LIMIT`

<!-- @section id="11.2" title="Prozess-Dauer" type="prose" -->
### §11.2 Prozess-Dauer

Jeder Prozess hat `expected_process_duration_s` (→ CONTRACTS §3.4).

Regeln:
- `expected_process_duration_s` muss positiv sein
- `expected_process_duration_s` darf `max_process_duration_s` aus dem SlotDescriptor nicht überschreiten
- Wenn `expected_process_duration_s` zu groß ist: `PROCESS_DURATION_EXCEEDS_LIMIT`

<!-- @section id="11.3" title="Timeout bei Kommandos" type="prose" -->
### §11.3 Timeout bei Kommandos

Bei Timeout:
- Kommando wird als `TIMEOUT` gemeldet
- Wenn der Slot physisch ist und der Zustand unklar bleibt:
  - Slot auf `ERROR`
  - `reconcile_slot_state` erforderlich
  - Kein blinder Retry
- Fehlerklasse: `OPERATIONAL`

<!-- @section id="11.4" title="Timeout bei Prozessen" type="prose" -->
### §11.4 Timeout bei Prozessen

Bei Prozess-Timeout:
- Prozess wird als `FAULT` gemeldet
- `on_lease_expiry_policy` wird angewendet
  - Wenn `SAFE_HOLD`: Prozess wird sicher angehalten
  - Wenn `ABORT_TO_SAFE_STATE`: Prozess wird in sicheren Zustand abgebrochen
  - Wenn `CONTINUE_PASSIVE_SAFE`: Prozess läuft passiv weiter
  - Wenn `REQUIRES_RECONCILE`: Zustand muss geklärt werden
- Fehlerklasse: `OPERATIONAL`

<!-- @section id="12" title="Crash-Recovery und Reconciliation" type="prose" -->
## §12 Crash-Recovery und Reconciliation

<!-- @section id="12.1" title="Grundsätze" type="prose" -->
### §12.1 Grundsätze

Nach einem Crash gilt:
- Kein automatischer Neustart von Kommandos
- Kein automatischer Neustart von Prozessen
- Kein blinder Retry
- Keine automatische Slot-Freigabe bei unklarem Zustand
- Keine automatische Zonen-Freigabe bei unklarem Zustand

<!-- @ref target="CHARTER §SR-10" type="security-rule" -->
→ Siehe CHARTER §SR-10 für die Fail-Closed-Regel.

<!-- @section id="12.2" title="Recovery-Schritte" type="dataflow" dataflow="crash_recovery" -->
### §12.2 Recovery-Schritte

<!-- @dataflow id="crash_recovery" trigger="CRASH_DETECTED" source_role="hal_interface" target_role="questor" -->
1. `get_estop_state()` prüfen
2. `get_slot_state()` prüfen
3. `get_zone_state()` prüfen
4. `get_command_status()` prüfen, falls vorhanden
5. `reconcile_slot_state()` aufrufen
6. `reconcile_process_state()` aufrufen, falls Prozess aktiv war

<!-- @section id="12.3" title="Recovery-Entscheidung" type="prose" -->
### §12.3 Recovery-Entscheidung

<!-- @table schema="recovery_decisions" -->
| Zustand | Aktion |
|---------|--------|
| Zustand eindeutig | Slot kann kontrolliert freigegeben oder weitergenutzt werden. Prozess kann kontrolliert fortgesetzt oder abgebrochen werden. |
| Zustand unklar | Slot auf `ERROR`. Prozess auf `UNKNOWN`. Ergebnis: `RECOVERY_UNSAFE`. |

Regel: HAL darf Recovery nicht als wissenschaftliche Entscheidung behandeln (→ CHARTER §SR-08).

<!-- @section id="13" title="Idempotenz" type="prose" -->
## §13 Idempotenz

<!-- @section id="13.1" title="Grundsatz" type="prose" -->
### §13.1 Grundsatz

HAL muss Kommandos und Prozesse idempotent behandeln.

<!-- @ref target="foundation/CONTRACTS.md §8.2" type="contract" -->
→ Siehe CONTRACTS §8.2 für die HAL-Idempotenz-Regeln.

<!-- @section id="13.2" title="Idempotenz-Schlüssel" type="prose" -->
### §13.2 Idempotenz-Schlüssel

```
hal_idempotency_key        = command_id:lease_ref:slot_id
hal_process_idempotency_key = process_id:lease_ref:slot_id
```

<!-- @section id="13.3" title="Regeln" type="prose" -->
### §13.3 Regeln

<!-- @table schema="idempotency_rules" -->
| Regel | Bedeutung |
|-------|-----------|
| Ein bereits ausgeführtes Kommando darf nicht erneut ausgeführt werden. | Keine doppelte Ausführung |
| Ein bereits gestarteter Prozess darf nicht erneut gestartet werden. | Keine doppelte Ausführung |
| Ein blockiertes Duplikat darf keine Seiteneffekte erzeugen. | Keine doppelten Seiteneffekte |
| Ein Duplikat wird als `DUPLICATE_BLOCKED` gemeldet. | Status-Meldung |
| Idempotenz ist besonders wichtig nach Crash, Timeout oder Recovery. | Crash-Sicherheit |

<!-- @section id="14" title="Logging und Audit" type="prose" -->
## §14 Logging und Audit

<!-- @section id="14.1" title="Erlaubte Event-Typen" type="prose" -->
### §14.1 Erlaubte Event-Typen

<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08 für die Operational/Scientific-Trennung.

```
command_received
command_accepted
command_denied
command_started
command_finished
command_timeout
command_duplicate_blocked
process_started
process_state_changed
process_safe_hold
process_waiting_for_release
process_completed
process_aborted
process_fault
process_unknown
lease_validation_failed
slot_state_changed
zone_state_changed
zone_lock_requested
zone_lock_granted
zone_lock_denied
zone_lock_expired
estop_triggered
estop_acknowledged
estop_reset_requested
estop_reset_confirmed
hardware_interlock_triggered
reconciliation_started
reconciliation_finished
```

<!-- @section id="14.2" title="Zielverzeichnis" type="prose" -->
### §14.2 Zielverzeichnis

```
data/operational_logs/
```

<!-- @section id="14.3" title="Verbotene Ziele" type="prose" -->
### §14.3 Verbotene Ziele

<!-- @table schema="forbidden_log_targets" -->
| Verboten | CHARTER-Referenz |
|----------|-----------------|
| Schreiben nach `data/archiv/` | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Schreiben nach `data/atlas/` | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Schreiben nach `data/questor_blackbox/` | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |
| Speichern wissenschaftlicher Hypothesen | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| Speichern von Questor-internen Trails | <!-- @ref target="CHARTER §SR-50" type="security-rule" -->CHARTER §SR-50 |
| Speichern von Blackbox-Inhalten | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |

<!-- @section id="15" title="HAL und Questor" type="prose" -->
## §15 HAL und Questor

<!-- @section id="15.1" title="Kommunikation" type="prose" -->
### §15.1 Kommunikation

Questor kommuniziert mit HAL über eine HAL-Bridge (→ specs/QUESTOR.md §8).
Questor darf nicht direkt auf Hardware zugreifen (→ CHARTER §SR-12).
Die HAL-Bridge übersetzt Questor-Intentionen in `HALCommand`- oder `ProcessCommand`-Objekte.

<!-- @section id="15.2" title="Regeln" type="prose" -->
### §15.2 Regeln

<!-- @table schema="hal_questor_rules" -->
| Regel | CHARTER-Referenz |
|-------|-----------------|
| Keine wissenschaftlichen Ziele in `HALCommand.parameters` | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| Keine Atlas-Signale in `HALCommand.parameters` | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| Keine Gate-Logik in HAL | — |
| Keine Lease-Vergabe in Questor oder HAL | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| Keine Atlas-Hybrid-Felder in HALCommand.parameters | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04, §SR-08 |
| Keine Atlas-Hybrid-Felder in ProcessCommand.parameters | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04, §SR-08 |
| HAL-Bridge übersetzt keine expectation_ref, frontier_candidate_ref oder evidence_kind | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |

<!-- @section id="15.3" title="Questor erhält von HAL" type="prose" -->
### §15.3 Questor erhält von HAL

- `HALCommandResult` (→ CONTRACTS §3.5)
- `ProcessResult` (→ CONTRACTS §3.6)
- Slot-Zustände (→ CONTRACTS §3.7)
- Zonen-Zustände (→ CONTRACTS §3.8)
- ESTOP-Zustände (→ CONTRACTS §3.10)

<!-- @section id="15.4" title="Questor meldet daraus resultierende Ergebnisse" type="prose" -->
### §15.4 Questor meldet daraus resultierende Ergebnisse

Questor meldet die Ergebnisse im `questor_ergebnis_paket` (→ CONTRACTS §2.1).

<!-- @section id="16" title="HAL und Resource Governor" type="prose" -->
## §16 HAL und Resource Governor

<!-- @section id="16.1" title="Zuständigkeiten" type="prose" -->
### §16.1 Zuständigkeiten

Resource Governor ist für Leases zuständig.

HAL darf:
- Lease-Referenzen prüfen
- Lease-Status anfragen
- ESTOP-bedingte Lease-Suspendierung melden
- Zonen-Locks anfragen
- Zonen-Lock-Status anfragen

HAL darf nicht:
- Leases erzeugen (→ CHARTER §SR-06)
- Leases verlängern (→ CHARTER §SR-06)
- Leases widerrufen (→ CHARTER §SR-06)
- Lease-Kontingente verwalten
- Pfad-Leases eigenmächtig koordinieren
- Zonen-Locks eigenmächtig vergeben (→ CHARTER §SR-06)

<!-- @section id="16.2" title="Pfad-Leases" type="prose" -->
### §16.2 Pfad-Leases

Pfad-Leases bleiben Aufgabe des Resource Governors.

<!-- @ref target="foundation/CONTRACTS.md §4.3" type="contract" -->
→ Siehe CONTRACTS §4.3 für den PathLease-Vertrag.

<!-- @section id="16.3" title="Zonen-Locks" type="prose" -->
### §16.3 Zonen-Locks

Zonen-Locks werden vom Resource Governor verwaltet.
HAL sieht normalerweise nur slotbezogene Lease-Referenzen.

<!-- @section id="17" title="HAL und Sicherheitsmodus" type="prose" -->
## §17 HAL und Sicherheitsmodus

<!-- @section id="17.1" title="Sicherheitsmodi" type="prose" -->
### §17.1 Sicherheitsmodi

<!-- @ref target="foundation/CONTRACTS.md §1.3" type="contract" -->
→ Siehe CONTRACTS §1.3 für die SecurityMode-Definition.

<!-- @table schema="security_modes" -->
| Modus | Bedeutung |
|-------|-----------|
| NORMAL | Produktivbetrieb. Physische Ausführung erlaubt. |
| SANDBOX | Simulationsbetrieb. Keine physische Wirkung auf echte Proben. |
| DEV_SANDBOX_ONLY | Reine Test/Dev-Umgebung. Keine Produktivdaten, keine echten Proben. |
| RECOVERY | Ausnahmezustand. Nur Zustandsklärung und Aufräumarbeiten. |

<!-- @section id="17.2" title="HAL-Reaktion auf Sicherheitsmodi" type="prose" -->
### §17.2 HAL-Reaktion auf Sicherheitsmodi

<!-- @table schema="hal_security_mode_reaction" -->
| Modus | Physisch | Compute | Sandbox |
|-------|----------|---------|---------|
| NORMAL | ✅ wenn `physical_actuation = true` und Lease `physical_execution_allowed = true` | ✅ wenn `compute_capable = true` und Lease `compute_execution_allowed = true` | ✅ |
| SANDBOX | ❌ | Nur Sandbox-Compute | ✅ wenn `sandbox_capable = true` |
| DEV_SANDBOX_ONLY | ❌ | Nur Dev-Compute | Nur Dev-Sandbox |
| RECOVERY | ❌ (außer `reconcile_*`) | ❌ (außer `reconcile_*`) | ❌ |

<!-- @ref target="CHARTER §SR-35" type="security-rule" -->
<!-- @ref target="CHARTER §SR-39" type="security-rule" -->
→ Siehe CHARTER §SR-35 bis §SR-39 für die Security-Mode-Regeln.

<!-- @section id="17.3" title="Fehler bei Modus-Mismatch" type="prose" -->
### §17.3 Fehler bei Modus-Mismatch

Wenn der Modus nicht zum Slot passt:

<!-- @table schema="security_mode_mismatch_errors" -->
| Fehler | Fehlerklasse |
|--------|-------------|
| PHYSICAL_EXECUTION_FORBIDDEN | OPERATIONAL |
| COMPUTE_EXECUTION_FORBIDDEN | OPERATIONAL |

<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08 für die Operational/Scientific-Trennung.

<!-- @section id="18" title="Dummy-HAL" type="prose" -->
## §18 Dummy-HAL

<!-- @section id="18.1" title="Zweck" type="prose" -->
### §18.1 Zweck

<!-- @role id="dummy_hal" layer="1" llm="false" writes_to="dummy_results" reads_from="dummy_commands" -->
Für Trockenlauf, Integrationstests und Implementierung ohne echte Hardware ist ein Dummy-HAL erforderlich.

<!-- @section id="18.2" title="Simulierbare Fehlermodi" type="prose" -->
### §18.2 Simulierbare Fehlermodi

Der Dummy-HAL muss folgende Modi simulieren können:

```
SUCCESS
LEASE_DENIED
LEASE_EXPIRED
LEASE_REVOKED
SLOT_BUSY
SLOT_UNAVAILABLE
ZONE_LOCK_UNAVAILABLE
ZONE_LOCK_DENIED
COMMAND_TIMEOUT
PROCESS_TIMEOUT
ESTOP
HARDWARE_INTERLOCK
OOM
COMPUTE_OOM
CUDA_OOM
GPU_LOST
SCHEDULER_REJECTED
NODE_UNAVAILABLE
CONTAINER_OOM_KILLED
CONTAINER_CRASHED
DEVICE_UNAVAILABLE
DUPLICATE_BLOCKED
DUPLICATE_PROCESS_BLOCKED
RECOVERY_UNSAFE
RESUME_TOKEN_INVALID
STAGE_RELEASE_DENIED
```

<!-- @section id="18.3" title="Zusätzliche Anforderungen" type="prose" -->
### §18.3 Zusätzliche Anforderungen

Der Dummy-HAL muss zusätzlich können:
- Slot-Zustände deterministisch zurückgeben
- Zonen-Zustände deterministisch zurückgeben
- ESTOP auslösen und zurücksetzen, aber nur über autorisierte Dummy-Funktionen
- Hardware-Interlock auslösen und zurücksetzen, aber nur über autorisierte Dummy-Funktionen
- Manifest bereitstellen
- Kommandos idempotent behandeln
- Prozesse idempotent behandeln
- Timeout simulieren
- Prozess-Timeout simulieren
- Unklaren Crash-Zustand simulieren
- Langzeit-Prozess mit SAFE_HOLD simulieren
- Langzeit-Prozess mit RESUME simulieren
- Langzeit-Prozess mit WAITING_FOR_RELEASE simulieren
- Operational-Audit-Ereignisse schreiben

<!-- @section id="18.4" title="Regel" type="prose" -->
### §18.4 Regel

Der Dummy-HAL darf keine echte Hardware ansprechen.

<!-- @section id="19" title="Implementierungsphasen" type="implementation-phase" -->
## §19 Implementierungsphasen

<!-- @section id="19.1" title="Übersicht" type="prose" -->
### §19.1 Übersicht

<!-- @table schema="phase_tasks" phase="hal" -->
| Phase | Name | Dauer (Schätzung) |
|-------|------|-------------------|
| HAL-H0 | HAL-Vertrag in Hauptstruktur bestätigen | 1 Tag |
| HAL-H1 | Interface und Datenmodelle | 3–5 Tage |
| HAL-H2 | Slot- und Lease-Logik | 2–3 Tage |
| HAL-H3 | Zonen-Mutex und Prozess-Logik | 3–4 Tage |
| HAL-H4 | ESTOP und Hardware-Interlocks | 2–3 Tage |
| HAL-H5 | Compute-Modell und Parameter-Schema | 2–3 Tage |
| HAL-H6 | Dummy-HAL und Integration | 3–4 Tage |

<!-- @section id="19.2" title="Phase HAL-H0: HAL-Vertrag bestätigen" type="prose" -->
### §19.2 Phase HAL-H0: HAL-Vertrag bestätigen

Aufgaben:
- HAL-Minimalvertrag mit dieser Datei abgleichen
- Dokumentenhierarchie bestätigen
- Keine sicherheitswidrigen Abweichungen zulassen

Akzeptanz:
- [ ] Strukturversion 1.1.1 bleibt maßgeblich
- [ ] HAL v0.2.0 ist als präzisierte Spezifikation akzeptiert

<!-- @section id="19.3" title="Phase HAL-H1: Interface und Datenmodelle" type="prose" -->
### §19.3 Phase HAL-H1: Interface und Datenmodelle

Aufgaben:
- `hal_interface.py`
- `dummy_hal.py`
- Pydantic-Modelle für alle HAL-Verträge (→ CONTRACTS §3)

Akzeptanz:
- [ ] Alle Modelle sind validierbar
- [ ] Keine wissenschaftlichen Felder
- [ ] Fehlerklassen sind korrekt getrennt
- [ ] Mindestens 40 Unit-Tests

<!-- @section id="19.4" title="Phase HAL-H2: Slot- und Lease-Logik" type="prose" -->
### §19.4 Phase HAL-H2: Slot- und Lease-Logik

Aufgaben:
- Slot-State-Handling
- Lease-Validierung
- Slot-Mutex
- Timeout-Prüfung
- Idempotenzprüfung

Akzeptanz:
- [ ] Kein Slot wird doppelt belegt
- [ ] Ungültige Leases werden abgelehnt
- [ ] Timeouts werden korrekt gemeldet
- [ ] Duplikate werden blockiert
- [ ] Mindestens 25 Unit-Tests

<!-- @section id="19.5" title="Phase HAL-H3: Zonen-Mutex und Prozess-Logik" type="prose" -->
### §19.5 Phase HAL-H3: Zonen-Mutex und Prozess-Logik

Aufgaben:
- Zone-State-Handling
- Zonen-Lock-Anfrage und -Antwort
- Prozess-State-Handling
- Langzeit-Prozess-Modell
- SAFE_HOLD und RESUME
- Stage-Release-Policy

Akzeptanz:
- [ ] Keine Zone wird doppelt belegt
- [ ] Zonen-Locks werden korrekt angefragt und freigegeben
- [ ] Langzeit-Prozesse können gestartet, angehalten und fortgesetzt werden
- [ ] Stage-Release funktioniert
- [ ] Mindestens 30 Unit-Tests

<!-- @section id="19.6" title="Phase HAL-H4: ESTOP und Hardware-Interlocks" type="prose" -->
### §19.6 Phase HAL-H4: ESTOP und Hardware-Interlocks

Aufgaben:
- ESTOP-Zustandsmaschine
- Hardware-Interlock-Zustandsmaschine
- `report_estop`
- `report_hardware_interlock`
- `get_estop_state`
- `reconcile_slot_state`
- `reconcile_process_state`
- Audit-Events für ESTOP und Interlocks

Akzeptanz:
- [ ] ESTOP stoppt Kommandos
- [ ] ESTOP suspendiert Leases
- [ ] Hardware-Interlock stoppt Kommandos
- [ ] Hardware-Interlock suspendiert Leases und Zonen
- [ ] Kein ESTOP bei Ressourcenkonflikt (→ CHARTER §SR-09)
- [ ] Kein blinder Retry nach Crash
- [ ] Mindestens 25 Unit-Tests

<!-- @section id="19.7" title="Phase HAL-H5: Compute-Modell und Parameter-Schema" type="prose" -->
### §19.7 Phase HAL-H5: Compute-Modell und Parameter-Schema

Aufgaben:
- Compute-Ressourcenmodell
- Compute-spezifische Fehlercodes
- Parameter-Schema-Registry
- Parameter-Schema-Validierung

Akzeptanz:
- [ ] Compute-Ressourcen werden korrekt angefragt
- [ ] Compute-Fehler sind operational (→ CHARTER §SR-08)
- [ ] Parameter-Schemas werden korrekt validiert
- [ ] Mindestens 20 Unit-Tests

<!-- @section id="19.8" title="Phase HAL-H6: Dummy-HAL und Integration" type="prose" -->
### §19.8 Phase HAL-H6: Dummy-HAL und Integration

Aufgaben:
- Vollständiger Dummy-HAL
- Alle Fehlermodi
- Integration mit Questor-HAL-Bridge
- Integration mit Resource Governor
- Operational-Audit

Akzeptanz:
- [ ] Dummy kann alle relevanten Szenarien simulieren
- [ ] Keine echte Hardware nötig
- [ ] Suite H kann vorbereitet werden
- [ ] Mindestens 25 Integrationstests

<!-- @section id="20" title="Zusammenfassung der Architektur-Entscheidungen" type="prose" -->
## §20 Zusammenfassung der Architektur-Entscheidungen

<!-- @table schema="architecture_decisions" -->
| Thema | Entscheidung | Quelle |
|-------|-------------|--------|
| HAL ist dünne Schicht | Ja | §1.2 |
| HAL ist deterministisch | Ja, keine LLM-Logik | §1.2 |
| HAL ist fail-closed | Ja | §1.2 |
| HAL interpretiert keine wissenschaftlichen Ziele | Ja | §1.2 |
| HAL vergibt keine Leases | Ja | §1.4 |
| HAL gibt keine Blackbox weiter | Ja | §1.4 |
| Slot-Zustandsmaschine | 8 Zustände | §3.1 |
| INTERLOCKED ist härter als ESTOP_SUSPENDED | Ja | §3.3 |
| Zonen-Mutex | 4 Lock-Policies | §4 |
| ESTOP vs Hardware-Interlock | Strikt getrennt | §5.2 |
| Langzeit-Prozessmodell | SAFE_HOLD, RESUME, WAITING_FOR_RELEASE | §6 |
| Trennung timeout_s vs expected_process_duration_s | Strikt | §6.2 |
| Compute-Ressourcenmodell | 5 Resource-Classes | §7.2 |
| CUDA_OOM ist OPERATIONAL | Ja | §7.3 |
| Parameter-Schema-Registry | Schema + Checksum | §8 |
| HAL-Schnittstellen | 16 Funktionen | §9 |
| Fehlermodell | OPERATIONAL / SAFETY | §10 |
| Timeout-Semantik | Kommando vs Prozess | §11 |
| Crash-Recovery | Kein blinder Retry | §12 |
| Idempotenz | command_id:lease_ref:slot_id | §13 |
| Logging | Nur operational | §14 |
| Sicherheitsmodus | 4 Modi, HAL prüft | §17 |
| Dummy-HAL | Alle Fehlermodi simulierbar | §18 |
| Implementierungsphasen | HAL-H0 bis HAL-H6 | §19 |
| Atlas-Hybrid-Kompatibilität | HAL erfordert keine Änderungen; Atlas-Hybrid-Felder gehen nicht an HAL | §0.1 |

<!-- @section id="21" title="Dokumentenhierarchie" type="prose" -->
## §21 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `specs/` und referenziert:
- `foundation/CHARTER.md` für Sicherheitsregeln (CHARTER §SR-XX)
- `foundation/CONTRACTS.md` für Datenverträge (CONTRACTS §X.X)
- `specs/QUESTOR.md` für Questor-spezifische Details
- `specs/GREMIUM.md` für Gremium-spezifische Details

Regel: Änderungen an HAL-Modulen in diesem Dokument erfordern eine Versionsänderung und eine Überprüfung der referenzierten Dokumente.

<!-- @section id="21.1" title="Kritische Warnung: Keine Atlas-Hybrid-Felder an HAL" type="prose" -->
### §21.1 Kritische Warnung: Keine Atlas-Hybrid-Felder an HAL

Wenn eine Implementierung erwartet, dass HAL Atlas-Hybrid-Felder wie `atlas_expectation_ref`, `frontier_candidate_ref`, `evidence_kind` oder `evidence_class` empfängt oder verarbeitet, ist die Implementierung falsch.

<!-- @ref target="CHARTER §SR-04" type="security-rule" -->
<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-04 und §SR-08.
<!-- @ref target="specs/QUESTOR.md §8" type="spec" -->
→ Siehe specs/QUESTOR.md §8 (HAL-Bridge-Übersetzungslogik).

<!-- @section id="A" title="Anhang A: Akzeptanzprüfung für ATLAS-HYB-1.0.0" type="acceptance" -->
## Anhang A: Akzeptanzprüfung für ATLAS-HYB-1.0.0

Nach dem Einfügen dieser Änderungen sollte `HAL.md` folgende Kriterien erfüllen:

<!-- @table schema="acceptance_criteria" -->
| # | Kriterium | Status |
|---|-----------|--------|
| 1 | Kopfzeile enthält Version `1.1.0-atlas-hyb.1` | ☐ |
| 2 | §0.1 Änderungsantrag ATLAS-HYB-1.0.0 ist vorhanden | ☐ |
| 3 | §0.1 bestätigt, dass HAL keine funktionalen Änderungen braucht | ☐ |
| 4 | §1.4 enthält neue Verbote für Atlas-Hybrid-Felder | ☐ |
| 5 | §15.2 enthält neue Regeln für Atlas-Hybrid-Felder | ☐ |
| 6 | §20 enthält Atlas-Hybrid-Kompatibilitätszeile | ☐ |
| 7 | Keine neuen HAL-Funktionen wurden definiert | ☐ |
| 8 | Keine neuen Datenverträge wurden definiert | ☐ |
| 9 | Keine neuen Sicherheitsregeln wurden definiert | ☐ |
| 10 | Die 16 HAL-Schnittstellenfunktionen bleiben unverändert | ☐ |
| 11 | Die Fehlerklassentrennung (OPERATIONAL/SAFETY) bleibt unverändert | ☐ |
| 12 | CHARTER-Hierarchie bleibt gewahrt | ☐ |