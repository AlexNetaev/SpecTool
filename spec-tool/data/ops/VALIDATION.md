---
doc_id: ops/VALIDATION.md
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
conflict_rule: [CHARTER, CONTRACTS, SPECS, THIS_DOC]
roles_referenced:
  - test_engineer
  - systems_integration_reviewer
  - dry_run_auditor
last_modified: 2026-08-21
---

<!-- @section id="0" title="Geltung und Änderungsregeln" type="meta" -->
# 🧪 VALIDATION — TESTSTRATEGIE UND AKZEPTANZKRITERIEN

## §0 Geltung und Änderungsregeln

Dieses Dokument definiert die vollständige Teststrategie für das Gesamtsystem.

Regel: Dieses Dokument referenziert Verträge aus `CONTRACTS.md` und Sicherheitsregeln aus `CHARTER.md`.
Es definiert keine neuen Verträge und keine neuen Sicherheitsregeln.

Konfliktregel: Bei Widersprüchen gilt `CHARTER.md` > `CONTRACTS.md` > `specs/*` > dieses Dokument.

<!-- @section id="0.1" title="Änderungsantrag ATLAS-HYB-1.0.0" type="change-request" -->
### §0.1 Änderungsantrag ATLAS-HYB-1.0.0 — Atlas-Hybrid-Test-Suite

Dieser Änderungsantrag fügt die Atlas-Hybrid-Test-Suite in die Teststrategie ein.
Die Atlas-Hybrid-Test-Suite wird als eigene Datei `ops/VALIDATION_ATLAS.md` geführt und in diesem Dokument referenziert.

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge (→ CONTRACTS.md).
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln (→ CHARTER.md).
- Die Atlas-Hybrid-Tests respektieren das Blackboard-Pattern und die Trennung von Operational und Scientific.
- Questor erhält auch in den Tests keine Atlas-Schreibrechte.

<!-- @section id="0.2" title="Änderungsantrag STRAT-1.0.0" type="change-request" -->
### §0.2 Änderungsantrag STRAT-1.0.0 — Strategic-Layer-Test-Suite

Dieser Änderungsantrag fügt die Strategic-Layer-Test-Suite (Suite STRAT) in die Teststrategie ein.

Die Strategic-Layer-Test-Suite testet:
- ControlState-Manager und 4-Achsen-Zustandsmaschine
- Closure-Regeln CT-1..CT-10
- SL-AX-ATOMIC (atomare Achsen-Transitionen)
- Intent-Verfügbarkeit und Blocklists
- Validierungspipeline (10 Stufen)
- DirectiveTranslationTable (DTT)
- Konfliktdetektor und NO_ACTION
- Briefing-Erzeugung und Sanitization
- Constitutional Anchor Protocol
- Symptom-Trigger und Vordenker-Ansteuerung
- SL-SAF-7 (SAFE_MODE-Exit)
- SL-SIG-7a (Overfitting als CONSTRAINT_NEAR_MISS)
- Quarantäne-Diagnostik-Ausnahme

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge (→ CONTRACTS.md §6.11).
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln (→ CHARTER.md).
- Die Strategic-Layer-Tests respektieren das Blackboard-Pattern und die Trennung von Operational und Scientific.
- Questor und HAL erhalten auch in den Tests keine Kenntnis von Strategic-Layer-Verträgen.
- Die Tests referenzieren `specs/GREMIUM_STRATEGY.md` für die Regeldefinitionen.

<!-- @section id="1" title="Validierungs-Übersicht und Grundprinzipien" type="prose" -->
## §1 Validierungs-Übersicht und Grundprinzipien

<!-- @section id="1.1" title="Zweck" type="prose" -->
### §1.1 Zweck

Dieses Dokument definiert:
- Die vollständige Testpyramide für MYRMEX v2.4.0 + Questor v0.2.3 + HAL v0.2.0
- Alle bestehenden Test-Suiten (N, I, S, R, Z, H)
- Alle neuen Questor-spezifischen Test-Suiten (Q-U, Q-C, Q-S, Q-P, Q-T)
- Die Atlas-Hybrid-Test-Suite (ATLAS)
- Die Strategic-Layer-Test-Suite (STRAT)
- Testdaten, Fixtures und Mock-Strategie
- Coverage-Ziele
- Test-Infrastruktur und CI/CD
- Akzeptanzkriterien für das Gesamtsystem

<!-- @section id="1.2" title="Die sechs Test-Grundprinzipien" type="prose" -->
### §1.2 Die sechs Test-Grundprinzipien

<!-- @table schema="test_principles" -->
| # | Prinzip | Bedeutung | CHARTER-Referenz |
|---|---------|-----------|-----------------|
| 1 | Deterministisch vor LLM | Tests sind deterministisch. Keine echten LLM-Aufrufe. | <!-- @ref target="CHARTER §SR-13" type="security-rule" -->CHARTER §SR-13 |
| 2 | Fail-Closed | Tests prüfen Fail-Closed-Verhalten an allen kritischen Punkten. | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->CHARTER §SR-10 |
| 3 | Blackboard-Pattern | Tests prüfen, dass keine direkten Aufrufe zwischen Gremium-Rängen erfolgen. | <!-- @ref target="CHARTER §2" type="security-rule" -->CHARTER §2 |
| 4 | Keine produktiven Altbezeichnungen | Tests prüfen, dass keine alten Swarm-Begriffe in produktiven Quellen vorkommen. | — |
| 5 | Operational ≠ Scientific | Tests prüfen die strikte Trennung von operationalen und wissenschaftlichen Fehlern. | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| 6 | ESTOP ≠ LEASE_DENIED | Tests prüfen die strikte Trennung von ESTOP und LEASE_DENIED. | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->CHARTER §SR-09 |

<!-- @section id="1.3" title="Rolle der Test-KI" type="prose" -->
### §1.3 Rolle der Test-KI

Die Test-KI handelt als:
- Senior Test Engineer
- Systems Integration Reviewer
- Dry-Run Auditor
- Architektur-Reviewer
- HAL-Integration-Reviewer

<!-- @section id="1.4" title="Dry-Run-Modus" type="prose" -->
### §1.4 Dry-Run-Modus

Wenn keine Implementierungsfreigabe gegeben ist:
- kein Code
- keine Dateiänderungen
- keine pytest-Ausführung
- mentale Simulation
- Bewertung mit `BESTANDEN` / `NICHT BESTANDEN`
- Blocker und Nicht-Blocker getrennt melden
- keine stillschweigenden Annahmen bei unklaren Spezifikationslücken

Wenn kein produktives Repository übergeben wurde:
- N-01 kann nur spezifikationsbasiert bewertet werden
- der spätere reale Source-Scan ist als Implementierungsbedingung zu nennen
- das Fehlen eines Repositories ist im Dry-Run eine Modusbedingung, kein Architekturfehler

<!-- @section id="1.5" title="Implementierungsmodus" type="prose" -->
### §1.5 Implementierungsmodus

Wenn eine Phase explizit freigegeben ist:
- nur die freigegebene Phase implementieren
- pytest verwenden
- keine späteren Phasen vorziehen
- nach jeder Phase Status-Report schreiben
- reale Source-Scans für N-01 durchführen, sobald produktive Quellen existieren

<!-- @section id="2" title="Testpyramide" type="prose" -->
## §2 Testpyramide

<!-- @section id="2.1" title="Visuelle Darstellung" type="prose" -->
### §2.1 Visuelle Darstellung

```
                    /\
                     /  \
                    / E2E \          ← Suite S (5 Tests, existiert)
                   /________\
                  /          \
                 / Integration\      ← Suite I (18 Tests, existiert)
                /______________\
               /                \
              /   Komponententests\    ← NEU: ~44 Tests
             /____________________\
            /                      \
           /      Unit-Tests       \  ← NEU: ~252 Tests
          /__________________________\
         /                            \
        /    Atlas-Hybrid-Tests       \  ← NEU: ~120 Tests
       /________________________________\
      /                                  \
     /    Strategic-Layer-Tests          \  ← NEU: ~170 Tests
    /______________________________________\
   /                                        \
  /    Sicherheit / Performance / Stress    \  ← NEU: ~51 Tests
 /____________________________________________\
```

<!-- @section id="2.2" title="Test-Verteilung" type="prose" -->
### §2.2 Test-Verteilung

<!-- @table schema="test_distribution" -->
| Ebene | Anzahl | Anteil | Zweck |
|-------|--------|--------|-------|
| Unit-Tests | ~252 | 35% | Einzelne Funktionen und Klassen |
| Komponententests | ~44 | 6% | Zusammenspiel mehrerer Module |
| Sicherheitstests | ~30 | 4% | Sicherheitskritische Pfade |
| Performance-/Stress-Tests | ~21 | 3% | Last, Latenz, Ressourcen |
| Atlas-Hybrid-Tests | ~120 | 17% | Atlas-Hybrid-System |
| Strategic-Layer-Tests | ~170 | 24% | Strategic Layer (Achsen, Kanzler, Königin) |
| Integrationstests (bestehend) | 18 | 3% | Questor ↔ Gremium (Suite I) |
| Szenario-Tests (bestehend) | 5 | 1% | End-to-End (Suite S) |
| Sonstige bestehende Tests | 51 | 7% | Suite N, R, Z, H |
| **Gesamt** | **~711** | **100%** | |

<!-- @section id="2.3" title="Test-Suiten-Übersicht" type="prose" -->
### §2.3 Test-Suiten-Übersicht

<!-- @table schema="test_suites_overview" -->
| Suite | Tests | Status | Zweck |
|-------|-------|--------|-------|
| Suite N | 7 | Existiert | Naming & Contract Migration |
| Suite I | 18 | Existiert | Integration |
| Suite S | 5 | Existiert | Szenario-Pflichttests |
| Suite R | 12 | Existiert | Regressions-Tests |
| Suite Z | 8 | Existiert | Zielpräzisierung |
| Suite H | 24 | Existiert | HAL v0.2.0 |
| Suite Q-U | ~252 | NEU | Questor Unit-Tests |
| Suite Q-C | ~44 | NEU | Questor Komponententests |
| Suite Q-S | ~30 | NEU | Questor Sicherheits-Tests |
| Suite Q-P | ~10 | NEU | Questor Performance-Tests |
| Suite Q-T | ~11 | NEU | Questor Stress-Tests |
| Suite ATLAS | ~120 | NEU | Atlas-Hybrid-System |
| Suite STRAT | ~170 | NEU | Strategic Layer (Achsen, Kanzler, Königin) |
| **Gesamt** | **~711** | | |

<!-- @section id="3" title="Bestehende Test-Suiten" type="prose" -->
## §3 Bestehende Test-Suiten

<!-- @section id="3.1" title="Suite N — Naming & Contract Migration" type="prose" -->
### §3.1 Suite N — Naming & Contract Migration (7 Tests)

<!-- @table schema="test_suite_N" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| N-01 | Keine produktiven Altbezeichnungen | Keine Treffer in produktiven Quellen. Treffer nur in Migrations-/Archiv-/Testdokumenten oder Allowlists erlaubt. Keine aktive Adapterlogik. |
| N-02 | QuestorErgebnisPaket validiert | Pydantic-Validierung erfolgreich. `questor_instance_id` vorhanden. `sequence_number` vorhanden. `idempotency_key` korrekt kanonisch gebildet. `questor_metadata` optional. Keine freien Zusatzfelder außerhalb von `questor_metadata`. |
| N-03 | Archivar nutzt questor_instance_id | Monotone Sequence wird akzeptiert. Doppelte oder rückläufige Sequence wird abgelehnt. Keine alte Instanz-ID wird geprüft. |
| N-04 | Dispatcher baut Envelope | Erzeugt `QuestorDispatchEnvelope`. Sendet nicht nacktes `ResearchPackage` im Produktivpfad. Envelope enthält `gate_record_ref`. Envelope enthält konsistente Lease- und Security-Angaben. |
| N-05 | Direkte Pakete sind sandbox-only | Nur erlaubt, wenn Test-/Dev-Konfiguration aktiv ist. `security_mode = DEV_SANDBOX_ONLY`. Keine physische Ausführung. Standardmäßig: `DIRECT_PACKAGE_FORBIDDEN`. |
| N-06 | QuestorMetadata wird nicht wissenschaftlich interpretiert | Keine Kristalle aus `questor_metadata`. Keine Signale aus `questor_metadata`. `operational_metrics` dürfen nur operational verarbeitet werden. |
| N-07 | Blackbox liegt außerhalb der Gremium-Daten | Nicht unter `data/archiv/`. Nicht unter `data/atlas/`. Nicht unter `data/operational_logs/`. Nur unter `data/questor_blackbox/` oder äquivalent isoliert. |

<!-- @section id="3.2" title="Suite I — Integration" type="prose" -->
### §3.2 Suite I — Integration (18 Tests)

<!-- @table schema="test_suite_I" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| I-01 | Happy Path Szenario A | Questor führt aus. Ergebnis: `status: erfolgreich`, `abbruch_grund: null`, `abbruch_klasse: OPERATIONAL`. Archivar empfängt Ergebnis. Kristallkandidaten werden verarbeitet. Keine Blackbox-Inhalte im Gremium. |
| I-02 | Invalides Paket | Questor bricht ab. Vollständiges Ergebnis: `status: abgebrochen`, `abbruch_grund: PACKAGE_INVALID`, `abbruch_klasse: OPERATIONAL`, `vollstaendig_flag: true`. Archivar kann Ergebnis verarbeiten. Keine HAL-Aktion. |
| I-03 | Direktes ResearchPackage verboten | `abbruch_grund: DIRECT_PACKAGE_FORBIDDEN`. `abbruch_klasse: OPERATIONAL`. Vollständiges Ergebnis. |
| I-04 | Envelope ohne gate_record_ref | `abbruch_grund: PACKAGE_INVALID`. `abbruch_klasse: OPERATIONAL`. Vollständiges Ergebnis. |
| I-05 | LEASE_DENIED ohne ESTOP | Zweites Paket erhält `LEASE_DENIED`. Kein ESTOP. Keine `SAFETY`-Klasse. Paket wartet oder bricht operational ab. |
| I-06 | LEASE_QUEUED Timeout | Kein unbegrenztes Warten. Abbruch: `abbruch_grund: LEASE_QUEUED_TIMEOUT`, `abbruch_klasse: OPERATIONAL`. Oder sicherer Sandbox-Fallback gemäß Policy. |
| I-07 | ESTOP während Questor-Ausführung | Aktive Commands stoppen. Leases werden `ESTOP_SUSPENDED`. Ergebnis: `status: abgebrochen`, `abbruch_grund: ESTOP_RECEIVED`, `abbruch_klasse: SAFETY`. Blackbox erhält `SAFETY_HOLD`. Gremium erhält keine Blackbox. |
| I-08 | Operativer Crash OOM | `status: abgebrochen`. `abbruch_grund: OOM`. `abbruch_klasse: OPERATIONAL`. Keine wissenschaftlichen Signale. Optional `resource_pressure_event` durch Gremium/Archivar. |
| I-09 | Wissenschaftlicher Fehlschlag | `status: fehlgeschlagen`. `abbruch_grund: TARGET_NOT_REACHED`. `abbruch_klasse: SCIENTIFIC`. Signalvorschläge erlaubt. Kristallkandidaten möglich. |
| I-10 | Routing-Loop-Schutz | `max_loop_iterations` wird respektiert. Abbruch: `abbruch_grund: ROUTING_LOOP_TIMEOUT`, `abbruch_klasse: OPERATIONAL`. |
| I-11 | Unbekannte Dimension ohne Approval | Keine physische Ausführung. Sandbox/Simulation erlaubt, falls konfiguriert. Sonst: `abbruch_grund: DIMENSION_APPROVAL_MISSING`, `abbruch_klasse: OPERATIONAL`. |
| I-12 | Fracture Diagnosis | Zone ist in QUARANTÄNE, Paket hat `gate_mode = FRACTURE_DIAGNOSIS`. Questor darf diagnostic-safe ausführen. Ergebnis kann diagnostische Kristallkandidaten enthalten. Diagnose-Kristalle werden nicht in normale Cluster-Berechnung übernommen. |
| I-13 | FULL_REBUILD während Questor läuft | Laufendes Paket referenziert alte `atlas_version_id`. `observed_atlas_version_id` bleibt alt. Neuer `atlas_head_pointer` gilt nur für neue Pakete. Keine Invalidierung laufender Quests. |
| I-14 | SAFE_MODE und Questor | Menschliche Königin löst SAFE_MODE aus. Keine neuen Dispatches. Keine neuen Pakete. Keine neue Exploration. Laufende risikoarme Quests dürfen kontrolliert abschließen. Riskante Quests werden pausiert oder sicher abgebrochen. |
| I-15 | Idempotenz im Archivar | Dasselbe `questor_ergebnis_paket` wird zweimal übergeben. Duplikat wird verworfen. Kein doppelter Kristall. Kein doppeltes Signal. Kanonischer `idempotency_key` wird korrekt verglichen. |
| I-16 | Sequence-Recovery nach Questor-Crash | Questor stirbt nach Sequence 7. Nächste Sequence ist 8. Keine Doppelnummer. Keine ungeklärte Lücke. Falls unsicher: `RECOVERY_UNSAFE`. |
| I-17 | Prompt-Injection im Paketkontext | `kontext` enthält eine Anweisung, Sicherheitsregeln zu ignorieren und physische Messung auszuführen. Questor führt keine sicherheitswidrige Aktion aus. LLM-Vorschläge werden verworfen. Keine physische Ausführung ohne deterministische Freigabe. |
| I-18 | Blackbox-Isolation | Gremium-Komponente versucht, QuestorBlackbox zu lesen. Zugriff ist vertraglich verboten. Ergebnis enthält maximal `LocalAuditRef`. Keine Blackbox-Inhalte im Gremium. |

