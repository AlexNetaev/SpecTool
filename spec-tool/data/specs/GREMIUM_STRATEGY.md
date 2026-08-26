---
doc_id: specs/GREMIUM_STRATEGY.md
doc_type: spec
version: 1.0.0
status: BINDEND
schema_version: spec-format-1.0
layer: specs
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1-twin.1
  - specs/GREMIUM.md@2.0.0-strat.1
conflict_rule: [CHARTER, CONTRACTS, GREMIUM, THIS_DOC]
roles_defined:
  - kanzler
  - koenigin
roles_referenced:
  - vordenker
  - lotse
  - quartiermeister
  - kartograph
  - archivar
dataflows_defined:
  - briefing_cycle
  - directive_validation
  - axiom_transition
  - symptom_trigger
  - mission_bootstrap
  - digital_twin_strategic_loop
last_modified: 2026-08-21
---

<!-- @section id="0" title="Zweck, Leseregel, Geltung" type="meta" -->
# 🧠 GREMIUM_STRATEGY — STRATEGISCHE STEUERUNG (COGNITIVE OBSERVATORY)

## §0 Zweck, Leseregel, Geltung

<!-- @section id="0.1" title="Zweck" type="prose" -->
### §0.1 Zweck

Dieses Dokument definiert die strategische Kognitionsschicht des Gremiums („Cognitive Observatory"): ein System, das über Wochen autonom forschen kann — drift-frei, CHARTER-konform, mit deterministischen Endentscheidungen und definierten menschlichen Eingriffspunkten.

<!-- @section id="0.2" title="Abgrenzung zu GREMIUM.md" type="prose" -->
### §0.2 Abgrenzung zu GREMIUM.md

<!-- @ref target="specs/GREMIUM.md §0.2" type="spec" -->
GREMIUM.md definiert die Pipeline-Mechanik: 9-Stufen-Pipeline, Archivar → Kartograph → Vordenker → Lotse → Quartiermeister → Sicherheitsrat → Dispatcher → Questor → Receiver.

Dieses Dokument definiert die strategische Steuerung: Kanzler/Königin, Briefing-Zyklus, 4-Achsen-Architektur, ControlState, Intent-Verfügbarkeit, Closure-Regeln.

Beide Dokumente bilden eine Einheit. GREMIUM.md ist das „Wie läuft ein Zyklus ab?", dieses Dokument ist das „Wer entscheidet was?".

<!-- @section id="0.3" title="Leseregel und Konfliktregel" type="prose" -->
### §0.3 Leseregel und Konfliktregel

<!-- @table schema="conflict_hierarchy" -->
| Rang | Dokument | Autorität |
|------|----------|-----------|
| 1 | CHARTER | Absolut |
| 2 | CONTRACTS | Datenverträge |
| 3 | GREMIUM.md | Pipeline-Mechanik |
| 4 | Dieses Dokument | Strategie/Achsen-Steuerung |

Innerhalb dieses Dokuments: SAFETY-Regeln (SL-SAF, SR-05, SR-19) sind absolut und überstimmen alle anderen Regeln.

Die 4-Achsen-Steuerung (§29..§34) ist eine DESIGN-FESTLEGUNG; wo sie vom Quell-SystemMode abweicht, ist sie als solche markiert.

<!-- @section id="0.4" title="Vertragsreferenz" type="prose" -->
### §0.4 Vertragsreferenz

<!-- @ref target="foundation/CONTRACTS.md §6.11" type="contract" -->
Alle Datenverträge (Enums, Pydantic-Modelle, Config) sind in CONTRACTS.md §6.11 definiert. Dieses Dokument definiert keine neuen Verträge. Es referenziert ausschließlich:

<!-- @table schema="contract_references" -->
| Vertrag | Abschnitt | Zweck |
|---------|-----------|-------|
| ControlState | CONTRACTS §6.11.1 | Gesamtzustand als 4-Achsen-Tupel |
| AxisTransition | CONTRACTS §6.11.2 | Einzelne Achsen-Transition |
| ControlStateLog | CONTRACTS §6.11.3 | Persistente Log-Datei |
| StrategicBriefing | CONTRACTS §6.11.4 | Briefing an die Königin |
| StrategicDirective | CONTRACTS §6.11.5 | Direktive der Königin |
| DirectiveParameters | CONTRACTS §6.11.6 | Discriminierte Union über Intent |
| Mission-Verträge | CONTRACTS §6.11.7 | ResearchManifest, ObjectiveFamilySeed |
| Governance-Verträge | CONTRACTS §6.11.8 | HumanResponseFile, HumanDirective, RoyalLog |
| Forschungs-Verträge | CONTRACTS §6.11.9 | ScientificHypothesis, DimensionOnboardingRequest |
| Report-Verträge | CONTRACTS §6.11.10 | FinalScientificReport |
| StrategicLayerConfig | CONTRACTS §6.11.11 | Gesamtkonfiguration |

<!-- @section id="0.5" title="Ehrlichkeitshinweis" type="prose" -->
### §0.5 Ehrlichkeitshinweis (bindend für Tests)

Die Achsen-Architektur ist eine Design-Festlegung, keine Quell-Ableitung. Die Severity-Ordnung (§34.1) und Closure-Regeln (§34.2) sind bewusste Wahlen. Die Dry-Tests DT8–DT10 waren selbst-generiert; reale Validierung steht aus.

<!-- @section id="1" title="MODUL CORE" type="prose" -->
## MODUL CORE

<!-- @section id="1" title="Grunddefinitionen" type="prose" -->
### §1 Grunddefinitionen (SL-DEF-1..5)

<!-- @table schema="definitions" -->
| ID | Definition | Text |
|----|-----------|------|
| SL-DEF-1 | Strategischer Zyklus | 1 Zyklus = 1 abgeschlossener Regelkreis: StrategicBriefing erzeugt → StrategicDirective empfangen → Validierung → Policy-Wirkung. Alle `*_cycles` beziehen sich darauf. |
| SL-DEF-2 | Weißraum | Eine Region ist Weißraum, wenn ihre Zone `UNEXPLORED` ist oder `EXPLORED_INCONCLUSIVE` mit `evidence_mass == 0`. |
| SL-DEF-3 | Pipeline-Takt | ereignisgetrieben; jedes verarbeitete Ergebnis schreitet fort. Treibt Archivar/Kartograph/Atlas. |
| SL-DEF-4 | Strategie-Zyklus | der Briefing-Regelkreis (SL-DEF-1). `briefing_id` ist die einzige Zyklen-ID (`zyklus_id` abgeschafft). Auslösung durch `cycle_trigger ∈ {TIME, EVENT_COUNT, MANUAL}`. |
| SL-DEF-5 | TimeService | Alle `*_days`-Parameter und Timeout-Auswertungen nutzen `TimeService`. Alle `*_cycles` nutzen den Strategie-Zyklus. Keine Vermischung. |

<!-- @section id="2" title="Rollen und Zugriffsregeln" type="prose" -->
### §2 Rollen und Zugriffsregeln (SL-ACC-1..4)

<!-- @table schema="role_access_matrix" -->
| Rolle | Schicht | LLM | Funktion | Achsen-Interaktion |
|-------|---------|-----|----------|-------------------|
| 👑 Königin | 5 | Ja (stateless) | Vision, Pivot, Budget-Vorschläge | liest ControlState via Briefing |
| 🏛️ Kanzler | 4 | Nein | Briefing, Validierung, Policy, RoyalLog, Achsen-Verwaltung | liest+schreibt ControlState |
| 🧠 Vordenker | 4 | Ja (grounded) | Hypothesen, Dimensions-Vorschläge | liest via SymptomEvents |
| 🧭 Lotse | 4 | Nein | Wegmarken, Capability-Prüfung | liest für Capability-Checks |
| 📦 Quartiermeister | 4 | Nein | Paketbau, Manifest-/Twin-Checks | liest für Paketbau |
| ⚖️ Sicherheitsrat | 4 | Seher advisor | Gate | liest SafetyAxis |
| 🗺️ Kartograph | 4 | Nein | Atlas, Symptome, Twin-Divergenz | liest für Symptom-Erzeugung |
| 📚 Archivar | 4 | Nein | Wissensaufnahme, Sanitization | liest für Sanitization |
| 🧭 Questor | 2 | intern | Ausführung (unverändert) | keine |

<!-- @table schema="access_rules" -->
| ID | Regel | CHARTER-Referenz |
|----|-------|-----------------|
| SL-ACC-1 | Alle Kommunikation über Blackboard-Artefakte (§24.5). Keine direkten Aufrufe. | <!-- @ref target="CHARTER §2" type="security-rule" -->CHARTER §2 |
| SL-ACC-2 | Die Königin liest den Atlas nicht direkt; ihr einziger Zugang ist das StrategicBriefing. | — |
| SL-ACC-3 | Der Vordenker liest Atlas-Topologie nur lesend als kuratierte Ausschnitte; er schreibt nie in den Atlas. | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |
| SL-ACC-4 | Questor und HAL bleiben unverändert; sie kennen keine strategischen Verträge. | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->CHARTER §SR-04 |

<!-- @section id="3" title="Constitutional Anchor Protocol" type="prose" -->
### §3 Constitutional Anchor Protocol (SL-ANCHOR-1..4)

<!-- @dataflow id="constitutional_anchor" trigger="KÖNIGIN_LLM_AUFRUF" source_role="kanzler" target_role="koenigin" -->
Jeder Königin-LLM-Aufruf erhält exakt drei Kontextblöcke (SL-ANCHOR-1):

<!-- @table schema="anchor_blocks" -->
| Block | Typ | Inhalt | Variabilität |
|-------|-----|--------|-------------|
| CONSTITUTIONAL MEMORY | invariant | mission_goal, hard_constraints, soft_preferences, Verbotene Aktionen, Output-Schema | Konstant pro Mission |
| STATELESS BRIEFING | dynamisch | aggregierter Zustand, Budget, Fractures, Twin-Status, DecisionsRequired — kein security_mode, keine Hybrid-Referenzen, kein Roh-metric_vector | Variiert pro Briefing |
| ANCHOR | Kontinuität | zuerst aktive HUMAN_OVERRIDE-Einträge, dann die letzten `royal_log_anchor_depth` (=3) eigenen Direktiven mit Outcome | Variiert pro Briefing |

<!-- @table schema="anchor_rules" -->
| ID | Regel |
|----|-------|
| SL-ANCHOR-2 | Kein persistenter Gesprächsverlauf. Jeder Aufruf frisch. |
| SL-ANCHOR-3 | Menschliche Weisungen im Anchor überschreiben alle Königin-Direktiven (expliziter Hinweis im Anchor). |
| SL-ANCHOR-4 | LLM-Fehler/Timeout → Policy bleibt unverändert, Audit, kein erweiterter Retry. Nach `max_consecutive_llm_failures` → Eskalation. |

<!-- @section id="4" title="Architektur-Überblick" type="prose" -->
### §4 Architektur-Überblick

<!-- @table schema="architecture_layers" -->
| Ebene | Komponente | Funktion |
|-------|-----------|----------|
| MENSCH | — | setzt ResearchManifest, beantwortet Eskalationen, SAFE_MODE |
| SCHICHT 5 | 👑 KÖNIGIN (stateless LLM) | IN: Manifest + Briefing + Anchor; OUT: StrategicDirective |
| SCHICHT 4 | 🏛️ KANZLER (deterministisch) | Briefing · Validator (10 Stufen) · DTT · RoyalLog · Budget · Dimension-/Eskalations-Governance · SAFETY-RESPONSE · ControlState-Verwaltung |
| SCHICHT 4 | PIPELINE | KARTOGRAPH → VORDENKER → PRE-FILTER → LOTSE → QUARTIERMEISTER → SICHERHEITSRAT → DISPATCH → QUESTOR → ARCHIVAR → KARTOGRAPH → ATLAS |

<!-- @section id="5" title="Kern-Patterns" type="prose" -->
### §5 Kern-Patterns

<!-- @table schema="core_patterns" -->
| Pattern | Abschnitt | Beschreibung |
|---------|-----------|-------------|
| Stateless Director | §5.1 | Königin zustandslos |
| Deterministic Gatekeeper | §5.2 | Kanzler rein deterministisch (SL-GATE-1). Kein LLM im Kanzler. |
| Topology-Grounded Hypothesis Engine | §5.3 | Vordenker nur via SymptomEvents |
| Digital-Twin-Loop | §5.4 | gemäß DIGITAL-TWIN-SEM, gehärtet (§14) |
| Orthogonal Control Axes | §5.5 (DESIGN) | 4 Achsen (§29), ControlState-Tupel |

<!-- @section id="6" title="MODUL RULES" type="prose" -->
## MODUL RULES

<!-- @section id="6" title="Missions-Bootstrap" type="dataflow" dataflow="mission_bootstrap" -->
### §6 Missions-Bootstrap (SL-BOOT-0..8)

<!-- @dataflow id="mission_bootstrap" trigger="MENSCH_ERSTELLT_MANIFEST" source_role="mensch" target_role="kanzler" -->
<!-- @dataflow-step order="1" -->
SL-BOOT-0 Manifest-Intake (fail-closed): `created_by==MENSCH` und `approved_by==MENSCH`; `value` XOR `range` je Operator; jeder `dimension_ref` existiert in `initial_dimensions`; EXCLUSION mit `categories` nicht-leer; `valid_until` via TimeService in Zukunft. Verstoß → REJECT.

<!-- @dataflow-step order="2" -->
SL-MAN-9 Operator×Enforcement-Matrix: EXCLUSION mit `categories` ODER (operator+value); SAFETY mit (operator+value); BOUNDS mit `range` ODER (operator+value).

<!-- @dataflow-step order="3" -->
SL-BOOT-1..6 Kaltstart: Mensch erstellt Manifest → Kanzler erzeugt MissionBootstrap (Dimensionen, ObjectiveFamily, Topic PROPOSED, Budget) → materialisiert Constraints → BOOTSTRAP-Briefing → Königin antwortet INITIAL_SWEEP → Topic ACTIVE → Kanzler emittiert SymptomEvent(INITIAL_SWEEP).

<!-- @dataflow-step order="4" -->
SL-BOOT-2 erweitert: Fehlen `lab_ambient_temp`/`lab_ambient_humidity` → Bootstrap blockiert (Schatten-Variablen-Check stets ausführbar).

<!-- @dataflow-step order="5" -->
SL-BOOT-2b Initiale Zonen: aus deterministischem Template des ObjectiveFamilySeed; leerer Atlas → `avg_uncertainty_score = None`.

<!-- @dataflow-step order="6" -->
SL-BOOT-7 Template-Lücke: fehlendes Template → Paket zurückgestellt, G-1 ausgelöst.

<!-- @dataflow-step order="7" -->
SL-BOOT-8 Deadlock-Schutz: nach `bootstrap_retry_limit` (=3) invaliden INITIAL_SWEEP-Antworten → TEMPLATE_GAP-Eskalation; Topic bleibt PROPOSED.

<!-- @section id="7" title="Validierungspipeline v2" type="dataflow" dataflow="directive_validation" -->
### §7 Validierungspipeline v2 (10 Stufen, feste Reihenfolge)

<!-- @dataflow id="directive_validation" trigger="STRATEGIC_DIRECTIVE_EMPFANGEN" source_role="koenigin" target_role="kanzler" -->
<!-- @dataflow-step order="1" -->
```
StrategicDirective
 ├─ 1. Schema (Pydantic + Intent-Submodelle, SL-DIR-9)  FAIL → VETO("SCHEMA_INVALID")
 ├─ 2. briefing_ref-Existenz (SL-DIR-2)                 FAIL → VETO("REF_NOT_FOUND")
 ├─ 3. Manifest-Prüfung (+ Seed-Feasibility SL-DTT-2)   FAIL → VETO("MANIFEST_VIOLATION")
 ├─ 3b. Weisungs-Prüfung (aktive HumanDirective)         FAIL → VETO("HUMAN_DIRECTIVE_VIOLATION")
 ├─ 3c. Target-Existenz & Zustandsmatrix                 FAIL → VETO("TARGET_LOCKED"/"TARGET_TERMINAL")
 ├─ 4. Safety-/Injection-Prüfung (rekursiv, Wortlisten)  FAIL → VETO + Audit
 ├─ 5. Budget-Prüfung (inkl. reserved-Simulation)        FAIL → VETO("BUDGET_NEGATIVE")
 ├─ 6. Intent-Sonderregeln (alle Intents, SL-DTT)
 ├─ 6b. Mode-Prüfung via ControlState (§32)              FAIL → VETO("MODE_VIOLATION")
 ├─ 6c. Semantische Dedup (SL-INT-5)                     FAIL → VETO("DUPLICATE_SEMANTIC")
 ├─ 7. Konflikt-Modus-Prüfung (SL-CON-3)                 FAIL → VETO("CONFLICT_MODE")
 └─ 8. ACCEPT → DirectiveTranslationTable
```

Schritt 6b (Mode-Prüfung): liest den ControlState und wendet die Intent-Verfügbarkeit (§32) an. Die Intent-Whitelist ergibt sich aus der Achsen-Kombination, nicht aus einem separaten SystemMode.

<!-- @section id="8" title="DirectiveTranslationTable" type="prose" -->
### §8 DirectiveTranslationTable (SL-DTT)

Deterministische Übersetzung; kein Interpretationsspielraum.

<!-- @table schema="directive_translation" -->
| Intent | Pflicht-Parameter | Deterministische Wirkung |
|--------|------------------|------------------------|
| NO_ACTION | — | keine Policy-Änderung; Zyklus protokolliert |
| INITIAL_SWEEP | grid_spec, sweep_template_ref | Topic PROPOSED→ACTIVE, Seed-Symptom. Setzt exploration_weight NICHT direkt (RESEARCH-besetzt) |
| PIVOT_DOMAIN / PIVOT_TARGET | from_topic_ref, to_topic_seed | Scope-Check (SL-DIR-8), Feasibility (SL-DTT-2), Loop-Erkennung (SL-DTT-3); altes Topic→ARCHIVED nach Lessons-Learned; neues PROPOSED |
| UNLOCK_BUDGET | amount_cycles, purpose | immer Eskalation(BUDGET); bei Bestätigung reserved→used (SL-BUD-3) |
| ABORT_MISSION | reason | immer ESCALATED; nur mit menschlicher Bestätigung |
| ADD_DIMENSION_HINT | source_ref, dimension_seed | erzeugt DimensionOnboardingRequest |
| INCREASE_DIAGNOSTIC | zone_ref, amount | diagnostic_budget += amount (max) |
| CALIBRATE_TWIN | twin_ref | VETO wenn nicht gedriftet (NO_DRIFT); sonst diagnostic_weight↑ |
| ARCHIVE_TOPIC | topic_ref | Topic→ARCHIVED nach Lessons-Learned |
| SET_PRIORITY | topic_ref, priority | Topic.priority setzen |
| DROP_SOFT_PREFERENCE | preference_ref | soft_preference deaktivieren |
| HUMAN_ESCALATION | question, escalation_category | Eskalation mit Typ aus category. Bei escalation_category=CAPEX: löst zusätzlich resource → PHYSICAL_WAIT (via CT-5) und governance → AWAITING_HUMAN (via CT-6) aus. (BF-08) |
| SET_RESEARCH_PHASE | target_phase, reason | löst ResearchAxis-Wechsel aus (§33); Validierung prüft Ziel-ControlState |

<!-- @table schema="dtt_rules" -->
| ID | Regel |
|----|-------|
| SL-DTT-1 | Lessons-Learned: topic-lokale weiche Filter (TopicConstraintProposal), keine ManifestConstraints. Aufstieg zu hart nur über neue menschliche Manifest-Version (SL-MAN-1 gewahrt). |
| SL-BRF-9 | provisional: Die DTT setzt `royal_log_entry.provisional = true`, wenn `briefing_ref` auf ein trunkiertes Briefing verweist (`briefing.truncation_applied == true`). Es ist ein DTT-Ausgabe-/Audit-Feld, kein Feld der Königin-Direktive. |

<!-- @section id="9" title="Konfliktdetektor und NO_ACTION" type="prose" -->
### §9 Konfliktdetektor & NO_ACTION (SL-CON, SL-NOACT)

<!-- @table schema="conflict_rules" -->
| ID | Regel |
|----|-------|
| SL-CON-1 | Jeder GOVERNANCE-VETO gegen eine Königin-Direktive zählt als Konflikt (BENIGN-VETOs zählen nicht, SL-CON-4). |
| SL-CON-2 | 2 Konflikte in `conflict_window_cycles` → URGENT + Eskalation(DEADLOCK); Königin erzeugt nur noch NO_ACTION. |
| SL-CON-3 | Mechanischer Konflikt-Modus: nur NO_ACTION/HUMAN_ESCALATION angenommen; übrige → VETO("CONFLICT_MODE"), zählt nicht als neuer Konflikt. |
| SL-CON-4 | VETO-Schwere-Klassen: BENIGN = {NO_DRIFT, TARGET_LOCKED, einzelne SCHEMA_INVALID, DUPLICATE_SEMANTIC}; GOVERNANCE = {MANIFEST_VIOLATION, HUMAN_DIRECTIVE_VIOLATION, Safety-/Injection-VETOs}. |
| SL-INT-5 | Semantische Dedup: `semantic_directive_id = sha256(intent + target_ref + canonical_json(parameters))`. Wiederholung mit gleichem Outcome innerhalb `semantic_dedup_window_cycles` → VETO("DUPLICATE_SEMANTIC"), ausgenommen NO_ACTION. |
| SL-NOACT-1 | liest `governance.stall_detection_active`. Wenn false → Stall-Counter wird NICHT erhöht. Wenn true → `no_action_stall_limit` aufeinanderfolgende NO_ACTION ohne Atlas-Fortschritt → URGENT. Reset nach URGENT-Zustellung. |
| SL-NOACT-2 | Während HOLD/SAFE (governance=AWAITING_HUMAN oder safety=SAFE_MODE) ist die Stall-Überwachung suspendiert. Kein Eskalations-Sturm. |

<!-- @section id="10" title="Symptom-Trigger und Vordenker" type="dataflow" dataflow="symptom_trigger" -->
### §10 Symptom-Trigger und Vordenker

<!-- @dataflow id="symptom_trigger" trigger="ATLAS_EREIGNIS" source_role="kartograph" target_role="vordenker" -->
<!-- @table schema="symptom_triggers" -->
| Symptom | Deterministische Bedingung | Vordenker-Aktion |
|---------|--------------------------|-----------------|
| INITIAL_SWEEP | Bootstrap (SL-BOOT-6) | Seed-Modus |
| WEISSRAUM | Zone gemäß SL-DEF-2 | Void-Prompting |
| FRACTURE_GAP | fracture_score ≥ quarantine_threshold | Fracture-Prompting |
| SATURATION | Topic-StopCondition SATURATION_CYCLES (einzige Quelle) | Paradigma-Wechsel |
| BRIDGE_OPP | Cluster-Kanten ≥ bridge_edge_threshold | Bridge-Prompting |
| TWIN_DRIFT | tolerance_breached = true | Twin-Calibration-Prompting |
| CAPABILITY_GAP_FEEDBACK | CapabilityGapSignal eingegangen | Hypothese anpassen |
| DIMENSION_GAP | Idee wegen approved=false-Dimension blockiert | alternative Hypothese |
| REPLICATE_DIVERGENCE | SL-SIG-5 | Replikations-Hypothese |
| QUARANTINE_BLOCK | Idee in quarantinierter Zone blockiert | Diagnose-Hypothese |

<!-- @table schema="urgent_triggers" -->
| ID | Regel |
|----|-------|
| SL-URG-1 | URGENT-Trigger: fracture_score ≥ full_rebuild_threshold; tolerance_breached; Topic SATURATED ohne Ziel bei Budget > stagnation_budget_threshold; LOCKED-Zone ohne Diagnose-Strategie; Konflikt; CapabilityGap mit requires_budget_or_hardware; SAFETY-Ereignis; Manifest-Sprung; NO_ACTION-Stall; Quarantäne-Timeout; questor_health_status==DEAD; remaining_cycles ≤ budget_unlock_threshold_fraction; Mission ohne aktives Topic. |
| SL-URG-3 | URGENT-Nachzügler während Cooldown werden ins nächste PERIODIC gemerged; kein stiller Verlust. |
| SL-SYM-1 | Verlustschutz: SymptomEvents vor Queue-Übergabe persistent; bei High-Watermark zurückgestellt und erneut zugestellt (At-Least-Once). |

<!-- @section id="11" title="Signal-Semantik" type="prose" -->
### §11 Signal-Semantik (SL-SIG, SL-HYP)

<!-- @table schema="signal_semantics_strategic" -->
| ID | Regel |
|----|-------|
| SL-SIG-1 | Korrigierter Fallback: WENN expectation_ref vorhanden: confirms_expectation==False → 🟨 CONTRADICTION (REFUTES); confirms_expectation==True → 🟩 (≥0.8) bzw. ⬜ (<0.8); confirms_expectation==None → ⬜ EXPLORATORY_COVERAGE. WENN keine Erwartung UND ziel_erreicht==True: konfidenz ≥ 0.8 → 🟩 CONFIRMATION; ≥ 0.5 → ⬜ EXPLORATORY_COVERAGE. WENN keine Erwartung UND ziel_erreicht==False: → ⬜ EXPLORATORY_COVERAGE mit evidence_kind = NEGATIVE_KNOWLEDGE |
| SL-SIG-2 | Operationale Paketfehler fließen nie in wissenschaftliche Metriken (nur HardwareHealth.operational_failure_count_recent). |
| SL-SIG-3 | Sättigung hat genau eine Quelle (Topic-StopCondition SATURATION_CYCLES). |
| SL-SIG-4 | ObjectiveFamily-Constraints werden binär gegatet. |
| SL-SIG-5 | Replikat-Divergenz: zwei parameter-äquivalente Kristalle mit Differenz > tolerance → REPLICATE_DIVERGENCE (nur wenn `replicate_divergence_check == true`, RESEARCH-besetzt). „Parameter-äquivalent" bedeutet: Alle Diskrepanzen in kontinuierlichen Dimensionen liegen innerhalb der konfigurierten Toleranz (`metric_tolerance_multiplier` oder `twin_epsilon_default`). (DT10-F-04) |
| SL-SIG-6 | Operativer Fehler auf integrity_dim → validity=COMPROMISED. |
| SL-SIG-7 | Constraint-Verletzung ohne Erwartung → ⬜ CONSTRAINT_NEAR_MISS. |
| SL-SIG-7a | Overfitting: Overfitting (z. B. `train_val_gap > threshold` in einem ObjectiveFamily-Constraint) wird als `CONSTRAINT_NEAR_MISS` (SL-SIG-7) behandelt: ⬜ Signal, kein 🟨 CONTRADICTION. Erst wenn der Constraint wiederholt verletzt wird, erzeugt der Kartograph eine `MetricConstraint`-Fracture. „Wiederholt" bedeutet: ≥ `min_confirmations` (=2, RESEARCH-besetzt) parameter-äquivalente Kristalle mit derselben Constraint-Verletzung innerhalb von `conflict_window_cycles` (=10). (BF-10, BF-17) |
| SL-SIG-8 | `negative_knowledge_decay` für erfolglos abgedeckte Regionen. |
| SL-HYP-4 | Erwartungs-Brücke: Bestätigende Hypothesen müssen ExpectationSpec tragen. `require_atlas_grounding` ist RESEARCH-besetzt: in BOOTSTRAP/EXPLORATION ist De-novo (atlas_refs=[]) erlaubt, in EXPLOITATION/SATURATION nicht. |

<!-- @section id="12" title="Manifest-Enforcement" type="prose" -->
### §12 Manifest-Enforcement (SL-MAN)

<!-- @table schema="manifest_enforcement_chain" -->
| Stufe | Ort | Aktion |
|-------|-----|--------|
| 1 | Manifest.hard_constraints | Mensch definiert |
| 2 | SL-BOOT-3 | Materialisierung |
| 3 | Atlas | ExclusionConstraint/SafetyConstraint |
| 4 | FrontierEngine | Hartfilter Nr.10 |
| 5 | Pre-Filter | Prüfung |
| 6 | Quartiermeister SL-MAN-4 | parameter_bounds ∩ Constraints |
| 7 | PolicyEvaluator | Prüfung 9 |

<!-- @table schema="manifest_rules" -->
| ID | Regel |
|----|-------|
| SL-MAN-7 | Semantische Umgehungsabwehr: neue kategorische Werte nicht in ManifestConstraint.categories → Constraint-Verstoß. |

<!-- @section id="13" title="Safety-Reaktionskette" type="prose" -->
### §13 Safety-Reaktionskette (SL-SAF, Quarantäne)

<!-- @table schema="safety_response_rules" -->
| ID | Regel |
|----|-------|
| SL-SAF-1..4 | ESTOP-Kette: HAL meldet ESTOP → Questor SAFETY-Abbruch (SR-19) → Archivar SAFETY-Governance-Ereignis → Kanzler ereignisgesteuert SOFORT: Zone→LOCKED, SafetyConstraint-Vorschlag, URGENT-Briefing, Eskalation(SAFETY_EVENT), Achsen-Transition safety→ESTOP_LOCKED (§29). |
| SL-SAF-2c | Globales ESTOP → Zonen-Mapping: Zonen mit in-flight-Paketen + Ursprungs-Slot-Zone → LOCKED; übrige → INTERLOCKED bis HAL-Gesundcheck. |
| SL-SAF-4 erweitert | ESTOP-/Reset-Begriffsprüfung rekursiv über canonical-geflattete parameters. |
| SL-SAF-5 | Entsperrpfad: LOCKED ausschließlich über strukturierte HumanResponseFile.unlock_decision. Zustandsfolge LOCKED → DIAGNOSTIC_ONLY → RELEASED. |
| SL-SAF-6 | SafetyConstraint-Aktivierung: Vorschlag gilt sofort als active=provisional; menschliche Bestätigung macht permanent. |
| SL-SAF-7 | SAFE_MODE-Exit-Pfad: (BF-01) Der Übergang `safety: SAFE_MODE → NORMAL` erfolgt ausschließlich durch eine `HumanResponseFile.unlock_decision` mit `scope_refs = ["GLOBAL_SAFETY"]` gemäß SL-SAF-5. Kein automatischer Übergang. Kein LLM-Pfad. Der Kanzler validiert die Freigabe und löst den atomaren Achsen-Transition aus. CT-9 (§34.2) erzwingt die Governance-Rückkehr. |

<!-- @section id="13.6" title="Quarantäne" type="state-machine" machine="quarantine_state" -->
#### §13.6 Quarantäne

<!-- @table schema="state_transitions" machine="quarantine_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| ENTRY | DIAGNOSTIC_ALLOWED | Diagnose-Budget vorhanden |
| DIAGNOSTIC_ALLOWED | QUARANTINE_EXIT | Diagnose erfolgreich abgeschlossen |
| QUARANTINE_EXIT | RESUME | Menschliche Freigabe |
| QUARANTINE_EXIT | CLOSE | Abschluss/Archivierung |

Diagnostik erlaubt und budgetiert. Blockierte Ideen emittieren QUARANTINE_BLOCK. Exit nur über strukturierte QUARANTINE_EXIT-Antwort. Sicherheitsrelevanz-Regel: Fracture ist sicherheitsrelevant genau dann, wenn seine Zone eine SafetyConstraint- oder SAFETY-Enforcement-Dimension schneidet.

<!-- @section id="14" title="Digital-Twin-Loop (strategisch)" type="dataflow" dataflow="digital_twin_strategic_loop" -->
### §14 Digital-Twin-Loop (SL-TWIN)

<!-- @dataflow id="digital_twin_strategic_loop" trigger="TWIN_DIVERGENCE_REPORT" source_role="kartograph" target_role="kanzler" -->
<!-- @ref target="specs/GREMIUM.md §6.14" type="spec" -->
<!-- @ref target="foundation/CONTRACTS.md §6.10.19" type="contract" -->
<!-- @ref target="foundation/CONTRACTS.md §6.10.20" type="contract" -->

<!-- @table schema="twin_strategic_rules" -->
| ID | Regel |
|----|-------|
| SL-TWIN-1 | Paarung: erfordert objective_family_ref + digital_twin_ref + Parameter-Äquivalenz. Nicht-äquivalente werden nicht gepaart. |
| SL-TWIN-2 | Deviation: `dev_metric = max(abs(sim−real)/max(abs(real), twin_epsilon_default), abs(sim−real)/abs_tolerance_metric)`. `abs_tolerance_metric = MetricDefinition.tolerance` falls gesetzt, sonst `twin_abs_tolerance_default`. Für real ≈ 0 gilt ausschließlich der Absolutterm. |
| SL-TWIN-3 | Validitätsprüfung: digital_twin_ref gesetzt UND drift_score > threshold UND objective_type ≠ DIAGNOSE → VETO(TWIN_DEGRADED). |
| SL-TWIN-4 | Gate×Security-Mode-Matrix: physisches Kalibrierungs-Paket konstruktionsunmöglich (SANDBOX erzwungen). |
| SL-TWIN-5 | Schatten-Variablen-Check: bei TWIN_DRIFT zwingend Umgebungs-Dimensionen im Vordenker-Prompt. |
| SL-TWIN-6..7 | Dedup/Deadlock-Freiheit: blocked_cache (twin_ref, zyklus); SANDBOX-Kalibrierung bleibt erlaubt. |
| SL-TWIN-8 | Konfidenz-Kalibrierung: rollierender vordenker_calibration_score; bei < calibration_alert_threshold DecisionOption. |
| SL-TWIN-9 | Kalibrierungs-Abbruch: nach twin_calibration_max_attempts (=3) ohne Drift-Reduktion ≥ twin_drift_reduction_min → SUSPENDED + Eskalation(TWIN_UNCALIBRATABLE). |
| SL-TWIN-10 | In-flight bei Drift: twin_invalidated=true im Briefing. |
| SL-TWIN-11 | Late-Pairing: nach TTL weitere twin_late_pairing_window_cycles nachpaarbar. |

<!-- @section id="15" title="Dimensions-Lebenszyklus" type="prose" -->
### §15 Dimensions-Lebenszyklus (SL-DIM)

<!-- @table schema="dimension_lifecycle_rules" -->
| ID | Regel |
|----|-------|
| SL-DIM-1..4 | Kanzler-Prüfung: Plausibilität, Range-Validierung, Cooldown (max_dimension_requests_per_topic_per_cycle), physische Auswirkung (requires_physical_actuation=true → zwingend ESCALATED). CT-4 (§34.2) erzwingt governance → AWAITING_HUMAN. |
| SL-DIM-5 | Deadlock-Freiheit: Ideen mit approved=false-Dimension werden nicht still verworfen → SymptomEvent(DIMENSION_GAP) + DecisionOption. |
| SL-DIM-6..7 | Genehmigung/Backfill: erzeugt TypedDimension(approved=false); optional BACKFILL_FRONTIER. |
| SL-DIM-8 | Abgeleitete Dimensionen: parent_dimension-Referenz. |
| SL-DIM-9 | CATEGORY_EXTENSION: neue Kategoriewerte → leichter Request. |
| SL-DIM-10 | requires_physical_actuation: jede Hardware-/Aktuierungsänderung außerhalb registrierter Capability-Parameter. |
| SL-DIM-11 | Lebenszeit-Limit: max_dimension_requests_per_topic_total + Wiederholungs-Erkennung über proposed_dimension_id. |
| SL-DIM-12 | Request-Outcomes: dimension_request_outcomes im Briefing. |
| SL-DIM-13 | Range-Korrekturen: Feedback-Symptom an Vordenker. |
| SL-DIR-7 | RequestSource-Union statt SymptomType-Zwang. |

<!-- @section id="16" title="Capability-Gap und CAPEX" type="prose" -->
### §16 Capability-Gap & CAPEX (SL-ESC-7)

<!-- @table schema="capability_gap_flow" -->
| Stufe | Komponente | Aktion |
|-------|-----------|--------|
| 1 | VORDENKER | ScientificHypothesis mit required_capabilities (Pflicht) |
| 2 | LOTSE | prüft gegen Capability-Registry |
| 3a | LOTSE (erfüllt) | → Wegmarke |
| 3b | LOTSE (unerfüllbar) | → CapabilityGapSignal |
| 4 | KANZLER | blocked_cache CAPABILITY_GAP |
| 5 | KANZLER | nach capability_gap_repeat_limit Wiederholungen: DecisionOption (bei requires_budget_or_hardware → CAPEX-Eskalation) |
| 6 | KANZLER | SL-ESC-7: CAPEX-Wartezeit → Eskalation(CAPABILITY_DELIVERY) mit Lieferdatum; blocked_cache-Clearing-Pfad → Achsen-Transition resource→PHYSICAL_WAIT (§29) |

<!-- @section id="17" title="Mensch-Schnittstelle" type="prose" -->
### §17 Mensch-Schnittstelle (SL-ESC)

<!-- @table schema="human_interface_rules" -->
| ID | Regel |
|----|-------|
| SL-ESC-1..4 | Eskalationskanal dateibasiert (`data/archiv/operational/escalations/`); Antworten in `data/human_inbox/`. Unbeantwortete Eskalation → nach timeout_cycles → governance→AWAITING_HUMAN. Erinnerungen alle escalation_reminder_interval_cycles (max escalation_reminder_cap). |
| SL-ESC-5 | HumanResponseFile-Validierung: Antwortdateien müssen gegen das Schema validieren. Unparsbar → PARSE_REJECTED + Erinnerungs-Template. |
| SL-ESC-6 | EscalationType-Erweiterung + Dedup: HUMAN_ESCALATION erhält Pflicht-Parameter escalation_category. Dedup über (escalation_type, target_ref). |

<!-- @section id="18" title="Briefing-Erzeugung" type="prose" -->
### §18 Briefing-Erzeugung (SL-BRF)

<!-- @table schema="briefing_rules" -->
| ID | Regel |
|----|-------|
| SL-BRF-1..6 | Sanitization: Verboten: security_mode, Hybrid-Referenzen, Roh-metric_vector. Fortschritt als deterministische Skalare. Quarantäne → [REDACTED:QUARANTINE]. |
| SL-BRF-4 | Trunkierungspriorität v2: URGENT-Auslöser + SAFETY > LOCKED/CRITICAL/QUARANTINE + drifted Twins + pending_escalations + decisions_required > höchste Fractures > aktive Topics > Rest. Twins mit calibration_required oder drift_score > 0 fallen nie in die Restklasse. |
| SL-BRF-8 | Gesamt-Kontext-Budget: max_total_context_chars = manifest_max_chars + max_briefing_chars + anchor_max_chars. Layer 3 (Anchor) wird nie trunkiert. |
| SL-BRF-10 | Briefing exponiert active_hypothesis_refs (Top-N). |

<!-- @section id="19" title="Sanitization" type="prose" -->
### §19 Sanitization (SL-SAN)

<!-- @table schema="sanitization_rules_strategic" -->
| ID | Regel |
|----|-------|
| SL-SAN-0 | First-Order-Scan: aller LLM-Outputs vor Persistenz. Treffer → Quarantäne + Audit + einmalige Neu-Generierung, danach Eskalation. |
| SL-SAN-1 | Archivar-Eingangssanitization: Freitextfelder eingehender questor_ergebnis_paket werden gescannt (INJ-01..15, XML-Escaping). |
| SL-SAN-2 | Second-Order-Scan: persistierte LLM-Texte beim Wiedereinspeisen erneut gescannt. Treffer → Quarantäne, Platzhalter, Audit, DecisionOption. |
| SL-SAN-5 | INJ-01..15 und Safety-Claim-Katalog als normativer Anhang. |
| SL-SAN-6 | Roh-Ergebnis-Trennung: observation_raw (quarantänefähig) und interpretation (niemals Erwartungsquelle). |
| SL-RPT-1 | Zitiermuster-Entfernung: deterministisch über Regex-Katalog; nicht erfassbare Fälle als review_required. |

<!-- @section id="20" title="Abschluss und Archivierung" type="dataflow" dataflow="mission_archive" -->
### §20 Abschluss und Archivierung (SL-RPT)

<!-- @dataflow id="mission_archive" trigger="STOP_CONDITION_REACHED" source_role="kanzler" target_role="archiv" -->
<!-- @dataflow-step order="1" -->
StopCondition REACHED → Topic SATURATED → FINAL-Briefing

<!-- @dataflow-step order="2" -->
→ Kanzler injiziert ReportFacts (deterministisch)

<!-- @dataflow-step order="3" -->
→ Königin-LLM: NUR executive_summary + future_recommendations

<!-- @dataflow-step order="4" -->
→ Kanzler: Sanitization + Zitierungs-Check

<!-- @dataflow-step order="5" -->
→ Mensch: human_reviewed = true → ARCHIVED → Cold Storage

<!-- @table schema="archive_rules" -->
| ID | Regel |
|----|-------|
| SL-RPT-2 | Fakten-Trennung: harte Fakten ausschließlich aus ReportFacts. |
| SL-RPT-3..4 | Unreviewed-Reminder alle review_reminder_interval_cycles. Nach review_grace_max_cycles finale Eskalation. Nach cold_storage_window_days mit human_reviewed=true → Cold Storage. |

<!-- @section id="21" title="Replikation" type="prose" -->
### §21 Replikation (SL-REP)

<!-- @table schema="replication_rules" -->
| ID | Regel |
|----|-------|
| SL-REP-1 | FrontierType um REPLICATE erweitert. |
| SL-REP-2 | REPLICATE-Frontiers bei crystallization_progress ≥ replication_trigger_progress und Bestätigungen < min_confirmations (RESEARCH-besetzt). Relevante Bestätigung: parameter-äquivalenter Kristall, gleiche ObjectiveFamily, ziel_erreicht=true. „Parameter-äquivalent" bedeutet: Alle Diskrepanzen in kontinuierlichen Dimensionen liegen innerhalb der konfigurierten Toleranz (`metric_tolerance_multiplier` oder `twin_epsilon_default`). (DT10-F-04) |
| SL-REP-3 | FrontierEngine gewichtet REPLICATE mit replication_weight. |
| SL-REP-4 | Quotenregel: ≥ 1 Replikation pro replication_cadence_cycles. |
| SL-REP-5 | Fracture-getriebene Replikation: FRACTURE_GAP mit ≥ 2 divergenten Kristallen → REPLICATE-DecisionOption. |

<!-- @section id="22" title="Datenintegrität" type="prose" -->
### §22 Datenintegrität (SL-INT)

<!-- @table schema="integrity_rules" -->
| ID | Regel |
|----|-------|
| SL-INT-1 | NaN: Kristall verworfen, gültige Geschwister bleiben. Gilt auch für SymptomEvent.metrics_snapshot. |
| SL-INT-2 | Sequenzlücken: akzeptiert + Audit-Flag + Reconciliation (Owner, Timeout, Abschlusszustand). |
| SL-INT-3 | Referentielle Integrität: briefing_ref, source_ref, twin_divergence_report_ref müssen existieren. |
| SL-INT-4 | Idempotenz: directive_id gemäß SL-DIR-1. |
| SL-INT-6 | Registry-Index: Dateien je Verzeichnis für Existenzprüfungen. |

<!-- @section id="23" title="Zyklus-, Zeit- und Budgetmodell" type="prose" -->
### §23 Zyklus-, Zeit- und Budgetmodell (SL-BUD, SL-URG)

<!-- @table schema="budget_rules" -->
| ID | Regel |
|----|-------|
| SL-BUD-1 | `used_cycles += 1 × resource.burn_rate_multiplier`. In PHYSICAL_WAIT/BUDGET_EXHAUSTED ist burn_rate_multiplier=0 → Budget brennt nicht. (Achsen-Integration: ResourceAxis besitzt burn_rate_multiplier.) |
| SL-BUD-1a | (BF-04) Mission-Budget-Erschöpfung (`resource=BUDGET_EXHAUSTED`) beeinflusst keine laufenden Questor-Pakete. Diese werden ausschließlich durch ihr eigenes `QuestorSpec.budget.max_duration_s` gesteuert (→ QUESTOR.md §11.5). Neue Pakete werden nicht mehr dispatched (`physical_dispatch_allowed=false`, ResourceAxis-Besitz §31). |
| SL-BUD-2 | remaining_cycles = total_cycles − used_cycles − reserved_cycles. |
| SL-BUD-3 | Bei UNLOCK_BUDGET-Bestätigung: reserved_cycles → used_cycles. |
| SL-BUD-4 | Formeln: burn_rate_per_cycle = used_cycles / max(elapsed_cycles, 1); estimated_completion_cycle = used_cycles + ceil(remaining_progress/progress_rate); progress_rate ≤ 0 → None |
| SL-URG-2 | BUDGET_EXHAUSTED: fällt remaining_cycles ≤ 0 oder unter budget_unlock_threshold_fraction → URGENT + Eskalation(BUDGET) + DecisionOption. Achsen-Transition: resource→BUDGET_EXHAUSTED, governance→AWAITING_HUMAN (via CT-1). |

<!-- @section id="24" title="Zustandsmaschinen" type="prose" -->
### §24 Zustandsmaschinen

<!-- @section id="24.1" title="Topic" type="state-machine" machine="topic_state" -->
#### §24.1 Topic

<!-- @table schema="state_transitions" machine="topic_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| PROPOSED | ACTIVE | Kanzler-Freigabe (via DTT INITIAL_SWEEP) |
| ACTIVE | SATURATED | StopCondition REACHED |
| ACTIVE | ABORTED | Menschlicher Abbruch |
| SATURATED | ARCHIVED | FINAL-Briefing + human_reviewed |
| ABORTED | ARCHIVED | Lessons-Learned-Transfer |

Alle Übergänge vom Kanzler. Lessons-Learned-Transfer bei jedem ACTIVE-Abschluss.

<!-- @section id="24.2" title="DimensionOnboardingRequest" type="state-machine" machine="dimension_request_state" -->
#### §24.2 DimensionOnboardingRequest

<!-- @table schema="state_transitions" machine="dimension_request_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| PROPOSED | APPROVED | Kanzler-Prüfung bestanden |
| PROPOSED | REJECTED | Kanzler-Prüfung fehlgeschlagen |
| PROPOSED | ESCALATED | requires_physical_actuation=true |
| PROPOSED | COOLDOWN | Cooldown aktiv |
| ESCALATED | APPROVED | Menschliche Genehmigung |
| ESCALATED | REJECTED | Menschliche Ablehnung |

<!-- @section id="24.3" title="Eskalation" type="state-machine" machine="escalation_state" -->
#### §24.3 Eskalation

<!-- @table schema="state_transitions" machine="escalation_state" -->
| Von | Nach | Auslöser |
|-----|------|----------|
| PENDING | ANSWERED | Menschliche Antwort |
| PENDING | TIMED_OUT | timeout_cycles erreicht |
| TIMED_OUT | (governance→AWAITING_HUMAN) | Automatisch |
| ANSWERED | (Umsetzung → RoyalLog) | DTT |

<!-- @section id="24.4" title="SystemMode zu Achsen" type="prose" -->
#### §24.4 SystemMode → Achsen (DESIGN)

<!-- @table schema="system_mode_mapping" -->
| SystemMode | Achsen-Änderung |
|-----------|----------------|
| SAFE_MODE | safety=SAFE_MODE |
| HOLD_STRATEGY | governance=AWAITING_HUMAN |
| ESTOP | safety=ESTOP_LOCKED |

Der einzelne SystemMode wird nicht als parallele Maschine geführt.

<!-- @section id="24.5" title="Speicherorte" type="prose" -->
#### §24.5 Speicherorte (Blackboard-konform)

<!-- @table schema="storage_locations" -->
| Artefakt | Ort |
|----------|-----|
| ResearchManifest | data/governance/manifests/ |
| StrategicBriefing | data/governance/briefings/ |
| StrategicDirective | data/governance/directives/ |
| MissionBudget | data/governance/budget/ |
| DimensionOnboardingRequest | data/governance/dimension_requests/ |
| RoyalLog | data/archiv/operational/royal_log/ |
| SymptomEvent, CapabilityGapSignal | data/archiv/operational/events/ |
| ScientificHypothesis | data/archiv/ideen/ |
| HumanEscalationRecord | data/archiv/operational/escalations/ |
| Menschliche Antworten | data/human_inbox/ |
| ControlStateLog | data/governance/control_state/ |
| Registries | data/governance/registries/ |
| blocked_cache | data/governance/cache/ |

<!-- @section id="25" title="Autonomie- und Eskalationsmatrix" type="prose" -->
### §25 Autonomie- und Eskalationsmatrix

<!-- @table schema="autonomy_matrix" -->
| Entscheidung | Königin | Kanzler | Nur Mensch |
|-------------|---------|---------|-----------|
| Exploration gewichten | vorschlagen | final | überstimmen |
| Topic archivieren | vorschlagen | final | überstimmen |
| Budget unter Threshold | vorschlagen | final | überstimmen |
| Budget über Threshold / UNLOCK_BUDGET | vorschlagen | eskalieren | final |
| Neue nicht-physische Dimension | Hint | genehmigen | überstimmen |
| Neue physische Dimension | Hint | eskalieren | final |
| CAPEX / Hardware-Kauf | DecisionOption anregen | eskalieren | final |
| Mission abbrechen | vorschlagen | eskalieren | final bestätigen |
| ESTOP/Interlock zurücksetzen | ❌ niemals | ❌ | ✅ autorisierter Sicherheitsprozess |
| Manifest-hard_constraints | ❌ | ❌ | ✅ (neue Version) |
| Twin-Kalibrierung anweisen | ✅ (CALIBRATE_TWIN) | prüfen + umsetzen | überstimmen |
| SafetyConstraint aufheben | ❌ | nur autorisiert | ✅ |
| ResearchPhase setzen | ✅ (SET_RESEARCH_PHASE) | prüfen + umsetzen | überstimmen (HumanDirective.set_research_phase) |

<!-- @section id="26" title="CHARTER-Konformitätsmatrix" type="prose" -->
### §26 CHARTER-Konformitätsmatrix

<!-- @table schema="charter_compliance" -->
| CHARTER-Regel | Umsetzung |
|---------------|-----------|
| SR-04 | Questor/HAL unverändert; strategische Verträge nur auf Gremium-Ebene |
| SR-08 | RoyalLog/Briefings/Direktiven operational; HardwareHealth verzerrt keine Metriken (SL-SIG-2) |
| SR-10 | Ungültige Direktive → VETO; unklarer DimensionRequest → REJECTED; LLM-Ausfall → Policy bleibt; NaN → Verwurf |
| SR-11 | Mensch nie überstimmt; ABORT, physische Dimensionen, CAPEX, Manifest immer menschlich |
| SR-13 | Königin/Vordenker schlagen vor; Kanzler, Pre-Filter, Gate entscheiden deterministisch |
| SR-14 | NaN-Fail-Closed auf Schicht 4 (SL-INT-1) |
| SR-24 | Briefing-Whitelist; Fortschritt als Skalare |
| SR-29 | security_mode in keinem strategischen Artefakt |
| SR-05 | ESTOP-Reset im Intent-Enum nicht ausdrückbar (SL-SAF-4) |
| §2 Blackboard | Alle Kommunikation über definierte Speicherorte (§24.5) |

<!-- @section id="27" title="Verbotene Patterns" type="prose" -->
### §27 Verbotene Patterns (Strategic Layer)

<!-- @table schema="forbidden_patterns_strategic" -->
| # | Pattern |
|---|---------|
| 1 | Königin-LLM mit persistentem Gesprächsverlauf. |
| 2 | Freitext-Report als primärer LLM-Input (nur strukturierte Briefings). |
| 3 | LLM-Einsatz im Kanzler (auch keine LLM-Zusammenfassungen). |
| 4 | Direkter Atlas-/Archiv-Zugriff der Königin. |
| 5 | Direkte Kommunikation Königin ↔ Vordenker. |
| 6 | Automatische Dimensions-Erzeugung ohne Kanzler-Prüfung. |
| 7 | security_mode oder Atlas-Hybrid-Referenzen im LLM-Kontext. |
| 8 | RoyalLog-Inhalte als wissenschaftliche Signale. |
| 9 | Sim-Evidenz, die physische Kristalle direkt bestätigt. |
| 10 | Physische Kalibrierungs-Pakete (SL-TWIN-4). |
| 11 | Explorations-Fehlschläge als 🟨 CONTRADICTION (SL-SIG-1). |
| 12 | Weiterlauf mit offener Eskalation nach Timeout (governance=AWAITING_HUMAN). |
| 13 | CHARTER-Änderung als Voraussetzung dieses Dokuments. |
| 14 | Achsen-Parameter direkt setzen statt über ControlState lesen (Single Ownership, §31). |

<!-- @section id="28" title="Testsuite" type="prose" -->
### §28 Testsuite (STRAT-01..55)

<!-- @table schema="test_overview" -->
| Bereich | Test-Präfix | Anzahl | Zweck |
|---------|------------|--------|-------|
| Verträge | STRAT-CTR | ~20 | Pydantic-Validierung |
| Achsen & ControlState | STRAT-AX | ~40 | Achsen-Zustandsmaschine, SL-AX-ATOMIC |
| Kanzler & DTT | STRAT-KANZ | ~55 | Validierungspipeline, DTT, Blocklists |
| Königin & Briefing | STRAT-KOEN | ~25 | Constitutional Anchor, Briefing |
| Symptom-Trigger & Signal | STRAT-SYM | ~15 | SymptomEvents, Signal-Semantik |
| End-to-End | STRAT-E2E | ~15 | Vollständiger Zyklus |
| Gesamt | | ~170 | |

<!-- @ref target="ops/VALIDATION.md §4.7" type="spec" -->
→ Siehe `ops/VALIDATION.md §4.7` für die vollständige Test-Spezifikation.

<!-- @section id="29" title="MODUL CONTROL (4-Achsen-Steuerung, DESIGN)" type="prose" -->
## MODUL CONTROL (4-Achsen-Steuerung, DESIGN)

<!-- @section id="29" title="Achsen-Definition" type="prose" -->
### §29 Achsen-Definition

<!-- @table schema="axis_definitions" -->
| Achse | Werte | Treiber | Absolutheit |
|-------|-------|---------|------------|
| SafetyAxis | NORMAL / SAFE_MODE / ESTOP_LOCKED | HAL-Ereignis, Mensch | Absolut |
| ResourceAxis | FUNDED / INCUBATING / PHYSICAL_WAIT / BUDGET_EXHAUSTED | Budgetzähler, Liefer-/Capability-Signal, in-flight | Hoch |
| ResearchAxis | BOOTSTRAP / EXPLORATION / EXPLOITATION / SATURATION | Atlas-Metriken | Normal |
| GovernanceAxis | AUTONOMOUS / AWAITING_HUMAN / CONFLICT_LOCK | Eskalationsstatus, Konfliktdetektor | Normal |

Der Gesamtzustand ist das Tupel `(safety, resource, research, governance)`. Jede Achse wird unabhängig aktualisiert; ein „Phasenwechsel" ist eine Änderung einer Achse, nicht des ganzen Tupels.

<!-- @section id="30" title="Kompositionsregeln" type="prose" -->
### §30 Kompositionsregeln (Validitätsmatrix)

<!-- @table schema="composition_rules" -->
| ID | Regel |
|----|-------|
| §30.1 | Orthogonalität: Achsen komponieren; kein Override. |
| §30.2 | Validitätsmatrix (ungültige Kombinationen): safety=ESTOP_LOCKED + resource=INCUBATING; safety=SAFE_MODE + research=BOOTSTRAP; resource=BUDGET_EXHAUSTED + governance=AUTONOMOUS. |
| §30.3 | Priorität: Safety ist absolut. Andere Gates multiplikativ. |
| §30.4 | Keine Hierarchie zwischen Achsen: Konflikte werden durch Single Ownership (§31) aufgelöst, nicht durch Rangfolge. |
| §30.5 | Quarantäne und ResearchAxis: (BF-09) Quarantäne (`quarantine_mode=true` auf allen aktiven Topics) ändert die ResearchAxis nicht. Sie blockiert nur normalen Dispatch. Die ResearchAxis bleibt in ihrem aktuellen Zustand, solange `diagnostic_budget > 0` ist. Bei `diagnostic_budget == 0` und Quarantäne: URGENT-Trigger (SL-URG-1). |

<!-- @section id="31" title="Parameter-Besitz-Matrix" type="prose" -->
### §31 Parameter-Besitz-Matrix (Single Ownership)

<!-- @table schema="parameter_ownership" -->
| Achse | Besetzte Parameter |
|-------|-------------------|
| ResearchAxis | exploration_weight, exploitation_weight, require_atlas_grounding, replicate_divergence_check, metric_tolerance_multiplier, replication_weight, min_confirmations |
| ResourceAxis | burn_rate_multiplier, physical_dispatch_allowed, escalation_timeout_multiplier |
| GovernanceAxis | stall_detection_active |
| SafetyAxis | safety_dispatch_allowed, safety_intent_blocklist (berechnete Gates) |

Regeln lesen diese Parameter über den ControlState; sie setzen sie NICHT direkt. Verstöße → SL-DEP-Lint Build-Fail.

<!-- @section id="32" title="Intent-Verfügbarkeit" type="prose" -->
### §32 Intent-Verfügbarkeit

```
verfügbare_Intents = alle_Intents
                     − safety_intent_blocklist
                     − resource_intent_blocklist
                     − governance_intent_blocklist
                     − research_intent_blocklist
```

<!-- @section id="32.1" title="safety_intent_blocklist" type="prose" -->
#### §32.1 safety_intent_blocklist (explizite Definition, BF-06)

Bei `safety=ESTOP_LOCKED`: alle Intents außer `{NO_ACTION, HUMAN_ESCALATION}`.

Bei `safety=SAFE_MODE`: `{PIVOT_DOMAIN, PIVOT_TARGET, UNLOCK_BUDGET, ADD_DIMENSION_HINT, SET_RESEARCH_PHASE, INCREASE_DIAGNOSTIC, CALIBRATE_TWIN, ARCHIVE_TOPIC, SET_PRIORITY, DROP_SOFT_PREFERENCE, ABORT_MISSION, INITIAL_SWEEP}`.

Erlaubt bei `safety=SAFE_MODE`: `{NO_ACTION, HUMAN_ESCALATION}`.

Quarantäne-Diagnostik-Ausnahme (BF-15): `INCREASE_DIAGNOSTIC` wird aus der `safety_intent_blocklist` bei `safety=SAFE_MODE` entfernt, wenn die Zielzone (`zone_ref` aus den Intent-Parametern) `quarantine_mode=true` hat (§13.6: „Diagnostik erlaubt und budgetiert"). In diesem Fall ist `INCREASE_DIAGNOSTIC` erlaubt, aber nur mit `amount ≤ diagnostic_budget_default` (=3) und nur für die quarantinierte Zone. Alle anderen Blocklist-Einträge bleiben unverändert.

<!-- @section id="32.2" title="resource_intent_blocklist" type="prose" -->
#### §32.2 resource_intent_blocklist (explizite Definition, BF-06)

Bei `resource=BUDGET_EXHAUSTED`: `{INITIAL_SWEEP, PIVOT_DOMAIN, PIVOT_TARGET, ADD_DIMENSION_HINT, INCREASE_DIAGNOSTIC, CALIBRATE_TWIN, SET_RESEARCH_PHASE, SET_PRIORITY}`.

Erlaubt bei `resource=BUDGET_EXHAUSTED`: `{NO_ACTION, UNLOCK_BUDGET, HUMAN_ESCALATION, ABORT_MISSION, ARCHIVE_TOPIC, DROP_SOFT_PREFERENCE}`.

<!-- @section id="32.3" title="Intent-Sonderregeln" type="prose" -->
#### §32.3 Intent-Sonderregeln

`UNLOCK_BUDGET` ist nur verfügbar, wenn `resource=BUDGET_EXHAUSTED`.

`SET_RESEARCH_PHASE` ist verfügbar, wenn keine Safety-/Governance-Sperre vorliegt und `resource ∈ {FUNDED, INCUBATING}`. Bei `resource=BUDGET_EXHAUSTED` oder `resource=PHYSICAL_WAIT` ist `SET_RESEARCH_PHASE` blockiert (Teil der `resource_intent_blocklist`). (BF-07)

<!-- @section id="33" title="Transitionen und Liveness" type="prose" -->
### §33 Transitionen & Liveness

Der Kanzler wertet Achsen-Transitionen bei jedem Strategie-Zyklus aus; Safety/Resource sind ereignisgesteuert (lösen sofort einen atomaren Auswertungszyklus aus, §34).

Liveness-Watchdog: global; wenn (now − letzter Strategie-Zyklus) > liveness_watchdog_hours → Heartbeat-Zyklus (nur Achsen-Auswertung, kein Briefing).

compute_phase_label(state): abgeleitetes Etikett, z. B. „EXPLOITATION + PHYSICAL_WAIT + CRISIS". Nicht authoritativ.

<!-- @section id="34" title="SL-AX-ATOMIC" type="dataflow" dataflow="axiom_transition" -->
### §34 SL-AX-ATOMIC: Atomare Achsen-Auswertung

<!-- @dataflow id="axiom_transition" trigger="ACHSEN_EREIGNIS" source_role="kanzler" target_role="control_state_log" -->
Alle Achsen-Transitionen werden atomar ausgewertet. Kein Zwischenzustand wird persistiert. (Behebt DT7-F-01 / K6-F-12.)

Algorithmus (feste Reihenfolge):

<!-- @dataflow-step order="1" -->
1. SAMMELN: alle im Auswertungszeitpunkt ausgelösten Transitionen in `direct_transitions` als (axis, from_value, to_value, timestamp).

<!-- @dataflow-step order="2" -->
2. KONFLIKT-ERKENNUNG: mehrere Ereignisse auf derselben Achse → schwerwiegendster Zielwert gewinnt (§34.1); unterlegene als SUPERSEDED verworfen.

<!-- @dataflow-step order="3" -->
3. ABSCHLUSS (Closure): Closure-Regeln (§34.2) iterativ anwenden, max closure_max_iterations (=5). Erzwungene Transitionen werden hinzugefügt.

<!-- @dataflow-step order="4" -->
4. VALIDIERUNG: finaler Ziel-Tupel gegen §30.2. Gültig → Commit. Ungültig trotz Closure → gesamte Transition VERWORFEN, ControlState unverändert, Audit + Eskalation(STRATEGIC_QUESTION) (fail-closed).

<!-- @dataflow-step order="5" -->
5. ATOMARER COMMIT: alle Transitionen des Batches in einer Operation, oder keine.

<!-- @dataflow-step order="6" -->
6. LOGGING: alle Transitionen eines Commits als ein Batch mit gemeinsamer batch_id.

<!-- @section id="34.1" title="Severity-Ordnung" type="prose" -->
#### §34.1 Severity-Ordnung (DESIGN-FESTLEGUNG)

Achsen-Priorität: SAFETY > RESOURCE > GOVERNANCE > RESEARCH.

<!-- @table schema="severity_order" -->
| Achse | Severity-Ordnung (schwer → leicht) |
|-------|-----------------------------------|
| SafetyAxis | ESTOP_LOCKED > SAFE_MODE > NORMAL |
| ResourceAxis | BUDGET_EXHAUSTED > PHYSICAL_WAIT > INCUBATING > FUNDED |
| GovernanceAxis | CONFLICT_LOCK > AWAITING_HUMAN > AUTONOMOUS |
| ResearchAxis | kein Severity-Begriff; bei Konflikt → Audit + Eskalation |

Bei gleicher Achse und Severity entscheidet der früheste TimeService-Zeitstempel.

<!-- @section id="34.2" title="Closure-Regeln" type="prose" -->
#### §34.2 Closure-Regeln (CT-1..CT-10)

<!-- @table schema="closure_rules" -->
| ID | Auslöser | Erzwungene Folge | Begründung | Quelle |
|----|----------|-----------------|-----------|--------|
| CT-1 | resource → BUDGET_EXHAUSTED | governance → AWAITING_HUMAN | §30.2 | v1.0.0 |
| CT-2 | safety → ESTOP_LOCKED ∧ resource=INCUBATING | resource verlässt INCUBATING (→ FUNDED, sofern kein schwererer Zielwert) | §30.2; in-flight abgebrochen (SR-19) | v1.0.0 |
| CT-3 | safety → SAFE_MODE | research-Transitionen werden unterdrückt; bei gleichzeitigem Auftreten im selben Batch hat Safety Vorrang (§34.1) | SAFE pausiert Direktiven | v1.0.0 + BF-12 |
| CT-4 | DimensionOnboardingRequest.status → ESCALATED ∧ requires_physical_actuation=true | governance → AWAITING_HUMAN | Physische Dimensionen erfordern menschliche Freigabe (SL-DIM-4, SR-11) | BF-05 |
| CT-5 | resource → PHYSICAL_WAIT | governance → AWAITING_HUMAN | Physisches Warten (CAPEX, Lieferung) erfordert menschliche Entscheidung (SR-11) | BF-02 |
| CT-6 | safety → SAFE_MODE ∨ safety → ESTOP_LOCKED | governance → AWAITING_HUMAN | Sicherheitsereignisse erfordern immer menschliche Aufsicht (SR-11) | BF-03 |
| CT-7 | resource: BUDGET_EXHAUSTED → FUNDED durch UNLOCK_BUDGET-Genehmigung | governance: AWAITING_HUMAN → AUTONOMOUS (sofern keine andere Governance-Sperre aktiv) | Symmetrie zu CT-1; verhindert Steckenbleiben in AWAITING_HUMAN | BF-11 |
| CT-8 | resource: PHYSICAL_WAIT → FUNDED durch CAPEX-/Lieferfreigabe (HumanResponseFile mit decision=APPROVE und escalation_type ∈ {CAPEX, CAPABILITY_DELIVERY}) und Capability in Registry als ACTIVE registriert | governance: AWAITING_HUMAN → AUTONOMOUS (sofern keine andere Governance-Sperre aktiv) | Symmetrie zu CT-5; verhindert Steckenbleiben in AWAITING_HUMAN nach physischer Lieferung. DT10-F-03-Präzisierung: Der Übergang erfordert nicht nur die Budget-Freigabe, sondern das Clearing des blocked_cache (d.h. die Capability muss in der Registry als ACTIVE registriert sein). | BF-14 + DT10-F-03 |
| CT-9 | safety: SAFE_MODE → NORMAL durch SL-SAF-7 (HumanResponseFile.unlock_decision mit scope_refs=["GLOBAL_SAFETY"]) | governance: AWAITING_HUMAN → AUTONOMOUS (sofern keine andere Governance-Sperre aktiv: resource ≠ BUDGET_EXHAUSTED ∧ resource ≠ PHYSICAL_WAIT ∧ kein CONFLICT_LOCK) | Symmetrie zu CT-6; verhindert Steckenbleiben in AWAITING_HUMAN nach Sicherheitsfreigabe | BF-16 |
| CT-10 | safety: ESTOP_LOCKED → NORMAL durch autorisierten Sicherheitsprozess (SR-05) | governance: AWAITING_HUMAN → AUTONOMOUS (sofern keine andere Governance-Sperre aktiv) | Symmetrie zu CT-6 für ESTOP; verhindert Steckenbleiben in AWAITING_HUMAN nach ESTOP-Reset | DT10-F-01 |

SR-A: ist safety ∈ {SAFE_MODE, ESTOP_LOCKED}, werden alle pending ResearchAxis-Transitionen verworfen.

<!-- @section id="34.3" title="SL-CT-SIMULTAN" type="prose" -->
#### §34.3 SL-CT-SIMULTAN (Gleichzeitigkeit, BF-18)

Wenn mehrere CT-Regeln denselben Zielwert auf derselben Achse erzwingen (z. B. CT-5 und CT-6 erzwingen beide `governance → AWAITING_HUMAN`), gilt: kein Konflikt, nur eine Transition. Die Severity-Ordnung (§34.1) bestimmt den auslösenden Trigger für das Audit-Log. Bei unterschiedlichen Zielwerten auf derselben Achse: schwerster Zielwert gewinnt (§34.1).

<!-- @section id="34.4" title="Gearbeitetes Beispiel" type="prose" -->
#### §34.4 Gearbeitetes Beispiel (ESTOP + Budget-Schwelle)

Ausgang: safety=NORMAL, resource=INCUBATING, research=EXPLOITATION, governance=AUTONOMOUS

```
E1: ESTOP → safety: NORMAL→ESTOP_LOCKED
E2: Budget-Schwelle → resource: INCUBATING→BUDGET_EXHAUSTED

1. SAMMELN: [(safety,NORMAL,ESTOP_LOCKED,t1), (resource,INCUBATING,BUDGET_EXHAUSTED,t2)]
2. KONFLIKT: keine (verschiedene Achsen)
3. ABSCHLUSS:
   - CT-2: resource INCUBATING→FUNDED; kollidiert mit E2 (→BUDGET_EXHAUSTED);
     Severity: BUDGET_EXHAUSTED > FUNDED ⇒ BUDGET_EXHAUSTED gewinnt
   - CT-1: resource=BUDGET_EXHAUSTED ⇒ governance AUTONOMOUS→AWAITING_HUMAN
   - CT-6: safety=ESTOP_LOCKED ⇒ governance AUTONOMOUS→AWAITING_HUMAN
     → SL-CT-SIMULTAN: CT-1 und CT-6 fordern dasselbe Ziel → nur EINE Transition
   - SR-A: keine research-Transitionen
   Fixpunkt.
4. VALIDIERUNG: (ESTOP_LOCKED, BUDGET_EXHAUSTED, EXPLOITATION, AWAITING_HUMAN) → GÜLTIG
5. COMMIT: safety, resource, governance atomar
6. LOGGING: 1 Batch, 3 AxisTransition-Einträge
```

<!-- @section id="35" title="MODUL INDEX" type="prose" -->
## MODUL INDEX

<!-- @section id="35" title="Fund-Register" type="prose" -->
### §35 Fund-Register (Behebungsstatus)

<!-- @table schema="finding_register" -->
| Fund-Cluster | Behebungs-Abschnitt | Status |
|-------------|-------------------|--------|
| KV-01/KV-20 Mensch-Schnittstelle | §17, §18 (SL-BRF-9) | BEHOBEN |
| KV-02 Lessons-Learned | §8 (SL-DTT-1) | BEHOBEN |
| KV-03 Zyklus/Zeit/Budget | §23 (SL-BUD) | BEHOBEN |
| KV-04 Manifest-Intake | §6 (SL-BOOT-0) | BEHOBEN |
| KV-05 Intent-Parameter | §7 (Validierungspipeline) | BEHOBEN |
| KV-06/07/08 Twin | §14 (SL-TWIN) | BEHOBEN |
| KV-09 Schatten-Variablen | §6 (SL-BOOT-2) | BEHOBEN |
| KV-10 Replikation | §21 (SL-REP) | BEHOBEN |
| KV-11 HOLD/SAFE | §30/§31 (Achsen), §9 (SL-NOACT-2) | BEHOBEN |
| KV-12 In-flight-Pakete | CONTRACTS §6.11.4 (InFlightPackageSummary) | BEHOBEN |
| KV-13 Config-Lücken | CONTRACTS §6.11.11 (StrategicLayerConfig v2) | BEHOBEN |
| KV-14 Entsperr-/Exit-Pfade | §13 (SL-SAF-5, Quarantäne) | BEHOBEN |
| KV-15 Dedup | §9 (SL-INT-5) | BEHOBEN |
| KV-16 Tote Vertragsfelder | §8 (priority/keep_constraints gestrichen) | BEHOBEN |
| KV-17 First-Order-Scan | §19 (SL-SAN-0) | BEHOBEN |
| KV-18 NO_ACTION-Zwang | §9 (SL-CON-3) | BEHOBEN |
| KV-19 EscalationType | §6 Enums, §17 (SL-ESC-6) | BEHOBEN |
| KV-21 Initiale Zonen | §6 (SL-BOOT-2b) | BEHOBEN |
| KV-22 Erwartungs-Brücke | §11 (SL-HYP-4) | BEHOBEN |
| DT7-F-01 Simultane Achsen-Transitionen | §34 (SL-AX-ATOMIC) | BEHOBEN |
| DT8-F-01 Dimensions-Eskalation → AWAITING_HUMAN | §34.2 (CT-4) | BEHOBEN |
| DT8-F-02 PHYSICAL_WAIT → AWAITING_HUMAN | §34.2 (CT-5) | BEHOBEN |
| DT8-F-03 CAPEX in §41 | §8 (SL-DTT), §34.2 (CT-5/CT-6) | BEHOBEN |
| DT8-F-05 SAFETY → AWAITING_HUMAN | §34.2 (CT-6) | BEHOBEN |
| DT8-F-06 SAFE_MODE → NORMAL | §13 (SL-SAF-7) | BEHOBEN |
| DT8-F-07 safety_intent_blocklist | §32.1 | BEHOBEN |
| DT8-F-08 Quarantäne + Research-Achse | §30.5 | BEHOBEN |
| DT8-F-10 Overfitting | §11 (SL-SIG-7a) | BEHOBEN |
| DT8-F-11 Laufende Jobs bei Budget-Erschöpfung | §23 (SL-BUD-1a) | BEHOBEN |
| DT8-F-12 SET_RESEARCH_PHASE bei BUDGET_EXHAUSTED | §32.3 | BEHOBEN |
| DT8-F-13 CT-1 Umkehrung | §34.2 (CT-7) | BEHOBEN |
| DT9-F-01 PHYSICAL_WAIT → FUNDED Rückkehr | §34.2 (CT-8) | BEHOBEN |
| DT9-F-03 INCREASE_DIAGNOSTIC bei Quarantäne | §32.1 (Quarantäne-Diagnostik-Ausnahme) | BEHOBEN |
| DT9-F-04 SAFE_MODE → NORMAL Rückkehr | §34.2 (CT-9) | BEHOBEN |
| DT9-F-05 CT-Gleichzeitigkeit | §34.3 (SL-CT-SIMULTAN) | BEHOBEN |
| DT9-F-07 SL-SIG-7a Quantifizierung | §11 (SL-SIG-7a) | BEHOBEN |
| DT10-F-01 ESTOP_LOCKED → NORMAL Rückkehr | §34.2 (CT-10) | BEHOBEN |
| DT10-F-02 Terminologie zone_ref | §32.1 (BF-15) | BEHOBEN |
| DT10-F-03 CT-8 Trigger-Präzisierung | §34.2 (CT-8, DT10-F-03-Präzisierung) | BEHOBEN |
| DT10-F-04 Parameter-Äquivalenz-Toleranz | §11 (SL-SIG-5), §21 (SL-REP-2) | BEHOBEN |

Restrisiken (bewusst dokumentiert):
- Freitext-only-Menschenweisungen sind nur beratend (§17 SL-ESC-5).
- Unreviewed-Reports blockieren Cold Storage, nicht neue Missionen.
- LLM-Wissenschaftsqualität nur in realen Domänen validierbar.
- Die 4-Achsen-Architektur, Severity-Ordnung (§34.1) und Closure-Regeln (§34.2) sind Design-Festlegungen; ihre reale Bewährung steht aus.

<!-- @section id="36" title="Change-Log" type="prose" -->
### §36 Change-Log

<!-- @table schema="changelog" -->
| Version | Änderung |
|---------|----------|
| 1.0.0 | Erstellung aus GREMIUM_UNIFIED_SPECIFICATION v1.0.0. Integration aller DT8-Backfixes (BF-01..BF-13), DT9-Backfixes (BF-14..BF-18) und DT10-Empfehlungen (CT-10, CT-8-Präzisierung, Parameter-Äquivalenz-Toleranz). Datenverträge in CONTRACTS.md §6.11 ausgelagert. 10 Closure-Regeln (CT-1..CT-10). SL-CT-SIMULTAN. SL-SAF-7. SL-SIG-7a. Quarantäne-Diagnostik-Ausnahme. |

<!-- @section id="37" title="Dokumentenhierarchie" type="prose" -->
## §37 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `specs/` und referenziert:

<!-- @table schema="document_hierarchy_strategic" -->
| Referenz | Zweck |
|----------|-------|
| `foundation/CHARTER.md` | Sicherheitsregeln (CHARTER §SR-XX) |
| `foundation/CONTRACTS.md` §6.11 | Datenverträge (Strategic Layer) |
| `specs/GREMIUM.md` | Pipeline-Mechanik (9-Stufen-Pipeline) |
| `specs/GREMIUM.md` §6.14 | Digital-Twin-Loop (Pipeline-Integration) |
| `ops/VALIDATION.md` §4.7 | Strategic-Layer-Test-Suite (STRAT) |

Regel: Änderungen an strategischen Modulen in diesem Dokument erfordern eine Versionsänderung und eine Überprüfung der referenzierten Dokumente.

Aufteilung zwischen GREMIUM.md und GREMIUM_STRATEGY.md:

<!-- @table schema="document_split_strategic" -->
| Thema | GREMIUM.md | GREMIUM_STRATEGY.md (dieses Dokument) |
|-------|-----------|--------------------------------------|
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

<!-- @section id="A" title="Anhang A: Akzeptanzprüfung" type="acceptance" -->
## Anhang A: Akzeptanzprüfung

Nach dem Einspielen dieser Migration sollte `GREMIUM_STRATEGY.md` folgende Kriterien erfüllen:

<!-- @table schema="acceptance_criteria" -->
| # | Kriterium | Status |
|---|-----------|--------|
| 1 | Kopfzeile enthält Version 1.0.0 | ☐ |
| 2 | YAML-Frontmatter mit doc_id, version, layer vorhanden | ☐ |
| 3 | @section-Marker für alle Abschnitte vorhanden | ☐ |
| 4 | @role-Marker für kanzler und koenigin vorhanden | ☐ |
| 5 | @dataflow-Marker für briefing_cycle, directive_validation, axiom_transition, symptom_trigger, mission_bootstrap vorhanden | ☐ |
| 6 | @table-Marker für alle Tabellen vorhanden | ☐ |
| 7 | @ref-Marker für Querverweise vorhanden | ☐ |
| 8 | @state_machine-Marker für Topic, DimensionRequest, Escalation, Quarantine vorhanden | ☐ |
| 9 | SL-AX-ATOMIC als @dataflow dokumentiert | ☐ |
| 10 | Alle 10 Closure-Regeln (CT-1..CT-10) dokumentiert | ☐ |
| 11 | Keine neuen Datenverträge definiert | ☐ |
| 12 | Keine neuen Sicherheitsregeln definiert | ☐ |
| 13 | CHARTER-Hierarchie bleibt gewahrt | ☐ |
| 14 | Keine strategischen Inhalte in GREMIUM.md dupliziert | ☐ |