<!-- @section id="3.3" title="Suite S — Szenario-Pflichttests" type="prose" -->
### §3.3 Suite S — Szenario-Pflichttests (5 Tests)

<!-- @table schema="test_suite_S" -->
| Test-ID | Szenario | Fokus |
|---------|----------|-------|
| S-A | Chemie — Kinetik-Optimierung | Happy Path, Envelope, Lease, HAL, Archivar, Kristallkandidaten |
| S-B | Biologie — Zellkultur / UV-Exposition | Routing-Schleife, `max_loop_iterations`, LEASE_DENIED, keine ESTOP durch Ressourcenkonflikt, Langzeit-Prozess mit SAFE_HOLD |
| S-C | Materialwissenschaft — Katalysator-Entdeckung | Gefahren, ESTOP, SAFETY_HOLD, Sicherheitsklassifikation, Hardware-Interlock |
| S-D | Trockenlabor — Hyperparameter-Optimierung | Compute-Job, OOM, operational vs scientific, resource_pressure_metric, CUDA_OOM als OPERATIONAL |
| S-E | Fraktur | Gelbe Fraktur, QUARANTÄNE, FRACTURE_DIAGNOSIS, diagnostische Kristalle, keine normale Cluster-Verzerrung |

<!-- @section id="3.4" title="Suite R — Regressions-Tests" type="prose" -->
### §3.4 Suite R — Regressions-Tests aus v2.3.1 (12 Tests)

<!-- @table schema="test_suite_R" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| R-01 | Crash in Stufe 6 | Recovery bleibt in Stufe 7, nicht Stufe 8. Kein vorzeitiger Questor-Dispatch. |
| R-02 | Slot-Konflikt | LEASE_DENIED. Kein ESTOP. Questor behandelt operational. |
| R-03 | Seher-Halluzination | Veto ohne Evidenz → `SEHER_INVALID_VETO`. Keine blinde Freigabe. Bei Kanzler-Bestätigung Policy-Veto statt rotem Signal. |
| R-04 | Dimensions-Expansion | PROPOSED_BY_IDEA → PROPOSED_BY_WAYPOINT → APPROVED_BEFORE_EXECUTION. Questor blockiert physische Ausführung ohne Approval. |
| R-05 | Gelbe Fraktur | Fraktur-Event korrekt erzeugt. fracture_score korrekt. FRACTURE_DIAGNOSIS möglich. Diagnostische Kristalle bleiben speziell. |
| R-06 | ESTOP vs LEASE_DENIED | Ressourcenkonflikt nie ESTOP. Physikalische Gefahr immer ESTOP. Leases bei ESTOP suspended. |
| R-07 | Operativer Crash | OOM → operational. Kein wissenschaftliches Signal. Optional resource_pressure_event. |
| R-08 | FULL_REBUILD unter Last | Laufende Quests referenzieren alte Atlas-Version. Neuer Head gilt nur für neue Pakete. Alte Version bleibt lesbar. |
| R-09 | Königin-Konflikt | SAFE_MODE. Keine neuen Questor-Dispatches. Menschliche Königin wird nicht überstimmt. |
| R-10 | Totaler Seher-Block | Circuit-Breaker greift. Zustände `SHADOW_MODE`, `TEMP_SUSPENDED` oder `PERMANENT_SUSPENDED` sind explizit definiert. Zustandswechsel werden protokolliert. Automatische Zustandswechsel erfolgen nur bei ausreichender Stichprobe. Rückkehr nach NORMAL erfordert Hysterese und manuelle Prüfung. |
| R-11 | Routing-Loop-Schutz | `max_loop_iterations`. `branch_condition_timeout`. `ROUTING_LOOP_TIMEOUT`. |
| R-12 | Policy-Veto-Review | Review nach `policy_veto_review_interval_cycles`. Standardwert ist 20. Wertebereich ist 1 bis 500. 0 ist ungültig. Review kann bestätigen, aufheben oder eskalieren. Review wird protokolliert. |

<!-- @section id="3.5" title="Suite Z — Zielpräzisierung" type="prose" -->
### §3.5 Suite Z — Zielpräzisierung (8 Tests)

<!-- @table schema="test_suite_Z" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| Z-01 | Kanonische Referenz und Begleitdokument | `structure_standalone_v2.4.0.md` Version 1.1.1 ist primäre Referenz. `structure_hal_v0.2.0.md` ist HAL-spezifische Referenz. `structure_standalone_questor_v0.2.3.md` ist unterstützendes Begleitdokument. Konfliktauflösung ist definiert. Formulierungen im Begleitdokument, die eine primäre Gesamtreferenz beanspruchen, sind nicht bindend. |
| Z-02 | Idempotency-Key-Kanonicalisierung und attempt_id | `idempotency_key = package_id:zyklus_id:attempt_id`. Keine Whitespace. Keine mehrdeutige Serialisierung. `package_id` und `zyklus_id` entsprechen dem erlaubten Regex. `attempt_id >= 0`. `attempt_id <= 999999`. Führende Nullen sind in der kanonischen Form verboten. Maximale Länge des Keys ist 264 Zeichen. Ungültige Eingaben führen zu `PACKAGE_INVALID`. |
| Z-03 | Erfolgssemantik von abbruch_klasse | `status: erfolgreich`. `abbruch_grund: null`. `abbruch_klasse: OPERATIONAL`. Die Semantik ist als Ergebnisklasse dokumentiert. `abbruch_klasse` darf bei Erfolg nicht als tatsächlicher Abbruch interpretiert werden. |
| Z-04 | Circuit-Breaker-Zustände und Metrikfenster | Zustände: `NORMAL`, `SHADOW_MODE`, `TEMP_SUSPENDED`, `PERMANENT_SUSPENDED`. Messfenster ist definiert. Mindeststichprobe ist definiert. Automatische Zustandswechsel erfolgen nur bei ausreichender Stichprobe. Hysterese für Rückkehr nach NORMAL ist definiert. Manuelle Prüfung ist für Rückkehr erforderlich. `PERMANENT_SUSPENDED` hat keine automatische Rückkehr. Audit-Felder enthalten mindestens: `old_state`, `new_state`, `trigger`, `metric_name`, `metric_value`, `window_size`, `sample_size`, `timestamp`, `authority`. |
| Z-05 | Policy-Veto-Review-Parameter | `policy_veto_review_interval_cycles` ist konfigurierbar. Standardwert ist 20. Wertebereich ist 1 bis 500. 0 ist ungültig. Review-Zähler ist persistent. Neustart setzt den Zähler nicht zurück. SAFE_MODE kann die Zählung pausieren, setzt sie aber nicht zurück. Review erzeugt Audit-Event `policy_veto_review`. Audit-Event enthält mindestens: `event_type`, `zyklus_id`, `policy_veto_id`, `review_decision`, `review_reason`, `review_timestamp`, `review_authority`, `escalation_target`. |
| Z-06 | QuestorSpec-Default-Instanz | Ein `ResearchPackage` ohne `questor_spec` wird verarbeitet. Default-Instanz wird angewendet. Defaults sind sicher. `autonomy_level = STRICT`. LLM bleibt Advisor. Keine physische Ausführung bei Unklarheit. `allowed_capabilities` und `allowed_loop_templates` sind leer. Leere Listen bedeuten: keine Capability und kein Template sind standardmäßig freigeschaltet. Physische Ausführung ist ohne explizite Freigabe nicht erlaubt. |
| Z-07 | HAL-Minimalvertrag | HAL bietet mindestens: `get_environment_manifest()`, `get_slot_state()`, `get_zone_state()`, `execute_command()`, `start_process()`, `monitor_process()`, `hold_process()`, `resume_process()`, `abort_process()`, `release_stage()`, `report_estop()`, `report_hardware_interlock()`, `get_estop_state()`, `reconcile_slot_state()`, `reconcile_process_state()`, `get_command_status()`. HAL vergibt keine Leases. HAL interpretiert keine wissenschaftlichen Ziele. HAL prüft `lease_ref` formal oder fragt Resource Governor. Fehler sind klassifiziert als `OPERATIONAL` oder `SAFETY`. ESTOP-Zustände sind: `NORMAL`, `ACTIVE`, `LATCHED`, `TEST`. ESTOP stoppt aktive Kommandos. ESTOP suspendiert betroffene Leases. Questor darf ESTOP nicht zurücksetzen. HAL protokolliert operational. Dummy-HAL kann alle relevanten Fehlermodi simulieren. |
| Z-08 | N-01-Scanbereich und Allowlist | N-01 sucht in produktiven Quellen. Migrations-/Archiv-/Testdokumente sind ausgenommen. Allowlist-Dateien sind zulässig, wenn explizit gekennzeichnet. Allowlist enthält mindestens: `path`, `pattern`, `reason`, `approved_until`, `owner`, `review_required`. Allowlists dürfen keine produktiven Laufzeitquellen freischalten. Allowlists sollten zeitlich begrenzt und review-pflichtig sein. |

<!-- @section id="3.6" title="Suite H — HAL v0.2.0" type="prose" -->
### §3.6 Suite H — HAL v0.2.0 (24 Tests)

<!-- @table schema="test_suite_H" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| H-01 | EnvironmentManifest ist vollständig | Manifest enthält Slots, Zonen, Capabilities, Timeout-Grenzen, ESTOP-Mechanismus, Resource-Classes, `supported_security_modes`. |
| H-02 | Kommando ohne Lease wird abgelehnt | `status: DENIED`. `error_code: LEASE_INVALID`. `error_class: OPERATIONAL`. Keine Ausführung. |
| H-03 | Ungültige Lease wird abgelehnt | `status: DENIED`. `error_code: LEASE_INVALID`. Keine Ausführung. |
| H-04 | Abgelaufene Lease wird abgelehnt | `status: DENIED`. `error_code: LEASE_EXPIRED`. Keine Ausführung. |
| H-05 | Slot-Mutex verhindert parallele Ausführung | Zweites Kommando erhält `SLOT_BUSY` oder `DENIED`. Kein paralleler physischer Zugriff. |
| H-06 | Zonen-Mutex verhindert parallele Zonen-Nutzung | Zweites Kommando erhält `ZONE_LOCK_UNAVAILABLE`. Kein paralleler Zugriff auf gemeinsame Schiene. |
| H-07 | ESTOP blockiert neue Kommandos | `status: ESTOP`. Keine neue Ausführung. `error_class: SAFETY`. |
| H-08 | Hardware-Interlock blockiert neue Kommandos | `status: INTERLOCK`. Keine neue Ausführung. `error_class: SAFETY`. `interlock_latched: true`. `physical_reset_required: true`. |
| H-09 | ESTOP suspendiert betroffene Leases | Resource Governor wird informiert. Betroffene Leases werden als suspendiert betrachtet. Questor erhält Sicherheitsabbruch. |
| H-10 | Hardware-Interlock suspendiert betroffene Leases und Zonen | Resource Governor wird informiert. Betroffene Leases werden als suspendiert betrachtet. Betroffene Zonen werden als `INTERLOCKED` betrachtet. Questor erhält Sicherheitsabbruch. |
| H-11 | Timeout führt zu operationalem Fehler | `status: TIMEOUT`. `error_code: COMMAND_TIMEOUT`. `error_class: OPERATIONAL`. Kein ESTOP. |
| H-12 | Timeout bei physischem Slot kann Reconciliation auslösen | Slot kann auf `ERROR` gehen. `reconcile_slot_state` erforderlich. Kein blinder Retry. |
| H-13 | Duplicate Command wird blockiert | `status: DUPLICATE_BLOCKED`. Keine erneute Ausführung. Keine doppelten Seiteneffekte. |
| H-14 | Crash-Recovery ohne blinden Retry | Nach unklarem Crash wird nicht automatisch neu ausgeführt. `RECOVERY_UNSAFE` möglich. Slot bleibt kontrolliert gesperrt bis Klärung. |
| H-15 | HAL schreibt nur operational Logs | Logs landen in `data/operational_logs/`. Keine Atlas-Einträge. Keine Archiv-Einträge. Keine Blackbox-Einträge. |
| H-16 | Physische Ausführung nur bei passendem Security-Mode | `SANDBOX` oder `DEV_SANDBOX_ONLY` führt nicht physisch aus. `NORMAL` darf physisch ausführen, wenn Lease und Slot es erlauben. Verstöße führen zu `PHYSICAL_EXECUTION_FORBIDDEN`. |
| H-17 | Compute-Ausführung nur bei passendem Security-Mode | `SANDBOX` oder `DEV_SANDBOX_ONLY` führt nicht echt aus. `NORMAL` darf Compute ausführen, wenn Lease und Slot es erlauben. Verstöße führen zu `COMPUTE_EXECUTION_FORBIDDEN`. |
| H-18 | Langzeit-Prozess mit SAFE_HOLD | Prozess wird gestartet. Prozess läuft für erwartete Dauer. Bei Lease-Expiry: Prozess geht in `SAFE_HOLD`. Prozess wird nicht zerstört. `resume_token` wird erzeugt. |
| H-19 | Langzeit-Prozess mit RESUME | Prozess wird gestartet. Prozess geht in `SAFE_HOLD`. `resume_process` mit gültigem `resume_token` wird aufgerufen. Prozess wird fortgesetzt. `process_state` geht von `SAFE_HOLD` nach `RUNNING`. |
| H-20 | Langzeit-Prozess mit WAITING_FOR_RELEASE | Prozess wird gestartet. Erste Stufe wird abgeschlossen. Prozess geht in `WAITING_FOR_RELEASE`. `release_stage` wird aufgerufen. Prozess wird fortgesetzt. `process_state` geht von `WAITING_FOR_RELEASE` nach `RUNNING`. |
| H-21 | Langzeit-Prozess mit Stage-Release-Denied | Prozess wird gestartet. Erste Stufe wird abgeschlossen. Prozess geht in `WAITING_FOR_RELEASE`. `release_stage` wird ohne Berechtigung aufgerufen. `STAGE_RELEASE_DENIED` wird zurückgegeben. Prozess bleibt in `WAITING_FOR_RELEASE`. |
| H-22 | CUDA-OOM ist operational | `status: ERROR`. `error_code: CUDA_OOM`. `error_class: OPERATIONAL`. Kein ESTOP. Keine Sicherheitsprüfung. |
| H-23 | Parameter-Schema-Validierung | Kommando mit gültigem Schema wird akzeptiert. Kommando mit unbekanntem Schema wird abgelehnt. Kommando mit falscher Checksumme wird abgelehnt. Fehlercode: `PARAMETER_SCHEMA_UNKNOWN` oder `PARAMETER_CHECKSUM_MISMATCH`. Fehlerklasse: `OPERATIONAL`. |
| H-24 | Dummy-HAL kann alle Fehlermodi simulieren | Alle definierten Fehlermodi sind testbar. Simulation ist deterministisch. Keine echte Hardware beteiligt. |

<!-- @section id="4" title="Neue Questor-Test-Suiten" type="prose" -->
## §4 Neue Questor-Test-Suiten

<!-- @section id="4.1" title="Suite Q-U — Questor Unit-Tests" type="prose" -->
### §4.1 Suite Q-U — Questor Unit-Tests (~252 Tests)

#### §4.1.1 `sanitization.py` (18 Tests)
<!-- @table schema="test_suite_Q_U_SAN" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-SAN-01 | Feld-Whitelist: Nur erlaubte Felder passieren | Nicht-erlaubte Felder werden entfernt |
| U-SAN-02 | Feld-Blocklist: `atlas_version_ref`, `gate_record_ref` werden blockiert | Blockierte Felder sind nicht im Output |
| U-SAN-03 | Injection-Pattern INJ-01: `"ignore all previous instructions"` | `injection_detected = true`, Feld wird quarantänen |
| U-SAN-04 | Injection-Pattern INJ-04: `"ESTOP"` im Freitext | `injection_detected = true`, Feld wird quarantänen |
| U-SAN-05 | Injection-Pattern INJ-05: `"setze ESTOP zurück"` | `injection_detected = true`, Feld wird quarantänen |
| U-SAN-06 | Control-Characters werden entfernt | Output enthält keine Control-Chars |
| U-SAN-07 | Zero-Width-Chars werden entfernt | Output enthält keine Zero-Width-Chars |
| U-SAN-08 | Text über `max_length` wird abgeschnitten | Text ist auf `max_length` begrenzt |
| U-SAN-09 | `parameter_bounds` mit NaN wird verworfen | Feld wird verworfen, Warning |
| U-SAN-10 | `parameter_bounds` mit Infinity wird verworfen | Feld wird verworfen, Warning |
| U-SAN-11 | LLM-Output ist kein JSON → PARSE_ERROR | `status = PARSE_ERROR`, Fallback |
| U-SAN-12 | LLM-Output enthält Safety-Keyword → SAFETY_REJECT | `status = SAFETY_REJECT`, Fallback |
| U-SAN-13 | LLM-Output verletzt parameter_bounds → INVALID | `status = INVALID`, Fallback |
| U-SAN-14 | LLM-Output außerhalb allowed_capabilities → INVALID | `status = INVALID`, Fallback |
| U-SAN-15 | LLM-Timeout → Fallback | Deterministischer Fallback wird verwendet |
| U-SAN-16 | `sanitize_for_llm` gibt `SanitizationResult` zurück | Struktur ist korrekt |
| U-SAN-17 | Leerer Kontext → kein Fehler | Leerer Kontext wird akzeptiert |
| U-SAN-18 | XML-Tag-Escaping: `<konzept>` im Freitext wird escaped | `<` → `&lt;`, `>` → `&gt;` |

#### §4.1.2 `capability_registry.py` (22 Tests)
<!-- @table schema="test_suite_Q_U_CAP" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-CAP-01 | Registry laden: gültige YAML-Dateien | Registry wird geladen, `capability_count` korrekt |
| U-CAP-02 | Registry laden: ungültige YAML-Datei | Questor startet nicht, Fehler wird protokolliert |
| U-CAP-03 | Registry laden: doppelte `capability_id` | Questor startet nicht, Fehler wird protokolliert |
| U-CAP-04 | `check_capability`: Capability in Registry, HAL, Package | `status = AVAILABLE` |
| U-CAP-05 | `check_capability`: Capability nicht in Registry | `status = UNKNOWN` |
| U-CAP-06 | `check_capability`: Capability deprecated | `status = DEPRECATED` |
| U-CAP-07 | `check_capability`: Capability nicht in HAL-Manifest | `status = UNAVAILABLE` |
| U-CAP-08 | `check_capability`: Capability nicht in allowed_capabilities | `status = SECURITY_RESTRICTED` |
| U-CAP-09 | `check_capability`: Security-Mode passt nicht | `status = SECURITY_RESTRICTED` |
| U-CAP-10 | `validate_parameters`: Alle Pflichtfelder vorhanden | Keine Fehler |
| U-CAP-11 | `validate_parameters`: Pflichtfeld fehlt | `MISSING_REQUIRED_PARAMETER` |
| U-CAP-12 | `validate_parameters`: FLOAT außerhalb Bounds | `BELOW_MIN` oder `ABOVE_MAX` |
| U-CAP-13 | `validate_parameters`: STRING zu lang | `TOO_LONG` |
| U-CAP-14 | `validate_parameters`: ENUM-Wert ungültig | `INVALID_ENUM` |
| U-CAP-15 | `validate_parameters`: NaN | `NAN_PARAMETER` |
| U-CAP-16 | `validate_parameters`: Infinity | `INFINITY_PARAMETER` |
| U-CAP-17 | `get_slots_for_capability`: Ein Slot verfügbar | Liste mit einer Slot-ID |
| U-CAP-18 | `get_slots_for_capability`: Mehrere Slots verfügbar | Liste mit mehreren Slot-IDs |
| U-CAP-19 | `get_slots_for_capability`: Kein Slot verfügbar | Leere Liste |
| U-CAP-20 | `capabilities_available`: Alle Capabilities verfügbar | `True` |
| U-CAP-21 | `capabilities_available`: Eine Capability fehlt | `False` |
| U-CAP-22 | Integritäts-Hash der Registry | Hash ist deterministisch und reproduzierbar |

#### §4.1.3 `security_mode.py` (11 Tests)
<!-- @table schema="test_suite_Q_U_SM" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-SM-01 | `get_effective_security_mode`: Paket NORMAL, Gate NORMAL, System NORMAL | `NORMAL` |
| U-SM-02 | `get_effective_security_mode`: Paket NORMAL, Gate SANDBOX | `SANDBOX` (restriktiver) |
| U-SM-03 | `get_effective_security_mode`: Paket NORMAL, System RECOVERY | `RECOVERY` (restriktiver) |
| U-SM-04 | `validate_package_security_mode`: Paket-Modus nicht in Gate | `PackageInvalidError` |
| U-SM-05 | `validate_package_security_mode`: Paket-Modus in Gate | `True` |
| U-SM-06 | `filter_templates_by_security_mode`: RECOVERY | Nur `is_recovery_template = true` |
| U-SM-07 | `filter_templates_by_security_mode`: SANDBOX | Nur Templates mit `allowed_security_modes ⊇ {SANDBOX}` |
| U-SM-08 | `policy_check_security_mode`: Physische Actuation in SANDBOX | `VETO` |
| U-SM-09 | `policy_check_security_mode`: Physische Actuation in NORMAL | `GO` |
| U-SM-10 | `policy_check_security_mode`: RECOVERY mit nicht-Recovery-Capability | `VETO` |
| U-SM-11 | `security_mode` fehlt im Paket | `PACKAGE_INVALID` |

#### §4.1.4 `shutdown.py` (13 Tests)
<!-- @table schema="test_suite_Q_U_SD" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-SD-01 | SIGTERM empfangen | `shutdown_requested = true`, Timer startet |
| U-SD-02 | Graceful-Shutdown in IDLE | Sofort beenden, `ShutdownResult.status = COMPLETED` |
| U-SD-03 | Graceful-Shutdown in EXECUTING | HAL-Kommando abwarten, Ergebnis bauen |
| U-SD-04 | Graceful-Shutdown in FINALIZING | Ergebnis fertigstellen, dann beenden |
| U-SD-05 | Graceful-Shutdown-Timeout erreicht | Force-Shutdown |
| U-SD-06 | WAL-Flush bei Shutdown | WAL wird flush'd |
| U-SD-07 | WAL-Flush fehlschlägt | Force-Shutdown |
| U-SD-08 | Ergebnis bei Shutdown bauen | `abbruch_grund = GRACEFUL_SHUTDOWN`, `abbruch_klasse = OPERATIONAL` |
| U-SD-09 | Langzeit-Prozess bei Shutdown | SAFE_HOLD anfragen |
| U-SD-10 | SAFE_HOLD fehlschlägt bei Shutdown | Prozess abbrechen |
| U-SD-11 | Leases bei Shutdown freigeben | Leases werden freigegeben |
| U-SD-12 | Blackbox bei Shutdown schreiben | Blackbox wird geschrieben |
| U-SD-13 | ESTOP hat Vorrang vor Shutdown | `abbruch_grund = ESTOP_RECEIVED`, nicht `GRACEFUL_SHUTDOWN` |

#### §4.1.5 `health_monitor.py` (15 Tests)
<!-- @table schema="test_suite_Q_U_HM" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-HM-01 | Heartbeat schreiben | `health.json` wird geschrieben |
| U-HM-02 | Heartbeat atomar schreiben (temp + rename) | Keine korrupte Datei |
| U-HM-03 | Heartbeat bei Disk-Full | Fehler protokolliert, Questor arbeitet weiter |
| U-HM-04 | Watchdog: Zustandsdauer überschritten | `watchdog_status = CRITICAL` |
| U-HM-05 | Watchdog: Speicherverbrauch zu hoch | `watchdog_status = WARNING` |
| U-HM-06 | Watchdog: CPU-Auslastung zu hoch | `watchdog_status = WARNING` |
| U-HM-07 | Watchdog: Kein Fortschritt | `watchdog_status = CRITICAL` |
| U-HM-08 | Watchdog: EXECUTING hat kein Zeitlimit | Kein Alarm bei langer EXECUTING-Dauer |
| U-HM-09 | Watchdog: WAITING_FOR_RELEASE hat kein Zeitlimit | Kein Alarm bei langer Wartezeit |
| U-HM-10 | `determine_health_status`: Alle Checks OK | `HEALTHY` |
| U-HM-11 | `determine_health_status`: Heartbeat veraltet | `UNHEALTHY` |
| U-HM-12 | `determine_health_status`: Prozess läuft nicht | `DEAD` |
| U-HM-13 | Externer Monitor: `health.json` lesen | `HealthCheckResult` korrekt |
| U-HM-14 | Externer Monitor: `health.json` fehlt | `overall_status = DEAD` |
| U-HM-15 | Alert-Cooldown | Kein zweiter Alert innerhalb von `alert_cooldown_s` |

#### §4.1.6 `trail_map.py` (11 Tests)
<!-- @table schema="test_suite_Q_U_TRAIL" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-TRAIL-01 | Trail erstellen mit `create_trails = true` | Trail wird erstellt |
| U-TRAIL-02 | Trail erstellen mit `create_trails = false` | Trail wird NICHT erstellt |
| U-TRAIL-03 | Trail mit `require_evidence = true` und Evidenz vorhanden | Trail wird erstellt |
| U-TRAIL-04 | Trail mit `require_evidence = true` und keine Evidenz | Trail wird erstellt mit `EVIDENCE_MISSING` |
| U-TRAIL-05 | Trail-Map finalisieren | `access_level = READ_ONLY`, `integrity_hash` berechnet |
| U-TRAIL-06 | TrailMapSummary erstellen | `trail_count`, `decision_type_counts` korrekt |
| U-TRAIL-07 | Trail-Append-Only: Trail nach Finalisierung hinzufügen | Fehler, Trail wird nicht hinzugefügt |
| U-TRAIL-08 | Trail-Map in Blackbox speichern | Datei wird geschrieben |
| U-TRAIL-09 | Trail-Map-Hash mit Ledger-Hash vergleichen | Hashes stimmen überein |
| U-TRAIL-10 | Trail mit `trail_detail_level = MINIMAL` | Nur `decision_type`, `chosen_alternative_id`, `reasoning` |
| U-TRAIL-11 | Trail mit `trail_detail_level = FULL` | Alle Felder vorhanden |

#### §4.1.7 `queue_integration.py` (14 Tests)
<!-- @table schema="test_suite_Q_U_QI" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| U-QI-01 | Dispatcher schreibt Envelope in `pending/` | Datei wird erstellt, Registry aktualisiert |
| U-QI-02 | Dispatcher schreibt dupliziertes Envelope | Duplikat wird abgelehnt |
| U-QI-03 | Dispatcher schreibt ohne `gate_record_ref` | Fehler, Envelope wird nicht geschrieben |
| U-QI-04 | Questor liest ältestes Paket aus `pending/` | Ältestes Paket wird genommen |
| U-QI-05 | Questor verschiebt Envelope nach `processing/` | Datei wird verschoben, Registry aktualisiert |
| U-QI-06 | Questor schreibt Result nach `completed/` | Datei wird erstellt, Registry aktualisiert |
| U-QI-07 | Questor schreibt Result nach `failed/` | Datei wird erstellt, Registry aktualisiert |
| U-QI-08 | Receiver liest Result aus `completed/` | `QuestorErgebnisPaket` wird gelesen |
| U-QI-09 | Receiver validiert `vollstaendig_flag` | `false` → Ergebnis wird nicht verarbeitet |
| U-QI-10 | Delete-Request für Paket in `pending/` | Paket wird gelöscht |
| U-QI-11 | Delete-Request für Paket in `processing/` | Paket wird NICHT gelöscht |
| U-QI-12 | Registry-Lock: Zwei Prozesse schreiben gleichzeitig | Kein Race Condition |
| U-QI-13 | Envelope-Datei ist korrupt | `QUEUE_FILE_CORRUPT`, Datei wird quarantänen |
| U-QI-14 | `registry.json` ist korrupt | Registry wird aus Dateien rekonstruiert |

#### §4.1.8 Weitere Module (~148 Tests)
<!-- @table schema="test_suite_Q_U_other" -->
| Modul | Test-Anzahl | Schwerpunkte |
|-------|-------------|--------------|
| objective_parser.py | 10 | Keyword-Matching, Clarity-Score |
| compass.py | 20 | Loop Selection, Ranking, Candidate-Window |
| policy_evaluator.py | 15 | Alle 8 Prüfungen, VETO/GO |
| loop_registry.py | 10 | Template laden, validieren, filtern |
| ledger.py | 15 | Hash-Chain, Genesis-Hash, NaN/Infinity |
| safety_monitor.py | 10 | ESTOP, Interlock, Timeout |
| recovery.py | 12 | WAL lesen, Checkpoint finden, Reconcile |
| sequence.py | 8 | Atomare Persistierung, Datei-Lock |
| hal_bridge.py | 20 | Übersetzung, Ergebnisverarbeitung, Idempotenz |
| result_builder.py | 20 | Feldzuordnung, Kristallkandidaten, Signale |
| blackbox_archiver.py | 8 | Retention-Class, Limits, Rotation |

<!-- @section id="4.2" title="Suite Q-C — Questor Komponententests" type="prose" -->
### §4.2 Suite Q-C — Questor Komponententests (~44 Tests)

#### §4.2.1 QuestCompass (15 Tests)
<!-- @table schema="test_suite_Q_C_QC" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| C-QC-01 | Objective Analysis: `objective_type` explizit gesetzt | Stufe 1 wird verwendet, kein LLM |
| C-QC-02 | Objective Analysis: Keyword-Matching | Stufe 2 wird verwendet |
| C-QC-03 | Objective Analysis: LLM-Clarification | Stufe 2.5 wird verwendet |
| C-QC-04 | Objective Analysis: LLM-Ausfall | Fail-Closed, `ABORT_IF_UNCLEAR` |
| C-QC-05 | Loop Selection: Ein Template verfügbar | Direkt wählen, kein LLM |
| C-QC-06 | Loop Selection: Mehrere Templates, STRICT | Top-1 wählen, kein LLM |
| C-QC-07 | Loop Selection: Mehrere Templates, GUIDED | Top-3, LLM bei Score-Diff < 0.15 |
| C-QC-08 | Loop Selection: FRACTURE_DIAGNOSIS | STRICT erzwingen, nur DIAGNOSE-Templates |
| C-QC-09 | Evaluation: OPTIMIZE, Konfidenz ≥ Threshold | ZIEL ERREICHT |
| C-QC-10 | Evaluation: OPTIMIZE, Konfidenz < Threshold | RE-PLANUNG |
| C-QC-11 | Decision Engine: ESTOP aktiv | SOFORT ABBRUCH (SAFETY) |
| C-QC-12 | Decision Engine: Budget erschöpft | ABBRUCH (BUDGET_EXHAUSTED) |
| C-QC-13 | Decision Engine: Ziel unerreichbar | ABBRUCH (TARGET_NOT_REACHABLE, SCIENTIFIC) |
| C-QC-14 | Gesamter Zyklus: PLAN → EXECUTE → EVALUATE → RE-PLAN | Korrekte Zustandsübergänge |
| C-QC-15 | LLM-Advice wird abgelehnt | Deterministische Entscheidung gewinnt |

#### §4.2.2 PolicyEvaluator (9 Tests)
<!-- @table schema="test_suite_Q_C_PE" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| C-PE-01 | Alle Prüfungen bestanden | GO |
| C-PE-02 | ESTOP aktiv | VETO (SAFETY_ACTIVE) |
| C-PE-03 | Außerhalb Routing-Graph | VETO (OUTSIDE_ROUTING_GRAPH) |
| C-PE-04 | Capability nicht verfügbar | VETO (CAPABILITY_UNAVAILABLE) |
| C-PE-05 | Budget überschritten | VETO (BUDGET_EXCEEDED) |
| C-PE-06 | Security-Mode passt nicht | VETO (SECURITY_MODE_MISMATCH) |
| C-PE-07 | Einfachere Alternative existiert | VETO (SIMPLER_ALTERNATIVE_EXISTS) |
| C-PE-08 | Dimension-Approval fehlt | VETO (DIMENSION_APPROVAL_MISSING) |
| C-PE-09 | Kombination: ESTOP + Budget überschritten | VETO (SAFETY_ACTIVE hat Vorrang) |

#### §4.2.3 HAL-Bridge (10 Tests)
<!-- @table schema="test_suite_Q_C_HB" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| C-HB-01 | LoopStep → HALCommand übersetzen | Korrekte Felder |
| C-HB-02 | LoopStep → ProcessCommand übersetzen | Korrekte Felder |
| C-HB-03 | HALCommandResult SUCCESS → Weiter im Loop | `BridgeResult.status = SUCCESS` |
| C-HB-04 | HALCommandResult ESTOP → SAFETY_ABORT | `BridgeResult.status = SAFETY_ABORT` |
| C-HB-05 | HALCommandResult LEASE_DENIED → OPERATIONAL_ABORT | `BridgeResult.status = OPERATIONAL_ABORT` |
| C-HB-06 | HALCommandResult DUPLICATE_BLOCKED → SUCCESS | `BridgeResult.status = SUCCESS` |
| C-HB-07 | Parameter-Validierung vor Senden | Ungültige Parameter → nicht senden |
| C-HB-08 | Idempotenz-Key erzeugen | `command_id:lease_ref:slot_id` |
| C-HB-09 | Kosten aktualisieren nach Ausführung | `accumulated_cost` korrekt |
| C-HB-10 | Prozess in SAFE_HOLD versetzen | `ProcessResult.process_state = SAFE_HOLD` |

#### §4.2.4 Result-Builder (10 Tests)
<!-- @table schema="test_suite_Q_C_RB" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| C-RB-01 | Ergebnis bei Erfolg bauen | `status = erfolgreich`, `abbruch_klasse = OPERATIONAL` |
| C-RB-02 | Ergebnis bei OPERATIONAL-Abbruch bauen | `status = abgebrochen`, `abbruch_klasse = OPERATIONAL` |
| C-RB-03 | Ergebnis bei SCIENTIFIC-Abbruch bauen | `status = fehlgeschlagen`, `abbruch_klasse = SCIENTIFIC` |
| C-RB-04 | Ergebnis bei SAFETY-Abbruch bauen | `kristall_kandidaten = []`, `signale_fuer_atlas = []` |
| C-RB-05 | Early-Abort-Ergebnis bauen | `vollstaendig_flag = true`, alle Pflichtfelder gesetzt |
| C-RB-06 | Kristallkandidaten aus Evaluation erzeugen | Korrekte `konfidenz`, `loop_template`, `loop_parameter` |
| C-RB-07 | Signale aus Kristallkandidaten erzeugen | Korrekte `signal_typ`, `zone_ref` |
| C-RB-08 | Guardian-Validierung: Hash-Chain prüfen | `guardian_status = PASS` |
| C-RB-09 | Guardian-Validierung: NaN in ergebnis_daten | `guardian_status = FAIL` |
| C-RB-10 | Blackbox schreiben | `retention_class` korrekt |

<!-- @section id="4.3" title="Suite Q-S — Questor Sicherheits-Tests" type="prose" -->
### §4.3 Suite Q-S — Questor Sicherheits-Tests (~30 Tests)

#### §4.3.1 Prompt-Injection (10 Tests)
<!-- @table schema="test_suite_Q_S_PI" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| SEC-PI-01 | Injection über `ziel` | Feld wird quarantänen, LLM-Aufruf ohne `ziel` |
| SEC-PI-02 | Injection über `kontext.zusammenfassung` | Feld wird quarantänen |
| SEC-PI-03 | Injection über `planning_hints.hinweis_text` | Feld wird quarantänen |
| SEC-PI-04 | Injection auf Deutsch | Deutsche Patterns werden erkannt |
| SEC-PI-05 | Injection auf Englisch | Englische Patterns werden erkannt |
| SEC-PI-06 | Injection mit Unicode-Escapes | Unicode-Escapes werden erkannt |
| SEC-PI-07 | Injection mit Base64-encoding | Base64-Pattern wird erkannt |
| SEC-PI-08 | Injection im LLM-Output | SAFETY_REJECT, Fallback |
| SEC-PI-09 | Mehrere Injections in einem Feld | Alle werden erkannt, Feld wird quarantänen |
| SEC-PI-10 | Injection in `parameter_bounds` Key | Key wird verworfen |

#### §4.3.2 Capability-Bypass (5 Tests)
<!-- @table schema="test_suite_Q_S_CB" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| SEC-CB-01 | Template fordert nicht registrierte Capability | VETO (CAPABILITY_UNAVAILABLE) |
| SEC-CB-02 | Template fordert Capability außerhalb allowed_capabilities | VETO (SECURITY_RESTRICTED) |
| SEC-CB-03 | LLM schlägt Capability außerhalb allowed_capabilities vor | Vorschlag wird verworfen |
| SEC-CB-04 | Capability mit `requires_physical_actuation = true` in SANDBOX | VETO |
| SEC-CB-05 | Capability mit `requires_dimension_approval = true` ohne Approval | VETO |

#### §4.3.3 Security-Mode-Eskalation (5 Tests)
<!-- @table schema="test_suite_Q_S_SM" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| SEC-SM-01 | Paket fordert NORMAL, Gate erlaubt nur SANDBOX | PACKAGE_INVALID |
| SEC-SM-02 | Paket fordert NORMAL, Slot ist nur sandbox_capable | PHYSICAL_EXECUTION_FORBIDDEN |
| SEC-SM-03 | LLM versucht, security_mode zu ändern | LLM-Output wird verworfen |
| SEC-SM-04 | Security-Mode wird während Ausführung geändert | Nicht möglich (Read-Only im Kontext) |
| SEC-SM-05 | RECOVERY-Modus mit physischer Capability | VETO |

#### §4.3.4 WAL-Manipulation (3 Tests)
<!-- @table schema="test_suite_Q_S_WAL" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| SEC-WAL-01 | WAL-Datei wird extern verändert | Hash-Chain-Prüfung schlägt fehl, RECOVERY_UNSAFE |
| SEC-WAL-02 | WAL-Datei wird gelöscht | RECOVERY_UNSAFE |
| SEC-WAL-03 | WAL-Eintrag wird nachträglich geändert | Hash-Chain-Prüfung schlägt fehl |

#### §4.3.5 Queue-Manipulation (5 Tests)
<!-- @table schema="test_suite_Q_S_QM" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| SEC-QM-01 | Envelope-Datei wird extern verändert | Validierung schlägt fehl, PACKAGE_INVALID |
| SEC-QM-02 | Result-Datei wird extern verändert | Receiver-Validierung schlägt fehl |
| SEC-QM-03 | Registry.json wird extern verändert | Registry wird aus Dateien rekonstruiert |
| SEC-QM-04 | Delete-Request-Datei wird extern verändert | Questor prüft Integrität, ungültiger Request wird ignoriert |
| SEC-QM-05 | Zwei Prozesse schreiben gleichzeitig in registry.json ohne Lock | Lock verhindert Race Condition |

#### §4.3.6 LLM-Output-Manipulation (2 Tests)
<!-- @table schema="test_suite_Q_S_LLM" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| SEC-LLM-01 | LLM-Output enthält versteckte JSON-Instruktionen | Schema-Validierung lehnt unbekannte Felder ab |
| SEC-LLM-02 | LLM-Output enthält Unicode-Escapes die bei Dekodierung Injektionen ergeben | Sanitization erkennt und blockiert |

<!-- @section id="4.4" title="Suite Q-P — Questor Performance-Tests" type="prose" -->
### §4.4 Suite Q-P — Questor Performance-Tests (~10 Tests)

<!-- @table schema="test_suite_Q_P" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| PERF-01 | Paket-Validierung (Envelope) | < 100ms |
| PERF-02 | Objective Analysis (deterministisch) | < 50ms |
| PERF-03 | Loop Selection (5 Templates) | < 200ms |
| PERF-04 | PolicyEvaluator (alle 8 Prüfungen) | < 100ms |
| PERF-05 | HALCommand-Übersetzung | < 50ms |
| PERF-06 | Result-Builder (Ergebnis bauen) | < 200ms |
| PERF-07 | WAL-Schreiben (100 Einträge) | < 500ms |
| PERF-08 | Ledger-Hash-Chain (100 Einträge) | < 500ms |
| PERF-09 | Trail-Map erstellen (50 Trails) | < 200ms |
| PERF-10 | Heartbeat schreiben | < 50ms |

<!-- @section id="4.5" title="Suite Q-T — Questor Stress-Tests" type="prose" -->
### §4.5 Suite Q-T — Questor Stress-Tests (~11 Tests)

<!-- @table schema="test_suite_Q_T" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRESS-01 | Queue mit 100 Paketen in `pending/` | Questor verarbeitet sequentiell, ältestes zuerst |
| STRESS-02 | WAL mit 10.000 Einträgen | Recovery funktioniert, Hash-Chain prüft |
| STRESS-03 | Ledger mit 5.000 Einträgen | Ergebnis wird korrekt gebaut |
| STRESS-04 | Disk zu 95% voll | Heartbeat wird geschrieben, Warning |
| STRESS-05 | Disk zu 100% voll | Fehler wird protokolliert, Questor arbeitet weiter (soweit möglich) |
| STRESS-06 | 10 LLM-Aufrufe gleichzeitig (max_calls = 3) | Nur 3 werden ausgeführt, Rest wird abgelehnt |
| STRESS-07 | Template-Registry mit 500 Templates | Laden < 5 Sekunden |
| STRESS-08 | Capability-Registry mit 200 Capabilities | Laden < 2 Sekunden |
| LOAD-01 | 10 Pakete in 24 Stunden | Alle werden verarbeitet |
| LOAD-02 | 1 Paket mit 100 Iterationen | Budget wird korrekt getrackt |
| LOAD-03 | 1 Langzeit-Prozess (72h) | SAFE_HOLD und RESUME funktionieren |

<!-- @section id="4.6" title="Suite ATLAS — Atlas-Hybrid-Tests" type="prose" -->
### §4.6 Suite ATLAS — Atlas-Hybrid-Tests (~120 Tests)

Die vollständige Spezifikation der Atlas-Hybrid-Test-Suite ist in `ops/VALIDATION_ATLAS.md` definiert.

#### §4.6.1 Übersicht der Atlas-Test-Bereiche
<!-- @table schema="atlas_test_areas" -->
| Bereich | Test-Präfix | Anzahl | Zweck |
|---------|-------------|--------|-------|
| Verträge | ATLAS-CTR | ~15 | Pydantic-Validierung der Atlas-Hybrid-Verträge |
| Semantik | ATLAS-SEM | ~20 | Evidence-Semantik, Erwartungsprüfung |
| Topologie | ATLAS-TOPO | ~15 | Dimensionen, Zonen, Knoten, Kanten |
| Integrität | ATLAS-INT | ~15 | Fracture, Confidence, Uncertainty, Zone-Health |
| Diagnostik | ATLAS-DIAG | ~10 | DiagnosticResolution, Heilung |
| Sicherheit | ATLAS-SAF | ~10 | SafetyConstraint, ExclusionConstraint, LOCKED |
| Frontier | ATLAS-FRNT | ~15 | FrontierEngine, FrontierCandidate |
| Themen | ATLAS-TOP | ~10 | ResearchTopic, ExplorationPolicy |
| Domänen | ATLAS-DOM | ~10 | Chemie, Biologie, Physik, ML Integration |
| **Gesamt** | | **~120** | |

#### §4.6.2 Referenz
→ Siehe `ops/VALIDATION_ATLAS.md` für die vollständige Test-Spezifikation.

<!-- @section id="4.7" title="Suite STRAT — Strategic-Layer-Tests" type="prose" -->
### §4.7 Suite STRAT — Strategic-Layer-Tests (~170 Tests)

#### §4.7.1 Übersicht der STRAT-Test-Bereiche
<!-- @table schema="strat_test_areas" -->
| Bereich | Test-Präfix | Anzahl | Zweck |
|---------|-------------|--------|-------|
| Verträge | STRAT-CTR | ~20 | Pydantic-Validierung der Strategic-Layer-Verträge |
| Achsen & ControlState | STRAT-AX | ~40 | Achsen-Zustandsmaschine, SL-AX-ATOMIC, Closure-Regeln |
| Kanzler & DTT | STRAT-KANZ | ~55 | Validierungspipeline, DTT, Blocklists, Konfliktdetektor |
| Königin & Briefing | STRAT-KOEN | ~25 | Constitutional Anchor, Briefing-Erzeugung, Sanitization |
| Symptom-Trigger & Signal | STRAT-SYM | ~15 | SymptomEvents, Signal-Semantik, SL-SIG-7a |
| End-to-End | STRAT-E2E | ~15 | Vollständiger Briefing → Directive → Policy-Zyklus |
| **Gesamt** | | **~170** | |

#### §4.7.2 STRAT-CTR — Vertrags-Tests (~20 Tests)
<!-- @table schema="test_suite_STRAT_CTR" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRAT-CTR-01 | `ControlState` validiert mit gültigem Tupel | Pydantic-Validierung erfolgreich |
| STRAT-CTR-02 | `ControlState` mit ungültigem SafetyAxis-Wert | Validierungsfehler |
| STRAT-CTR-03 | `AxisTransition` mit gültigem `batch_id` | Pydantic-Validierung erfolgreich |
| STRAT-CTR-04 | `AxisTransition` mit ungültigem `axis`-Wert | Validierungsfehler |
| STRAT-CTR-05 | `StrategicBriefing` validiert mit gültigen Werten | Pydantic-Validierung erfolgreich |
| STRAT-CTR-06 | `StrategicBriefing.generated_by` ist nicht `"KANZLER"` | Validierungsfehler |
| STRAT-CTR-07 | `StrategicDirective` mit gültigem `intent` und `parameters` | Pydantic-Validierung erfolgreich |
| STRAT-CTR-08 | `StrategicDirective` mit `intent=UNLOCK_BUDGET` aber `parameters` vom Typ `NoActionParams` | Validierungsfehler (Discriminator-Mismatch) |
| STRAT-CTR-09 | `DirectiveParameters` discriminierte Union: alle 14 Intents validieren | Alle Submodelle validieren |
| STRAT-CTR-10 | `ResearchManifest` mit `created_by` ≠ Mensch | Validierungsfehler |
| STRAT-CTR-11 | `ResearchManifest` mit `approved_by` ≠ Mensch | Validierungsfehler |
| STRAT-CTR-12 | `HumanResponseFile` mit `answered_by` ≠ Mensch | Validierungsfehler |
| STRAT-CTR-13 | `HumanDirective` mit `created_by` ≠ Mensch | Validierungsfehler |
| STRAT-CTR-14 | `StrategicLayerConfig` mit gültigen Defaults | Pydantic-Validierung erfolgreich |
| STRAT-CTR-15 | `StrategicLayerConfig` mit `briefing_interval_cycles = 0` | Validierungsfehler |
| STRAT-CTR-16 | `SymptomEvent` mit gültigem `symptom_type` | Pydantic-Validierung erfolgreich |
| STRAT-CTR-17 | `ScientificHypothesis` mit leerem `hypothesis_text` | Validierungsfehler |
| STRAT-CTR-18 | `DimensionOnboardingRequest` mit `requires_physical_actuation=true` | Pydantic-Validierung erfolgreich |
| STRAT-CTR-19 | `CapabilityGapSignal` mit gültigen Werten | Pydantic-Validierung erfolgreich |
| STRAT-CTR-20 | `FinalScientificReport` mit `human_reviewed=false` | Pydantic-Validierung erfolgreich |

#### §4.7.3 STRAT-AX — Achsen & ControlState Tests (~40 Tests)
<!-- @table schema="test_suite_STRAT_AX" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRAT-AX-01 | ControlState-Tupel `(NORMAL, FUNDED, EXPLORATION, AUTONOMOUS)` ist gültig | Gültig |
| STRAT-AX-02 | ControlState-Tupel `(ESTOP_LOCKED, INCUBATING, EXPLORATION, AUTONOMOUS)` ist ungültig | Ungültig (§30.2) |
| STRAT-AX-03 | ControlState-Tupel `(SAFE_MODE, FUNDED, BOOTSTRAP, AUTONOMOUS)` ist ungültig | Ungültig (§30.2) |
| STRAT-AX-04 | ControlState-Tupel `(NORMAL, BUDGET_EXHAUSTED, EXPLORATION, AUTONOMOUS)` ist ungültig | Ungültig (§30.2) |
| STRAT-AX-05 | CT-1: `resource → BUDGET_EXHAUSTED` erzwingt `governance → AWAITING_HUMAN` | Closure feuert |
| STRAT-AX-06 | CT-2: `safety → ESTOP_LOCKED` + `resource=INCUBATING` → resource verlässt INCUBATING | Closure feuert |
| STRAT-AX-07 | CT-3: `safety → SAFE_MODE` unterdrückt pending ResearchAxis-Transitionen | ResearchAxis-Transition verworfen |
| STRAT-AX-08 | CT-4: `DimensionOnboardingRequest.status → ESCALATED` + `requires_physical_actuation=true` → `governance → AWAITING_HUMAN` | Closure feuert |
| STRAT-AX-09 | CT-5: `resource → PHYSICAL_WAIT` → `governance → AWAITING_HUMAN` | Closure feuert |
| STRAT-AX-10 | CT-6: `safety → SAFE_MODE` → `governance → AWAITING_HUMAN` | Closure feuert |
| STRAT-AX-11 | CT-6: `safety → ESTOP_LOCKED` → `governance → AWAITING_HUMAN` | Closure feuert |
| STRAT-AX-12 | CT-7: `resource: BUDGET_EXHAUSTED → FUNDED` via UNLOCK_BUDGET → `governance → AUTONOMOUS` | Closure feuert |
| STRAT-AX-13 | CT-8: `resource: PHYSICAL_WAIT → FUNDED` via CAPEX-Freigabe + Capability in Registry → `governance → AUTONOMOUS` | Closure feuert |
| STRAT-AX-14 | CT-8: `resource: PHYSICAL_WAIT → FUNDED` via CAPEX-Freigabe aber Capability NICHT in Registry → Closure feuert NICHT | Closure feuert nicht |
| STRAT-AX-15 | CT-9: `safety: SAFE_MODE → NORMAL` via SL-SAF-7 → `governance → AUTONOMOUS` | Closure feuert |
| STRAT-AX-16 | CT-10: `safety: ESTOP_LOCKED → NORMAL` via autorisierten Sicherheitsprozess → `governance → AUTONOMOUS` | Closure feuert |
| STRAT-AX-17 | SL-CT-SIMULTAN: CT-1 und CT-6 feuern gleichzeitig → nur EINE governance-Transition | Eine Transition |
| STRAT-AX-18 | SL-CT-SIMULTAN: CT-5 und CT-6 feuern gleichzeitig → nur EINE governance-Transition | Eine Transition |
| STRAT-AX-19 | SL-AX-ATOMIC: Zwei simultane Achsen-Transitionen werden atomar committet | Atomarer Commit |
| STRAT-AX-20 | SL-AX-ATOMIC: Ungültiger Ziel-Tupel nach Closure → gesamte Transition VERWORFEN | Fail-Closed |
| STRAT-AX-21 | SL-AX-ATOMIC: `batch_id` ist für alle Transitionen eines Commits identisch | Gleiche batch_id |
| STRAT-AX-22 | SL-AX-ATOMIC: Einzel-Transition hat `batch_id = transition_id` | Selbstreferenz |
| STRAT-AX-23 | Severity-Ordnung: SAFETY > RESOURCE bei gleichzeitigem Konflikt | SAFETY gewinnt |
| STRAT-AX-24 | Severity-Ordnung: RESOURCE > GOVERNANCE bei gleichzeitigem Konflikt | RESOURCE gewinnt |
| STRAT-AX-25 | Severity-Ordnung: GOVERNANCE > RESEARCH bei gleichzeitigem Konflikt | GOVERNANCE gewinnt |
| STRAT-AX-26 | ResearchAxis hat keinen Severity-Begriff → Audit + Eskalation bei Konflikt | Eskalation |
| STRAT-AX-27 | SR-A: `safety ∈ {SAFE_MODE, ESTOP_LOCKED}` → alle pending ResearchAxis-Transitionen verworfen | Verworfen |
| STRAT-AX-28 | Liveness-Watchdog: `(now − letzter Strategie-Zyklus) > liveness_watchdog_hours` → Heartbeat-Zyklus | Heartbeat |
| STRAT-AX-29 | `compute_phase_label()` erzeugt korrektes Etikett | z.B. `"EXPLOITATION + PHYSICAL_WAIT"` |
| STRAT-AX-30 | `compute_phase_label()` ist nicht authoritativ | Nicht authoritativ |
| STRAT-AX-31 | Parameter-Besitz-Matrix: ResearchAxis setzt `exploration_weight` | Erlaubt |
| STRAT-AX-32 | Parameter-Besitz-Matrix: ResourceAxis versucht `exploration_weight` zu setzen | SL-DEP-Lint Build-Fail |
| STRAT-AX-33 | Parameter-Besitz-Matrix: GovernanceAxis setzt `stall_detection_active` | Erlaubt |
| STRAT-AX-34 | Parameter-Besitz-Matrix: SafetyAxis setzt `safety_dispatch_allowed` | Erlaubt |
| STRAT-AX-35 | Closure-Iteration: `closure_max_iterations=5` wird nicht überschritten | Max 5 Iterationen |
| STRAT-AX-36 | Closure-Fixpunkt: Nach 2 Iterationen ist Fixpunkt erreicht | Fixpunkt |
| STRAT-AX-37 | ESTOP + Budget-Schwelle simultan: Gearbeitetes Beispiel aus §34.4 | Korrekter Ziel-Tupel |
| STRAT-AX-38 | `ControlStateLog` wird korrekt aktualisiert | `current_state` authoritativ |
| STRAT-AX-39 | Achsen-Transition wird im `ControlStateLog` protokolliert | Protokolliert |
| STRAT-AX-40 | Achsen-Transition mit `triggered_by=HAL` bei ESTOP | `triggered_by=HAL` |

#### §4.7.4 STRAT-KANZ — Kanzler & DTT Tests (~55 Tests)
<!-- @table schema="test_suite_STRAT_KANZ" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRAT-KANZ-01 | Validierungspipeline Stufe 1: Schema-Validierung erfolgreich | Weiter zu Stufe 2 |
| STRAT-KANZ-02 | Validierungspipeline Stufe 1: Schema-Validierung fehlgeschlagen | VETO(`"SCHEMA_INVALID"`) |
| STRAT-KANZ-03 | Validierungspipeline Stufe 2: `briefing_ref` existiert | Weiter zu Stufe 3 |
| STRAT-KANZ-04 | Validierungspipeline Stufe 2: `briefing_ref` existiert nicht | VETO(`"REF_NOT_FOUND"`) |
| STRAT-KANZ-05 | Validierungspipeline Stufe 3: Manifest-Prüfung erfolgreich | Weiter zu Stufe 3b |
| STRAT-KANZ-06 | Validierungspipeline Stufe 3: Manifest-Prüfung fehlgeschlagen | VETO(`"MANIFEST_VIOLATION"`) |
| STRAT-KANZ-07 | Validierungspipeline Stufe 3b: Weisungs-Prüfung erfolgreich | Weiter zu Stufe 3c |
| STRAT-KANZ-08 | Validierungspipeline Stufe 3b: Weisungs-Prüfung fehlgeschlagen | VETO(`"HUMAN_DIRECTIVE_VIOLATION"`) |
| STRAT-KANZ-09 | Validierungspipeline Stufe 3c: Target-Existenz erfolgreich | Weiter zu Stufe 4 |
| STRAT-KANZ-10 | Validierungspipeline Stufe 3c: Target ist LOCKED | VETO(`"TARGET_LOCKED"`) |
| STRAT-KANZ-11 | Validierungspipeline Stufe 4: Safety-/Injection-Prüfung erfolgreich | Weiter zu Stufe 5 |
| STRAT-KANZ-12 | Validierungspipeline Stufe 4: Injection erkannt | VETO + Audit |
| STRAT-KANZ-13 | Validierungspipeline Stufe 5: Budget-Prüfung erfolgreich | Weiter zu Stufe 6 |
| STRAT-KANZ-14 | Validierungspipeline Stufe 5: Budget negativ | VETO(`"BUDGET_NEGATIVE"`) |
| STRAT-KANZ-15 | Validierungspipeline Stufe 6b: Mode-Prüfung via ControlState erfolgreich | Weiter zu Stufe 6c |
| STRAT-KANZ-16 | Validierungspipeline Stufe 6b: Mode-Prüfung fehlgeschlagen | VETO(`"MODE_VIOLATION"`) |
| STRAT-KANZ-17 | Validierungspipeline Stufe 6c: Semantische Dedup erfolgreich | Weiter zu Stufe 7 |
| STRAT-KANZ-18 | Validierungspipeline Stufe 6c: Semantisches Duplikat erkannt | VETO(`"DUPLICATE_SEMANTIC"`) |
| STRAT-KANZ-19 | Validierungspipeline Stufe 7: Konflikt-Modus-Prüfung erfolgreich | ACCEPT |
| STRAT-KANZ-20 | Validierungspipeline Stufe 7: Konflikt-Modus aktiv | VETO(`"CONFLICT_MODE"`) |
| STRAT-KANZ-21 | DTT: NO_ACTION → keine Policy-Änderung | Zyklus protokolliert |
| STRAT-KANZ-22 | DTT: INITIAL_SWEEP → Topic PROPOSED→ACTIVE | Topic aktiviert |
| STRAT-KANZ-23 | DTT: PIVOT_DOMAIN → Scope-Check + Feasibility + Loop-Erkennung | Altes Topic ARCHIVED |
| STRAT-KANZ-24 | DTT: UNLOCK_BUDGET → immer Eskalation(BUDGET) | Eskalation erstellt |
| STRAT-KANZ-25 | DTT: ABORT_MISSION → immer ESCALATED | Eskalation erstellt |
| STRAT-KANZ-26 | DTT: HUMAN_ESCALATION(CAPEX) → `resource → PHYSICAL_WAIT` + `governance → AWAITING_HUMAN` | CT-5 + CT-6 feuern |
| STRAT-KANZ-27 | DTT: SET_RESEARCH_PHASE → löst ResearchAxis-Wechsel aus | Achsen-Transition |
| STRAT-KANZ-28 | DTT: INCREASE_DIAGNOSTIC → `diagnostic_budget += amount` | Budget erhöht |
| STRAT-KANZ-29 | DTT: CALIBRATE_TWIN bei nicht gedriftetem Twin | VETO(`"NO_DRIFT"`) |
| STRAT-KANZ-30 | Intent-Verfügbarkeit: UNLOCK_BUDGET bei `resource=FUNDED` | VETO(`"MODE_VIOLATION"`) |
| STRAT-KANZ-31 | Intent-Verfügbarkeit: UNLOCK_BUDGET bei `resource=BUDGET_EXHAUSTED` | Intent verfügbar |
| STRAT-KANZ-32 | Intent-Verfügbarkeit: SET_RESEARCH_PHASE bei `resource=BUDGET_EXHAUSTED` | Blockiert |
| STRAT-KANZ-33 | Intent-Verfügbarkeit: SET_RESEARCH_PHASE bei `resource=PHYSICAL_WAIT` | Blockiert |
| STRAT-KANZ-34 | Intent-Verfügbarkeit: SET_RESEARCH_PHASE bei `resource=FUNDED` | Verfügbar |
| STRAT-KANZ-35 | Intent-Verfügbarkeit: INCREASE_DIAGNOSTIC bei `safety=SAFE_MODE` ohne Quarantäne | Blockiert |
| STRAT-KANZ-36 | Intent-Verfügbarkeit: INCREASE_DIAGNOSTIC bei `safety=SAFE_MODE` mit Quarantäne-Zone | Erlaubt (BF-15) |
| STRAT-KANZ-37 | Intent-Verfügbarkeit: INCREASE_DIAGNOSTIC bei `safety=SAFE_MODE` mit Quarantäne aber `amount > diagnostic_budget_default` | Blockiert |
| STRAT-KANZ-38 | Intent-Verfügbarkeit: Alle Intents bei `safety=ESTOP_LOCKED` außer NO_ACTION und HUMAN_ESCALATION | Blockiert |
| STRAT-KANZ-39 | Konfliktdetektor: GOVERNANCE-VETO zählt als Konflikt | Konflikt gezählt |
| STRAT-KANZ-40 | Konfliktdetektor: BENIGN-VETO zählt nicht als Konflikt | Kein Konflikt |
| STRAT-KANZ-41 | Konfliktdetektor: 2 Konflikte in `conflict_window_cycles` → URGENT + DEADLOCK-Eskalation | Eskalation |
| STRAT-KANZ-42 | Konfliktdetektor: Konflikt-Modus → nur NO_ACTION/HUMAN_ESCALATION angenommen | Andere → VETO |
| STRAT-KANZ-43 | NO_ACTION-Stall: `no_action_stall_limit` aufeinanderfolgende NO_ACTION → URGENT | URGENT |
| STRAT-KANZ-44 | NO_ACTION-Stall: `stall_detection_active=false` → Stall-Counter wird NICHT erhöht | Kein URGENT |
| STRAT-KANZ-45 | NO_ACTION-Stall: Während AWAITING_HUMAN → Stall-Überwachung suspendiert | Kein URGENT |
| STRAT-KANZ-46 | SL-SAF-7: SAFE_MODE → NORMAL nur via `HumanResponseFile.unlock_decision` mit `scope_refs=["GLOBAL_SAFETY"]` | Übergang |
| STRAT-KANZ-47 | SL-SAF-7: SAFE_MODE → NORMAL ohne `scope_refs=["GLOBAL_SAFETY"]` | Kein Übergang |
| STRAT-KANZ-48 | SL-BUD-1: `used_cycles += 1 × resource.burn_rate_multiplier` | Budget brennt |
| STRAT-KANZ-49 | SL-BUD-1: `burn_rate_multiplier=0` in PHYSICAL_WAIT | Budget brennt nicht |
| STRAT-KANZ-50 | SL-BUD-1: `burn_rate_multiplier=0` in BUDGET_EXHAUSTED | Budget brennt nicht |
| STRAT-KANZ-51 | SL-BUD-1a: Laufende Questor-Pakete bei BUDGET_EXHAUSTED → nicht beeinflusst | Paket läuft weiter |
| STRAT-KANZ-52 | SL-URG-2: `remaining_cycles ≤ budget_unlock_threshold_fraction` → URGENT + Eskalation(BUDGET) | Eskalation |
| STRAT-KANZ-53 | SL-BRF-9: `provisional=true` bei trunkiertem Briefing | `royal_log_entry.provisional=true` |
| STRAT-KANZ-54 | SL-BRF-9: `provisional=false` bei nicht trunkiertem Briefing | `royal_log_entry.provisional=false` |
| STRAT-KANZ-55 | Semantische Dedup: `semantic_directive_id = sha256(intent + target_ref + canonical_json(parameters))` | Deterministisch |

#### §4.7.5 STRAT-KOEN — Königin & Briefing Tests (~25 Tests)
<!-- @table schema="test_suite_STRAT_KOEN" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRAT-KOEN-01 | Constitutional Anchor: Königin erhält exakt 3 Kontextblöcke | 3 Blöcke |
| STRAT-KOEN-02 | Constitutional Anchor: CONSTITUTIONAL MEMORY enthält mission_goal, hard_constraints, soft_preferences | Vorhanden |
| STRAT-KOEN-03 | Constitutional Anchor: STATELESS BRIEFING enthält keinen `security_mode` | Nicht vorhanden |
| STRAT-KOEN-04 | Constitutional Anchor: STATELESS BRIEFING enthält keine Hybrid-Referenzen | Nicht vorhanden |
| STRAT-KOEN-05 | Constitutional Anchor: STATELESS BRIEFING enthält keinen Roh-metric_vector | Nicht vorhanden |
| STRAT-KOEN-06 | Constitutional Anchor: ANCHOR enthält aktive HUMAN_OVERRIDE-Einträge zuerst | HUMAN_OVERRIDE zuerst |
| STRAT-KOEN-07 | Constitutional Anchor: ANCHOR enthält letzte `royal_log_anchor_depth=3` Direktiven | 3 Direktiven |
| STRAT-KOEN-08 | Constitutional Anchor: Kein persistenter Gesprächsverlauf | Stateless |
| STRAT-KOEN-09 | Constitutional Anchor: Menschliche Weisungen überschreiben Königin-Direktiven | Mensch gewinnt |
| STRAT-KOEN-10 | Constitutional Anchor: LLM-Fehler → Policy bleibt unverändert | Policy unverändert |
| STRAT-KOEN-11 | Constitutional Anchor: Nach `max_consecutive_llm_failures` → Eskalation | Eskalation |
| STRAT-KOEN-12 | Briefing-Erzeugung: `briefing_id` ist die einzige Zyklen-ID | Keine `zyklus_id` |
| STRAT-KOEN-13 | Briefing-Erzeugung: `generated_by` ist immer `"KANZLER"` | KANZLER |
| STRAT-KOEN-14 | Briefing-Erzeugung: Trunkierungspriorität v2 wird angewendet | Korrekte Priorität |
| STRAT-KOEN-15 | Briefing-Erzeugung: Twins mit `calibration_required` fallen nie in Restklasse | Nie Restklasse |
| STRAT-KOEN-16 | Briefing-Erzeugung: Quarantäne → `[REDACTED:QUARANTINE]` | Redacted |
| STRAT-KOEN-17 | Briefing-Erzeugung: Gesamt-Kontext-Budget wird eingehalten | `max_total_context_chars` |
| STRAT-KOEN-18 | Briefing-Erzeugung: Layer 3 (Anchor) wird nie trunkiert | Nie trunkiert |
| STRAT-KOEN-19 | Briefing-Erzeugung: `active_hypothesis_refs` (Top-N) vorhanden | Vorhanden |
| STRAT-KOEN-20 | Briefing-Erzeugung: `in_flight_packages` vorhanden | Vorhanden |
| STRAT-KOEN-21 | Briefing-Typ: BOOTSTRAP bei Mission-Start | BOOTSTRAP |
| STRAT-KOEN-22 | Briefing-Typ: PERIODIC im Normalbetrieb | PERIODIC |
| STRAT-KOEN-23 | Briefing-Typ: URGENT bei SL-URG-1 Trigger | URGENT |
| STRAT-KOEN-24 | Briefing-Typ: FINAL bei Topic-SATURATION | FINAL |
| STRAT-KOEN-25 | SL-URG-3: URGENT-Nachzügler während Cooldown → ins nächste PERIODIC gemerged | Gemerged |

#### §4.7.6 STRAT-SYM — Symptom-Trigger & Signal Tests (~15 Tests)
<!-- @table schema="test_suite_STRAT_SYM" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRAT-SYM-01 | SymptomEvent(INITIAL_SWEEP) bei Bootstrap | SymptomEvent erzeugt |
| STRAT-SYM-02 | SymptomEvent(WEISSRAUM) bei Zone gemäß SL-DEF-2 | SymptomEvent erzeugt |
| STRAT-SYM-03 | SymptomEvent(FRACTURE_GAP) bei `fracture_score ≥ quarantine_threshold` | SymptomEvent erzeugt |
| STRAT-SYM-04 | SymptomEvent(SATURATION) bei Topic-StopCondition SATURATION_CYCLES | SymptomEvent erzeugt |
| STRAT-SYM-05 | SymptomEvent(TWIN_DRIFT) bei `tolerance_breached=true` | SymptomEvent erzeugt |
| STRAT-SYM-06 | SymptomEvent(CAPABILITY_GAP_FEEDBACK) bei CapabilityGapSignal | SymptomEvent erzeugt |
| STRAT-SYM-07 | SymptomEvent(DIMENSION_GAP) bei blockierter approved=false-Dimension | SymptomEvent erzeugt |
| STRAT-SYM-08 | SymptomEvent(REPLICATE_DIVERGENCE) bei SL-SIG-5 | SymptomEvent erzeugt |
| STRAT-SYM-09 | SymptomEvent(QUARANTINE_BLOCK) bei blockierter Idee in quarantinierter Zone | SymptomEvent erzeugt |
| STRAT-SYM-10 | SL-SIG-7a: Overfitting (`train_val_gap > threshold`) → ⬜ CONSTRAINT_NEAR_MISS | Kein 🟨 |
| STRAT-SYM-11 | SL-SIG-7a: Overfitting wiederholt (≥ `min_confirmations` in `conflict_window_cycles`) → MetricConstraint-Fracture | Fracture |
| STRAT-SYM-12 | SL-SIG-7a: `"Parameter-äquivalent"` mit Float-Toleranz (`metric_tolerance_multiplier`) | Toleranz angewendet |
| STRAT-SYM-13 | SL-SIG-1: `confirms_expectation=False` → 🟨 CONTRADICTION | 🟨 |
| STRAT-SYM-14 | SL-SIG-1: `confirms_expectation=True` + `konfidenz ≥ 0.8` → 🟩 | 🟩 |
| STRAT-SYM-15 | SL-SIG-1: `confirms_expectation=None` → ⬜ EXPLORATORY_COVERAGE | ⬜ |

#### §4.7.7 STRAT-E2E — End-to-End Tests (~15 Tests)
<!-- @table schema="test_suite_STRAT_E2E" -->
| Test-ID | Test | Erwartet |
|---------|------|----------|
| STRAT-E2E-01 | Vollständiger Zyklus: Briefing → Directive → Validierung → DTT → Policy-Wirkung | Zyklus abgeschlossen |
| STRAT-E2E-02 | Missions-Bootstrap: Manifest → BOOTSTRAP-Briefing → INITIAL_SWEEP → Topic ACTIVE | Bootstrap erfolgreich |
| STRAT-E2E-03 | Missions-Bootstrap: Manifest-Intake fail-closed bei ungültigem Manifest | REJECT |
| STRAT-E2E-04 | Missions-Bootstrap: Nach `bootstrap_retry_limit=3` invaliden INITIAL_SWEEP → TEMPLATE_GAP-Eskalation | Eskalation |
| STRAT-E2E-05 | CAPEX-Flow: CapabilityGapSignal → CAPEX-Eskalation → PHYSICAL_WAIT → AWAITING_HUMAN → Mensch genehmigt → Capability in Registry → FUNDED → AUTONOMOUS | Vollständiger Flow |
| STRAT-E2E-06 | SAFE_MODE-Flow: SafetyConstraint → SAFE_MODE → AWAITING_HUMAN → Diagnose → SL-SAF-7 → NORMAL → AUTONOMOUS | Vollständiger Flow |
| STRAT-E2E-07 | ESTOP-Flow: HAL ESTOP → ESTOP_LOCKED → AWAITING_HUMAN → Sicherheitsprozess → NORMAL → AUTONOMOUS | Vollständiger Flow |
| STRAT-E2E-08 | BUDGET_EXHAUSTED-Flow: Budget-Schwelle → BUDGET_EXHAUSTED → AWAITING_HUMAN → UNLOCK_BUDGET → FUNDED → AUTONOMOUS | Vollständiger Flow |
| STRAT-E2E-09 | Quarantäne-Diagnostik-Flow: Fracture → Quarantäne → SAFE_MODE → INCREASE_DIAGNOSTIC (BF-15) → Diagnose → Exit | Vollständiger Flow |
| STRAT-E2E-10 | Overfitting-Flow: CONSTRAINT_NEAR_MISS → wiederholt → MetricConstraint-Fracture → Vordenker erhält Symptom | Vollständiger Flow |
| STRAT-E2E-11 | Simultane Multi-Achsen-Transition: ESTOP + Budget-Schwelle + SATURATION gleichzeitig | SL-AX-ATOMIC korrekt |
| STRAT-E2E-12 | Dimensions-Eskalation-Flow: Vordenker schlägt Dimension vor → CT-4 → AWAITING_HUMAN → Mensch genehmigt → AUTONOMOUS | Vollständiger Flow |
| STRAT-E2E-13 | Topic-Archivierung-Flow: StopCondition REACHED → SATURATED → FINAL-Briefing → ReportFacts → FinalScientificReport → ARCHIVED | Vollständiger Flow |
| STRAT-E2E-14 | HumanDirective-Override: Mensch sendet HumanDirective → Königin-Direktive wird überschrieben | Mensch gewinnt |
| STRAT-E2E-15 | SymptomEvent-Verlustschutz: SymptomEvent vor Queue-Übergabe persistent → At-Least-Once | Nicht verloren |

<!-- @section id="5" title="Testdaten und Fixtures" type="prose" -->
## §5 Testdaten und Fixtures

<!-- @section id="5.1" title="Test-Fixture-Struktur" type="prose" -->
### §5.1 Test-Fixture-Struktur

```
tests/
    └── test_questor/
        ├── fixtures/
        │   ├── envelopes/
        │   │   ├── valid_envelope.json
        │   │   ├── invalid_envelope_no_gate.json
        │   │   ├── invalid_envelope_no_lease.json
        │   │   └── envelope_with_injection.json
        │   ├── templates/
        │   │   ├── chemie_optimize_v1.yaml
        │   │   ├── biologie_incubation_v1.yaml
        │   │   ├── ml_training_v1.yaml
        │   │   └── recovery_reconcile_v1.yaml
        │   ├── capabilities/
        │   │   ├── pipette.transfer.yaml
        │   │   ├── spectrometer.measure_absorbance.yaml
        │   │   └── gpu.train.yaml
        │   ├── hal_manifests/
        │   │   ├── normal_manifest.json
        │   │   ├── sandbox_manifest.json
        │   │   └── recovery_manifest.json
        │   ├── wal/
        │   │   ├── valid_wal/
        │   │   ├── corrupt_wal/
        │   │   └── empty_wal/
        │   └── results/
        │       ├── successful_result.json
        │       ├── operational_abort_result.json
        │       ├── scientific_abort_result.json
        │       └── safety_abort_result.json
        ├── mocks/
        │   ├── mock_hal.py
        │   ├── mock_llm.py
        │   ├── mock_resource_governor.py
        │   └── mock_filesystem.py
        └── conftest.py
    └── test_atlas/
        ├── fixtures/
        │   ├── evidence_events/
        │   ├── atlas_nodes/
        │   ├── atlas_edges/
        │   ├── zone_geometries/
        │   ├── safety_constraints/
        │   ├── frontier_candidates/
        │   └── diagnostic_resolutions/
        ├── mocks/
        │   └── mock_cartographer.py
        └── conftest.py
    └── test_strategy/
        ├── fixtures/
        │   ├── control_states/
        │   │   ├── normal_funded_exploration_autonomous.json
        │   │   ├── estop_locked_budget_exhausted.json
        │   │   ├── safe_mode_awaiting_human.json
        │   │   └── physical_wait_awaiting_human.json
        │   ├── briefings/
        │   │   ├── bootstrap_briefing.json
        │   │   ├── periodic_briefing.json
        │   │   ├── urgent_briefing.json
        │   │   └── final_briefing.json
        │   ├── directives/
        │   │   ├── initial_sweep_directive.json
        │   │   ├── unlock_budget_directive.json
        │   │   ├── pivot_domain_directive.json
        │   │   └── no_action_directive.json
        │   ├── manifests/
        │   │   ├── valid_manifest.json
        │   │   └── invalid_manifest.json
        │   ├── human_responses/
        │   │   ├── unlock_budget_response.json
        │   │   ├── capex_approval_response.json
        │   │   └── safety_unlock_response.json
        │   └── symptom_events/
        │       ├── initial_sweep_event.json
        │       ├── fracture_gap_event.json
        │       ├── twin_drift_event.json
        │       └── capability_gap_event.json
        ├── mocks/
        │   ├── mock_kanzler.py
        │   ├── mock_koenigin_llm.py
        │   ├── mock_control_state_manager.py
        │   └── mock_atlas.py
        └── conftest.py
```

<!-- @section id="5.2" title="Mock-Strategie" type="prose" -->
### §5.2 Mock-Strategie

<!-- @table schema="mock_strategy" -->
| Mock | Zweck |
|------|-------|
| mock_hal.py | Simuliert HAL-Antworten (SUCCESS, DENIED, ESTOP, etc.) |
| mock_llm.py | Simuliert LLM-Antworten (JSON, Timeout, Injection) |
| mock_resource_governor.py | Simuliert Lease-Vergabe und -Ablehnung |
| mock_filesystem.py | Simuliert Disk-Full, Permission-Error, etc. |
| mock_cartographer.py | Simuliert Kartograph-Operationen für Atlas-Tests |
| mock_kanzler.py | Simuliert Kanzler-Operationen für Strategic-Layer-Tests |
| mock_koenigin_llm.py | Simuliert Königin-LLM-Antworten (stateless) |
| mock_control_state_manager.py | Simuliert ControlState-Verwaltung und Achsen-Transitionen |
| mock_atlas.py | Simuliert Atlas-Zustände für Strategic-Layer-Tests |

<!-- @section id="5.3" title="Testdaten-Regeln" type="prose" -->
### §5.3 Testdaten-Regeln

<!-- @table schema="test_data_rules" -->
| Regel | Beschreibung |
|-------|-------------|
| TD-1 | Testdaten sind deterministisch. Keine Zufälligkeit. |
| TD-2 | Testdaten enthalten keine echten Forschungsdaten. |
| TD-3 | Testdaten enthalten keine echten Gate-Records. |
| TD-4 | Testdaten enthalten keine echten Lease-Tokens. |
| TD-5 | Testdaten sind in `tests/test_questor/fixtures/`, `tests/test_atlas/fixtures/` und `tests/test_strategy/fixtures/` gespeichert. |
| TD-6 | Testdaten sind versioniert (git). |
| TD-7 | Strategic-Layer-Fixtures enthalten keine echten Manifest-Daten. |
| TD-8 | ControlState-Fixtures decken alle gültigen und ungültigen Achsen-Kombinationen ab. |

<!-- @section id="6" title="Coverage-Ziele" type="prose" -->
## §6 Coverage-Ziele

<!-- @section id="6.1" title="Mindestabdeckung pro Modul" type="prose" -->
### §6.1 Mindestabdeckung pro Modul

<!-- @table schema="coverage_targets" -->
| Modul | Mindestabdeckung | Begründung |
|-------|-----------------|-----------|
| sanitization.py | 95% | Sicherheitskritisch |
| capability_registry.py | 90% | Sicherheitskritisch |
| security_mode.py | 95% | Sicherheitskritisch |
| policy_evaluator.py | 95% | Sicherheitskritisch |
| safety_monitor.py | 95% | Sicherheitskritisch |
| shutdown.py | 90% | Crash-Sicherheit |
| health_monitor.py | 85% | Betriebssicherheit |
| hal_bridge.py | 90% | Hardware-Zugriff |
| result_builder.py | 90% | Ergebnis-Integrität |
| ledger.py | 90% | Datenintegrität |
| recovery.py | 90% | Crash-Recovery |
| compass.py | 85% | Kernlogik |
| trail_map.py | 80% | Operational |
| queue_integration.py | 85% | Betriebskritisch |
| facade.py | 85% | Eintrittspunkt |
| validator.py | 90% | Eintrittspunkt |
| atlas_core.py | 90% | Atlas-Hybrid-Kern |
| frontier_engine.py | 85% | Frontier-Logik |
| diagnostic_resolution.py | 90% | Diagnostik-Logik |
| safety_constraint.py | 95% | Sicherheitskritisch |
| control_state_manager.py | 95% | Achsen-Steuerung |
| directive_translation_table.py | 90% | DTT-Logik |
| briefing_generator.py | 85% | Briefing-Erzeugung |
| konfliktdetektor.py | 90% | Konflikt-Erkennung |
| Gesamt | ≥ 88% | |

<!-- @section id="6.2" title="Coverage-Regeln" type="prose" -->
### §6.2 Coverage-Regeln

<!-- @table schema="coverage_rules" -->
| Regel | Beschreibung |
|-------|-------------|
| COV-1 | Sicherheitskritische Module haben ≥ 95% Abdeckung. |
| COV-2 | Kernlogik hat ≥ 85% Abdeckung. |
| COV-3 | Jeder Fail-Closed-Punkt muss getestet sein. |
| COV-4 | Jeder Edge Case muss getestet sein. |
| COV-5 | Jede Fehlerbehandlung muss getestet sein. |
| COV-6 | Jeder Zustandsübergang muss getestet sein. |
| COV-7 | Jede Closure-Regel (CT-1..CT-10) muss getestet sein. |
| COV-8 | Jede Intent-Verfügbarkeitsregel muss getestet sein. |

<!-- @section id="7" title="Test-Infrastruktur" type="prose" -->
## §7 Test-Infrastruktur

<!-- @section id="7.1" title="Framework" type="prose" -->
### §7.1 Framework

<!-- @table schema="test_framework" -->
| Tool | Zweck |
|------|-------|
| pytest | Test-Framework |
| pytest-cov | Code-Coverage |
| pytest-asyncio | Async-Tests (falls nötig) |
| pytest-timeout | Timeout für Tests |
| pytest-mock | Mocking |
| hypothesis | Property-based Testing (optional) |

<!-- @section id="7.2" title="Test-Konfiguration" type="prose" -->
### §7.2 Test-Konfiguration

```python
# pytest.ini
[pytest]
testpaths = tests/test_questor tests/test_atlas tests/test_strategy
addopts = --cov=src/questor --cov=src/gremium --cov=src/strategy --cov-report=html --cov-report=term-missing
timeout = 60
markers =
    unit: Unit-Tests
    component: Komponententests
    integration: Integrationstests
    security: Sicherheitstests
    performance: Performance-Tests
    stress: Stress-Tests
    atlas: Atlas-Hybrid-Tests
    strat: Strategic-Layer-Tests
    slow: Langsame Tests (> 10s)
```

<!-- @section id="7.3" title="Continuous Integration" type="prose" -->
### §7.3 Continuous Integration

```yaml
# .github/workflows/questor-tests.yml
name: Questor Tests
on: [push, pull_request]
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/test_questor -m unit --cov=src/questor
  component-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/test_questor -m component
  security-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/test_questor -m security
  atlas-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/test_atlas -m atlas --cov=src/gremium
  strategy-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/test_strategy -m strat --cov=src/strategy
  performance-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/test_questor -m performance --timeout=300
```

<!-- @section id="8" title="Test-Ausführungsstrategie" type="prose" -->
## §8 Test-Ausführungsstrategie

<!-- @section id="8.1" title="Ausführungsreihenfolge" type="prose" -->
### §8.1 Ausführungsreihenfolge

```
PHASE 1: Unit-Tests (schnell, ~2 Minuten)
   → pytest -m unit

PHASE 2: Komponententests (~5 Minuten)
   → pytest -m component

PHASE 3: Sicherheitstests (~3 Minuten)
   → pytest -m security

PHASE 4: Atlas-Hybrid-Tests (~8 Minuten)
   → pytest -m atlas

PHASE 4b: Strategic-Layer-Tests (~12 Minuten)
   → pytest -m strat

PHASE 5: Integrationstests (Suite I, ~10 Minuten)
   → pytest -m integration

PHASE 6: Szenario-Tests (Suite S, ~15 Minuten)
   → pytest -m scenario

PHASE 7: Performance/Stress-Tests (~10 Minuten)
   → pytest -m "performance or stress" --timeout=300

PHASE 8: Vollständige Suite (~67 Minuten)
   → pytest --cov=src/questor --cov=src/gremium --cov=src/strategy
```

<!-- @section id="8.2" title="Test-Gates" type="prose" -->
### §8.2 Test-Gates

<!-- @table schema="test_gates" -->
| Gate | Bedingung |
|------|-----------|
| GATE-1 | Alle Unit-Tests bestehen |
| GATE-2 | Alle Komponententests bestehen |
| GATE-3 | Alle Sicherheitstests bestehen |
| GATE-4 | Coverage ≥ 88% |
| GATE-5 | Alle Integrationstests bestehen (Suite I) |
| GATE-6 | Alle Szenario-Tests bestehen (Suite S) |
| GATE-7 | Performance-Tests innerhalb der Limits |
| GATE-8 | Keine offenen Blocker |
| GATE-ATLAS | Alle Atlas-Hybrid-Tests bestehen (Suite ATLAS) |
| GATE-STRAT | Alle Strategic-Layer-Tests bestehen (Suite STRAT) |

<!-- @section id="9" title="Akzeptanzkriterien für das Gesamtsystem" type="prose" -->
## §9 Akzeptanzkriterien für das Gesamtsystem

Das Gesamtsystem gilt als integriert, wenn:

<!-- @table schema="acceptance_criteria" -->
| # | Kriterium | CHARTER-Referenz |
|---|-----------|-----------------|
| 1 | Alle Naming-Tests bestehen | — |
| 2 | Alle Integrationstests bestehen | — |
| 3 | Alle Szenario-Tests bestehen | — |
| 4 | Alle Regressions-Tests bestehen | — |
| 5 | Alle Präzisierungs-Tests bestehen | — |
| 6 | Alle HAL-Tests bestehen | — |
| 7 | Alle Questor-Unit-Tests bestehen | — |
| 8 | Alle Questor-Komponententests bestehen | — |
| 9 | Alle Questor-Sicherheitstests bestehen | — |
| 10 | Alle Questor-Performance-/Stress-Tests bestehen | — |
| 11 | Keine produktiven Altbezeichnungen vorhanden sind | — |
| 12 | Kein produktiver Adapter vorhanden ist | — |
| 13 | QuestorBlackbox isoliert bleibt | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |
| 14 | Operational keine wissenschaftlichen Signale erzeugt | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->CHARTER §SR-08 |
| 15 | ESTOP und LEASE_DENIED strikt getrennt bleiben | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->CHARTER §SR-09 |
| 16 | SAFE_MODE weiterhin menschliche Sicherheit garantiert | <!-- @ref target="CHARTER §SR-11" type="security-rule" -->CHARTER §SR-11 |
| 17 | FRACTURE_DIAGNOSIS korrekt bleibt | — |
| 18 | Dimensions-Expansion approval-pflichtig bleibt | — |
| 19 | `idempotency_key` kanonisch ist | CONTRACTS §8.1 |
| 20 | `attempt_id` vollständig eingeschränkt ist | CONTRACTS §1.3 |
| 21 | QuestorSpec-Defaults sicher sind | CONTRACTS §1.2 |
| 22 | Circuit-Breaker-Zustände explizit sind | — |
| 23 | Policy-Veto-Review konfigurierbar ist | — |
| 24 | HAL-Minimalvertrag testbar ist | CONTRACTS §3.12 |
| 25 | HAL Langzeit-Prozesse unterstützt | CONTRACTS §3.4 |
| 26 | HAL Hardware-Interlocks unterstützt | CONTRACTS §3.11 |
| 27 | HAL Zonen-Mutex unterstützt | CONTRACTS §3.8 |
| 28 | HAL Compute-Ressourcenmodell unterstützt | CONTRACTS §3.2 |
| 29 | HAL Parameter-Schema-Registry unterstützt | CONTRACTS §3.3 |
| 30 | Naming-Allowlist explizit und review-pflichtig ist | — |
| 31 | Alle Atlas-Hybrid-Verträge sind Pydantic-v2-konform | — |
| 32 | Leere Zone ist UNEXPLORED, niemals automatisch HEALTHY | — |
| 33 | ⬜ WEISS erzeugt coverage_energy, keine support_energy | — |
| 34 | Questor schreibt keine Atlas-Signale | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| 35 | SafetyConstraint unterliegt keinem automatischen Decay | — |
| 36 | DiagnosticResolution heilt Fracture nur auditiert | — |
| 37 | FrontierCandidate enthält strukturierte Begründung | — |
| 38 | Multi-Objective Trade-offs erzeugen keine Fracture | — |
| 39 | LOCKED überschreibt alle Frontier-Freigaben | — |
| 40 | ResearchTopic wird deterministisch auf SATURATED gesetzt | — |
| 41 | Alle Strategic-Layer-Tests bestehen (Suite STRAT) | — |
| 42 | Strategic-Layer-Phasen S1–S3 abgeschlossen | — |
| 43 | ControlState wird atomar verwaltet (SL-AX-ATOMIC) | <!-- @ref target="CHARTER §SR-55" type="security-rule" -->CHARTER §SR-55 |
| 44 | Alle 10 Closure-Regeln (CT-1..CT-10) funktionieren | — |
| 45 | Intent-Verfügbarkeit wird korrekt durch Blocklists gesteuert | — |
| 46 | SAFE_MODE → NORMAL nur via menschliche Freigabe (SL-SAF-7) | <!-- @ref target="CHARTER §SR-11" type="security-rule" -->CHARTER §SR-11 |
| 47 | ESTOP_LOCKED → NORMAL nur via autorisierten Sicherheitsprozess | <!-- @ref target="CHARTER §SR-05" type="security-rule" -->CHARTER §SR-05 |
| 48 | Königin erhält exakt 3 Kontextblöcke (Constitutional Anchor) | <!-- @ref target="CHARTER §SR-13" type="security-rule" -->CHARTER §SR-13 |
| 49 | Kein security_mode im Briefing | <!-- @ref target="CHARTER §SR-29" type="security-rule" -->CHARTER §SR-29 |
| 50 | Questor und HAL kennen keine Strategic-Layer-Verträge | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |

<!-- @section id="10" title="Sicherheitsregeln für Tests" type="prose" -->
## §10 Sicherheitsregeln für Tests

<!-- @table schema="test_security_rules" -->
| # | Regel | CHARTER-Referenz |
|---|-------|-----------------|
| S1 | Tests dürfen keine echte Hardware ansprechen. | <!-- @ref target="CHARTER §SR-12" type="security-rule" -->CHARTER §SR-12 |
| S2 | Tests dürfen keine echten Leases verwenden. | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->CHARTER §SR-06 |
| S3 | Tests dürfen keine echten Gate-Records verwenden. | — |
| S4 | Tests dürfen keine echten Atlas-Daten verwenden. | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| S5 | Tests dürfen keine echten LLM-Aufrufe machen (nur Mocks). | <!-- @ref target="CHARTER §SR-13" type="security-rule" -->CHARTER §SR-13 |
| S6 | Tests müssen deterministisch sein. | <!-- @ref target="CHARTER §2" type="security-rule" -->CHARTER §2 |
| S7 | Tests müssen reproduzierbar sein. | — |
| S8 | Tests dürfen keine Daten in `data/archiv/` oder `data/atlas/` schreiben. | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| S9 | Tests dürfen keine Daten in `data/questor_blackbox/` schreiben (nur in `tests/tmp/`). | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->CHARTER §SR-07 |
| S10 | Sicherheitstests müssen die Fail-Closed-Punkte testen. | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->CHARTER §SR-10 |
| S11 | Strategic-Layer-Tests dürfen keine echten menschlichen Weisungen verwenden. | <!-- @ref target="CHARTER §SR-11" type="security-rule" -->CHARTER §SR-11 |
| S12 | Strategic-Layer-Tests dürfen keine echten ControlState-Transitionen in Produktion auslösen. | <!-- @ref target="CHARTER §SR-55" type="security-rule" -->CHARTER §SR-55 |

<!-- @section id="11" title="Kritische Warnungen für den Test" type="prose" -->
## §11 Kritische Warnungen für den Test

<!-- @section id="11.1" title="Nicht alte Kasten testen" type="prose" -->
### §11.1 Nicht alte Kasten testen

Wenn ein Test alte Kasten wie `AnalystCaste`, `PlannerCaste`, `ExecutorCaste`, `TheoristCaste` als aktive Vertragskomponenten erwartet, ist der Test falsch.

Questor ersetzt nicht diese Kasten direkt, sondern die frühere Black Box aus v2.3.1.

<!-- @section id="11.2" title="Keine Blackbox im Archivar" type="prose" -->
### §11.2 Keine Blackbox im Archivar

Wenn ein Test erwartet, dass der Archivar QuestorBlackbox liest, ist der Test falsch.
<!-- @ref target="CHARTER §SR-07" type="security-rule" -->
→ Siehe CHARTER §SR-07.

<!-- @section id="11.3" title="Keine wissenschaftlichen Signale aus operationalen Fehlern" type="prose" -->
### §11.3 Keine wissenschaftlichen Signale aus operationalen Fehlern

Wenn ein Test OOM, Timeout oder Lease-Konflikt als wissenschaftliches Signal interpretiert, ist der Test falsch.
<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08.

<!-- @section id="11.4" title="Kein ESTOP bei Ressourcenkonflikt" type="prose" -->
### §11.4 Kein ESTOP bei Ressourcenkonflikt

Wenn ein Test LEASE_DENIED als ESTOP behandelt, ist der Test falsch.
<!-- @ref target="CHARTER §SR-09" type="security-rule" -->
→ Siehe CHARTER §SR-09.

<!-- @section id="11.5" title="Kein direkter Atlas-Zugriff durch Questor" type="prose" -->
### §11.5 Kein direkter Atlas-Zugriff durch Questor

Wenn ein Test erwartet, dass Questor direkt Signale in den Atlas schreibt, ist der Test falsch.
<!-- @ref target="CHARTER §SR-04" type="security-rule" -->
→ Siehe CHARTER §SR-04.

<!-- @section id="11.6" title="Keine Doppelreferenz" type="prose" -->
### §11.6 Keine Doppelreferenz

Wenn ein Test zwei primäre Referenzdateien ohne Konflikthierarchie annimmt, ist der Test falsch.

<!-- @section id="11.7" title="Keine HAL-Lease-Vergabe" type="prose" -->
### §11.7 Keine HAL-Lease-Vergabe

Wenn ein Test erwartet, dass HAL Leases vergibt, ist der Test falsch.
<!-- @ref target="CHARTER §SR-06" type="security-rule" -->
→ Siehe CHARTER §SR-06.

<!-- @section id="11.8" title="Keine HAL-Wissenschaft" type="prose" -->
### §11.8 Keine HAL-Wissenschaft

Wenn ein Test erwartet, dass HAL wissenschaftliche Ziele interpretiert oder wissenschaftliche Signale erzeugt, ist der Test falsch.
<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08.

<!-- @section id="11.9" title="Kein CUDA-OOM als SAFETY" type="prose" -->
### §11.9 Kein CUDA-OOM als SAFETY

Wenn ein Test CUDA_OOM als SAFETY oder ESTOP interpretiert, ist der Test falsch.
<!-- @ref target="CHARTER §SR-08" type="security-rule" -->
→ Siehe CHARTER §SR-08.

<!-- @section id="11.10" title="Kein Hardware-Interlock als OPERATIONAL" type="prose" -->
### §11.10 Kein Hardware-Interlock als OPERATIONAL

Wenn ein Test Hardware-Interlock als OPERATIONAL interpretiert, ist der Test falsch.
<!-- @ref target="CHARTER §SR-09" type="security-rule" -->
→ Siehe CHARTER §SR-09.

<!-- @section id="11.11" title="Kein blinder Retry nach Crash" type="prose" -->
### §11.11 Kein blinder Retry nach Crash

Wenn ein Test erwartet, dass HAL nach einem Crash automatisch neu startet, ist der Test falsch.
<!-- @ref target="CHARTER §SR-10" type="security-rule" -->
→ Siehe CHARTER §SR-10.

<!-- @section id="11.12" title="Keine automatische Interlock-Rücksetzung" type="prose" -->
### §11.12 Keine automatische Interlock-Rücksetzung

Wenn ein Test erwartet, dass HAL einen Hardware-Interlock automatisch zurücksetzt, ist der Test falsch.
<!-- @ref target="CHARTER §SR-05" type="security-rule" -->
→ Siehe CHARTER §SR-05.

<!-- @section id="11.13" title="Keine Zonen-Lock-Eigenvergabe" type="prose" -->
### §11.13 Keine Zonen-Lock-Eigenvergabe

Wenn ein Test erwartet, dass HAL Zonen-Locks eigenmächtig vergibt, ist der Test falsch.
<!-- @ref target="CHARTER §SR-06" type="security-rule" -->
→ Siehe CHARTER §SR-06.

<!-- @section id="11.14" title="Keine Prozess-Fortsetzung ohne Resume-Token" type="prose" -->
### §11.14 Keine Prozess-Fortsetzung ohne Resume-Token

Wenn ein Test erwartet, dass HAL einen Prozess ohne gültigen Resume-Token fortsetzt, ist der Test falsch.

<!-- @section id="11.15" title="Keine Stage-Release ohne Berechtigung" type="prose" -->
### §11.15 Keine Stage-Release ohne Berechtigung

Wenn ein Test erwartet, dass HAL eine Stage ohne Berechtigung freigibt, ist der Test falsch.

<!-- @section id="11.16" title="Keine Atlas-Hybrid-Frontier ohne Evidenz" type="prose" -->
### §11.16 Keine Atlas-Hybrid-Frontier ohne Evidenz

Wenn ein Test erwartet, dass die FrontierEngine Kanten ohne `evidence_refs` erzeugt, ist der Test falsch.
<!-- @ref target="specs/GREMIUM.md §6.3" type="spec" -->
→ Siehe GREMIUM §6.3.

<!-- @section id="11.17" title="Kein automatischer Decay bei SafetyConstraint" type="prose" -->
### §11.17 Kein automatischer Decay bei SafetyConstraint

Wenn ein Test erwartet, dass ein SafetyConstraint nach Zeit automatisch abläuft, ist der Test falsch.
<!-- @ref target="specs/GREMIUM.md §6.9" type="spec" -->
→ Siehe GREMIUM §6.9.

<!-- @section id="11.18" title="Keine Kristallisation aus Sandbox-Evidenz" type="prose" -->
### §11.18 Keine Kristallisation aus Sandbox-Evidenz

Wenn ein Test erwartet, dass `evidence_class = SANDBOX` einen physischen Kristall ohne physische Validierung erzeugt, ist der Test falsch.
<!-- @ref target="specs/GREMIUM.md §6.7" type="spec" -->
→ Siehe GREMIUM §6.7.

<!-- @section id="11.19" title="Kein ControlState ohne SL-AX-ATOMIC" type="prose" -->
### §11.19 Kein ControlState ohne SL-AX-ATOMIC

Wenn ein Test erwartet, dass Achsen-Transitionen nicht atomar committet werden, ist der Test falsch.
<!-- @ref target="specs/GREMIUM_STRATEGY.md §34" type="spec" -->
→ Siehe GREMIUM_STRATEGY.md §34.

<!-- @section id="11.20" title="Keine Closure-Regel ohne Severity-Ordnung" type="prose" -->
### §11.20 Keine Closure-Regel ohne Severity-Ordnung

Wenn ein Test erwartet, dass Closure-Regeln die Severity-Ordnung ignorieren, ist der Test falsch.
<!-- @ref target="specs/GREMIUM_STRATEGY.md §34.1" type="spec" -->
→ Siehe GREMIUM_STRATEGY.md §34.1.

<!-- @section id="11.21" title="Kein SAFE_MODE-Exit ohne menschliche Freigabe" type="prose" -->
### §11.21 Kein SAFE_MODE-Exit ohne menschliche Freigabe

Wenn ein Test erwartet, dass SAFE_MODE → NORMAL automatisch erfolgt, ist der Test falsch.
<!-- @ref target="specs/GREMIUM_STRATEGY.md §13" type="spec" -->
→ Siehe GREMIUM_STRATEGY.md §13 (SL-SAF-7).

<!-- @section id="11.22" title="Kein ESTOP-Reset durch Questor oder LLM" type="prose" -->
### §11.22 Kein ESTOP-Reset durch Questor oder LLM

Wenn ein Test erwartet, dass Questor oder LLM einen ESTOP zurücksetzen kann, ist der Test falsch.
<!-- @ref target="CHARTER §SR-05" type="security-rule" -->
→ Siehe CHARTER §SR-05.

<!-- @section id="11.23" title="Keine Achsen-Parameter direkt setzen" type="prose" -->
### §11.23 Keine Achsen-Parameter direkt setzen

Wenn ein Test erwartet, dass eine Regel Achsen-Parameter direkt setzt (statt über ControlState zu lesen), ist der Test falsch.
<!-- @ref target="specs/GREMIUM_STRATEGY.md §31" type="spec" -->
→ Siehe GREMIUM_STRATEGY.md §31 (Single Ownership).

<!-- @section id="11.24" title="Kein security_mode im Briefing" type="prose" -->
### §11.24 Kein security_mode im Briefing

Wenn ein Test erwartet, dass `security_mode` im StrategicBriefing enthalten ist, ist der Test falsch.
<!-- @ref target="CHARTER §SR-29" type="security-rule" -->
→ Siehe CHARTER §SR-29.

<!-- @section id="12" title="Protokollformat" type="prose" -->
## §12 Protokollformat

Die Test-KI muss jeden Test wie folgt protokollieren:

```
[NAMING-TEST N-XX] [KOMPONENTE] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[INTEGRATIONS-TEST I-XX] [SZENARIO Y] [KOMPONENTE] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[SZENARIO-TEST S-X] [KOMPONENTE] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[REGRESSIONS-TEST R-XX] [KOMPONENTE] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[PRÄZISIERUNGS-TEST Z-XX] [KOMPONENTE] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[HAL-TEST H-XX] [KOMPONENTE] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[QUESTOR-UNIT-TEST Q-U-XXX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[QUESTOR-KOMPONENTENTEST Q-C-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[QUESTOR-SICHERHEITSTEST Q-S-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[QUESTOR-PERFORMANCETEST Q-P-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[QUESTOR-STRESSTEST Q-T-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-CTR-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-SEM-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-TOPO-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-INT-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-DIAG-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-SAF-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-FRNT-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-TOP-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[ATLAS-TEST ATLAS-DOM-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[STRAT-TEST STRAT-CTR-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[STRAT-TEST STRAT-AX-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[STRAT-TEST STRAT-KANZ-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[STRAT-TEST STRAT-KOEN-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[STRAT-TEST STRAT-SYM-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
[STRAT-TEST STRAT-E2E-XX] [MODUL] [PROBLEM?] [BESTANDEN/NICHT BESTANDEN]
```

Am Ende müssen die Gesamtsummen stehen:

```
NAMING GESAMT: X/7 BESTANDEN
INTEGRATION GESAMT: X/18 BESTANDEN
SZENARIEN GESAMT: X/5 BESTANDEN
REGRESSION GESAMT: X/12 BESTANDEN
PRÄZISIERUNG GESAMT: X/8 BESTANDEN
HAL GESAMT: X/24 BESTANDEN
QUESTOR-UNIT GESAMT: X/~252 BESTANDEN
QUESTOR-KOMPONENTEN GESAMT: X/~44 BESTANDEN
QUESTOR-SICHERHEIT GESAMT: X/~30 BESTANDEN
QUESTOR-PERFORMANCE GESAMT: X/~10 BESTANDEN
QUESTOR-STRESS GESAMT: X/~11 BESTANDEN
ATLAS-CTR GESAMT: X/~15 BESTANDEN
ATLAS-SEM GESAMT: X/~20 BESTANDEN
ATLAS-TOPO GESAMT: X/~15 BESTANDEN
ATLAS-INT GESAMT: X/~15 BESTANDEN
ATLAS-DIAG GESAMT: X/~10 BESTANDEN
ATLAS-SAF GESAMT: X/~10 BESTANDEN
ATLAS-FRNT GESAMT: X/~15 BESTANDEN
ATLAS-TOP GESAMT: X/~10 BESTANDEN
ATLAS-DOM GESAMT: X/~10 BESTANDEN
ATLAS GESAMT: X/~120 BESTANDEN
STRAT-CTR GESAMT: X/~20 BESTANDEN
STRAT-AX GESAMT: X/~40 BESTANDEN
STRAT-KANZ GESAMT: X/~55 BESTANDEN
STRAT-KOEN GESAMT: X/~25 BESTANDEN
STRAT-SYM GESAMT: X/~15 BESTANDEN
STRAT-E2E GESAMT: X/~15 BESTANDEN
STRAT GESAMT: X/~170 BESTANDEN
GESAMT: X/~711 BESTANDEN
```

<!-- @section id="13" title="Zusammenfassender Bericht an die Test-KI" type="prose" -->
## §13 Zusammenfassender Bericht an die Test-KI

Am Ende des Testlaufs muss die Test-KI einen Bericht in dieser Struktur liefern:

```markdown
## Testbericht — MYRMEX v2.4.0 + Questor v0.2.3 + HAL v0.2.0

### 1. Modus
- Dry-Run | Implementierung

### 2. Testgrundlage
- CHARTER.md (foundation/)
- CONTRACTS.md (foundation/)
- QUESTOR.md (specs/)
- HAL.md (specs/)
- GREMIUM.md (specs/)
- GREMIUM_STRATEGY.md (specs/)
- VALIDATION.md (ops/)
- VALIDATION_ATLAS.md (ops/)
- optional: produktives Repository

### 3. Ergebnisse
NAMING GESAMT: X/7 BESTANDEN
INTEGRATION GESAMT: X/18 BESTANDEN
SZENARIEN GESAMT: X/5 BESTANDEN
REGRESSION GESAMT: X/12 BESTANDEN
PRÄZISIERUNG GESAMT: X/8 BESTANDEN
HAL GESAMT: X/24 BESTANDEN
QUESTOR-UNIT GESAMT: X/~252 BESTANDEN
QUESTOR-KOMPONENTEN GESAMT: X/~44 BESTANDEN
QUESTOR-SICHERHEIT GESAMT: X/~30 BESTANDEN
QUESTOR-PERFORMANCE GESAMT: X/~10 BESTANDEN
QUESTOR-STRESS GESAMT: X/~11 BESTANDEN
ATLAS GESAMT: X/~120 BESTANDEN
STRAT GESAMT: X/~170 BESTANDEN
GESAMT: X/~711 BESTANDEN

### 4. Blocker
- [Blocker 1]
- [Blocker 2]
- oder: keine

### 5. Nicht-Blocker
- [Nicht-Blocker 1]
- oder: keine

### 6. Kritische Abweichungen
- [Abweichung]
- oder: keine

### 7. Sicherheitsrelevante Befunde
- [Befund]
- oder: keine

### 8. Gesamtbewertung
- BESTANDEN | NICHT BESTANDEN | TEILWEISE BESTANDEN

### 9. Freigabeempfehlung
- Freigabe für Phase X | keine Freigabe | nur bedingte Freigabe

### 10. Nächster Schritt
- [konkreter nächster Schritt]
```

<!-- @section id="14" title="Fehlerbericht bei nicht bestandenen Tests" type="prose" -->
## §14 Fehlerbericht bei nicht bestandenen Tests

Wenn ein Test fehlschlägt, muss die Test-KI zusätzlich melden:

```
Fehlgeschlagener Test: [ID]
Komponente: [Komponente]
Problem: [Problem]
Erwartetes Verhalten: [Erwartung]
Beobachtetes Verhalten: [Beobachtung]
Wahrscheinliche Ursache: [Ursache]
Empfohlene Korrektur: [Korrektur]
Priorität: Blocker | Hoch | Mittel | Niedrig
```

Wenn ein Test wegen fehlender Eingaben nicht prüfbar ist:

```
Nicht prüfbarer Test: [ID]
Grund: [Grund]
Empfehlung: [benötigte Unterlage oder Freigabe]
Status: BLOCKIERT | NICHT PRÜFBAR
```

Ein nicht prüfbarer Test darf nicht stillschweigend als bestanden markiert werden.

<!-- @section id="15" title="Dokumentenhierarchie" type="prose" -->
## §15 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `ops/` und referenziert:

<!-- @table schema="document_hierarchy" -->
| Referenz | Zweck |
|----------|-------|
| `foundation/CHARTER.md` | Sicherheitsregeln (CHARTER §SR-XX) |
| `foundation/CONTRACTS.md` | Datenverträge (CONTRACTS §X.X) |
| `specs/QUESTOR.md` | Questor-spezifische Details |
| `specs/HAL.md` | HAL-spezifische Details |
| `specs/GREMIUM.md` | Gremium-spezifische Details (inkl. Atlas-Hybrid-System §6) |
| `specs/GREMIUM_STRATEGY.md` | Strategic-Layer-Regeln (Achsen, ControlState, Kanzler/Königin) |
| `ops/VALIDATION_ATLAS.md` | Vollständige Atlas-Hybrid-Test-Spezifikation |
| `ops/ROADMAP.md` | Implementierungsplan und Phasen |

Regel: Änderungen an Test-Suiten in diesem Dokument erfordern eine Versionsänderung und eine Überprüfung der referenzierten Dokumente.

<!-- @section id="A" title="Anhang A: Akzeptanzprüfung für ATLAS-HYB-1.0.0" type="acceptance" -->
## Anhang A: Akzeptanzprüfung für ATLAS-HYB-1.0.0

Nach dem Einfügen der Atlas-Hybrid-Änderungen sollte `VALIDATION.md` folgende Kriterien erfüllen:

<!-- @table schema="acceptance_criteria_atlas" -->
| # | Kriterium | Status |
|---|-----------|--------|
| 1 | Kopfzeile enthält Version `1.1.0-atlas-hyb.1` | ☐ |
| 2 | §0.1 Änderungsantrag ATLAS-HYB-1.0.0 ist vorhanden | ☐ |
| 3 | §2.2 enthält Atlas-Hybrid-Tests in der Verteilung | ☐ |
| 4 | §2.3 enthält Suite ATLAS in der Übersicht | ☐ |
| 5 | §4.6 definiert die Atlas-Test-Bereiche | ☐ |
| 6 | §8.1 enthält Atlas-Phase in der Ausführungsreihenfolge | ☐ |
| 7 | §8.2 enthält GATE-ATLAS | ☐ |
| 8 | §9 enthält Atlas-spezifische Akzeptanzkriterien (31–40) | ☐ |
| 9 | §12 enthält Atlas-Protokollformat | ☐ |
| 10 | Gesamtzahl ist ~541 Tests (vor STRAT-Erweiterung) | ☐ |
| 11 | Keine neuen Sicherheitsregeln wurden definiert | ☐ |
| 12 | CHARTER-Hierarchie bleibt gewahrt | ☐ |
| 13 | Referenz auf `ops/VALIDATION_ATLAS.md` ist vorhanden | ☐ |

<!-- @section id="B" title="Anhang B: Akzeptanzprüfung für STRAT-1.0.0" type="acceptance" -->
## Anhang B: Akzeptanzprüfung für STRAT-1.0.0

Nach dem Einfügen der Strategic-Layer-Änderungen sollte `VALIDATION.md` folgende Kriterien erfüllen:

<!-- @table schema="acceptance_criteria_strat" -->
| # | Kriterium | Status |
|---|-----------|--------|
| 1 | Kopfzeile enthält Version `1.2.0-strat.1` | ☐ |
| 2 | §0.2 Änderungsantrag STRAT-1.0.0 ist vorhanden | ☐ |
| 3 | §2.2 enthält Strategic-Layer-Tests in der Verteilung | ☐ |
| 4 | §2.3 enthält Suite STRAT in der Übersicht | ☐ |
| 5 | §4.7 definiert die STRAT-Test-Bereiche | ☐ |
| 6 | §4.7.2 enthält STRAT-CTR-Tests (~20 Tests) | ☐ |
| 7 | §4.7.3 enthält STRAT-AX-Tests (~40 Tests) | ☐ |
| 8 | §4.7.4 enthält STRAT-KANZ-Tests (~55 Tests) | ☐ |
| 9 | §4.7.5 enthält STRAT-KOEN-Tests (~25 Tests) | ☐ |
| 10 | §4.7.6 enthält STRAT-SYM-Tests (~15 Tests) | ☐ |
| 11 | §4.7.7 enthält STRAT-E2E-Tests (~15 Tests) | ☐ |
| 12 | §5.1 enthält Strategic-Layer-Test-Fixtures | ☐ |
| 13 | §8.1 enthält STRAT-Phase in der Ausführungsreihenfolge | ☐ |
| 14 | §8.2 enthält GATE-STRAT | ☐ |
| 15 | §9 enthält Strategic-Layer-Akzeptanzkriterien (41–50) | ☐ |
| 16 | §11 enthält Strategic-Layer-Warnungen (11.19–11.24) | ☐ |
| 17 | §12 enthält STRAT-Protokollformat | ☐ |
| 18 | Gesamtzahl ist ~711 Tests | ☐ |
| 19 | Keine neuen Sicherheitsregeln wurden definiert | ☐ |
| 20 | CHARTER-Hierarchie bleibt gewahrt | ☐ |
| 21 | Referenz auf `specs/GREMIUM_STRATEGY.md` ist vorhanden | ☐ |
| 22 | Questor und HAL kennen keine Strategic-Layer-Verträge (SL-ACC-4) | ☐ |
| 23 | SAFE_MODE-Exit nur via menschliche Freigabe (SL-SAF-7) | ☐ |
| 24 | ESTOP-Reset nur via autorisierten Sicherheitsprozess (SR-05) | ☐ |
| 25 | Constitutional Anchor: Königin erhält exakt 3 Kontextblöcke | ☐ |
| 26 | Kein security_mode im Briefing (SR-29) | ☐ |