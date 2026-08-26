---
doc_id: foundation/CHARTER.md
doc_type: charter
version: 1.0.0
status: BINDEND
schema_version: spec-format-1.0
layer: foundation
builds_on: []
conflict_rule: []
roles_defined: []
roles_referenced:
  - koenigin
  - kanzler
  - kartograph
  - vordenker
  - lotse
  - quartiermeister
  - richter
  - seher
  - archivar
  - dispatcher
  - receiver
test_suites_defined: []
dataflows_defined: []
last_modified: 2026-08-21
---

<!-- @section id="0" title="Präambel: Der Anti-Endlosschleifen-Pakt" type="meta" -->
# 🏛️ CHARTER — VERFASSUNG DES MYRMEX-SYSTEMS

## §0 Präambel: Der Anti-Endlosschleifen-Pakt

Dieses Dokument friert den Scope der Architektur ein.

**Single Source of Truth:** Jede Information in diesem Dokument ist genau einmal definiert. Alle anderen Dokumente referenzieren sie.

**Keine neuen Features:** Unklare Details während der Codierung werden als „Implementation Detail" im Code gelöst, nicht durch neue Spec-Patches.

**Backlog:** Jede neue Idee wandert in ein „Backlog für v3.0.0".

**Vorrang:** Bei Widersprüchen zwischen diesem Dokument und anderen Spezifikationen (CONTRACTS, SPECS) gilt immer dieser Charter.

<!-- @section id="1" title="System-Überblick" type="prose" -->
## §1 System-Überblick

<!-- @section id="1.1" title="Die 6 Schichten" type="prose" -->
### §1.1 Die 6 Schichten

<!-- @table schema="system_layers" -->
| Schicht | Name | Verantwortung |
|---------|------|---------------|
| 5 | 👑 Königin | Langfristige Vision, Meta-Ziele, menschliche Führung |
| 4 | 🏛️ Gremium | Intelligenz, Atlas, Archiv, Ideen, Pakete, Sicherheit |
| 3 | ⚖️ Dispatch-Koordination | Dispatch-Vorbereitung, Lease-/Gate-Koordination |
| 2 | 🧭 Questor | Paketgebundenes Execution Subsystem (Totalfunktion) |
| 1 | 🔌 HAL & Resource Governor | Slot-Routing, Leases, ESTOP, Hardwarezugriff |
| 0 | ⚙️ Physis / Compute | Hardware, Simulation, Compute |

<!-- @section id="1.2" title="Die 9-Stufen-Pipeline" type="prose" -->
### §1.2 Die 9-Stufen-Pipeline

<!-- @table schema="pipeline_stages" -->
| Stufe | Name | Verantwortlich |
|-------|------|----------------|
| 1 | Wissens-Aufnahme | <!-- @role-ref id="archivar" -->Archivar |
| 2 | Atlas-Strukturierung | <!-- @role-ref id="kartograph" -->Kartograph |
| 3 | Strategische Review | <!-- @role-ref id="kanzler" -->Kanzler ↔ Königin |
| 4 | Ideen-Generierung | <!-- @role-ref id="vordenker" -->Vordenker |
| 5a | Pre-Filter | Deterministischer Fast-Path |
| 5b | Ideen-Erdung | <!-- @role-ref id="lotse" -->Lotse |
| 6 | Paket-Bau | <!-- @role-ref id="quartiermeister" -->Quartiermeister |
| 7 | Sicherheits-Gate | <!-- @role-ref id="richter" -->Richter + <!-- @role-ref id="seher" -->Seher |
| 8 | Dispatch & Execution | <!-- @role-ref id="dispatcher" -->Dispatcher → Questor → <!-- @role-ref id="receiver" -->Receiver |

<!-- @section id="2" title="Kernprinzipien" type="prose" -->
## §2 Kernprinzipien (Die 4 Säulen)

<!-- @table schema="core_principles" -->
| # | Prinzip | Definition |
|---|---------|------------|
| 1 | Fail-Closed | Wenn ein Zustand nicht sicher bestimmt werden kann: **keine Ausführung**, kontrollierter Abbruch oder Eskalation. Niemals „blind" weitermachen. |
| 2 | Deterministic-First | LLMs dürfen beraten, aber **niemals final entscheiden**. QuestCompass und PolicyEvaluator entscheiden deterministisch. |
| 3 | Totalfunktion | Questor liefert **IMMER** ein Ergebnis (`questor_ergebnis_paket`). Auch bei Early-Abort, Crash oder Shutdown. |
| 4 | Blackboard-Pattern | Keine direkten Aufrufe zwischen Gremiums-Rängen. Kommunikation nur über Atlas und Archiv. Questor ist **kein** Gremiums-Rang. |

<!-- @section id="3" title="Sicherheitsregeln" type="safety-rule" -->
## §3 Sicherheitsregeln (Der Kanon)

Dies ist die zentrale Liste aller 58 Sicherheitsregeln. Alle anderen Dokumente verweisen auf diese IDs.

<!-- @section id="3.A" title="Grundregeln (Hauptreferenz & Questor)" type="safety-rule" -->
### §3.A Grundregeln (Hauptreferenz & Questor)

<!-- @table schema="safety_rules" category="grundregeln" -->
| ID | Regel |
|----|-------|
| <!-- @safety-rule id="SR-01" category="grundregel" -->SR-01 | Keine physische Ausführung ohne gültigen `QuestorDispatchEnvelope`. |
| <!-- @safety-rule id="SR-02" category="grundregel" -->SR-02 | Keine physische Ausführung ohne gültiges Gate (`gate_record_ref`). |
| <!-- @safety-rule id="SR-03" category="grundregel" -->SR-03 | Keine physische Ausführung ohne gültige Lease (`lease_grants`). |
| <!-- @safety-rule id="SR-04" category="grundregel" -->SR-04 | Questor schreibt **nie** in Atlas oder Archiv. |
| <!-- @safety-rule id="SR-05" category="grundregel" -->SR-05 | Questor setzt **nie** einen ESTOP zurück. |
| <!-- @safety-rule id="SR-06" category="grundregel" -->SR-06 | Questor vergibt **nie** Leases (nur Resource Governor). |
| <!-- @safety-rule id="SR-07" category="grundregel" -->SR-07 | QuestorBlackbox bleibt **lokal** und isoliert. |
| <!-- @safety-rule id="SR-08" category="grundregel" -->SR-08 | Operational ≠ Scientific: Prozessfehler erzeugen keine wissenschaftlichen Signale. |
| <!-- @safety-rule id="SR-09" category="grundregel" -->SR-09 | ESTOP ≠ LEASE_DENIED: Ressourcenkonflikte sind Operational, keine Safety-Events. |
| <!-- @safety-rule id="SR-10" category="grundregel" -->SR-10 | Fail-Closed bei Unklarheit (z.B. unklarer Crash-Zustand). |
| <!-- @safety-rule id="SR-11" category="grundregel" -->SR-11 | Menschliche Königin wird **niemals** überstimmt. |
| <!-- @safety-rule id="SR-12" category="grundregel" -->SR-12 | Hardwarezugriff **nur** über HAL. |
| <!-- @safety-rule id="SR-13" category="grundregel" -->SR-13 | LLM ist **nur Advisor**, niemals finale Instanz. |
| <!-- @safety-rule id="SR-14" category="grundregel" -->SR-14 | NaN/Infinity in Payloads führt zu **Fail-Closed** (C18). |
| <!-- @safety-rule id="SR-15" category="grundregel" -->SR-15 | `atlas_version_ref` ist Pass-Through (kein LLM-Zugriff). |
| <!-- @safety-rule id="SR-16" category="grundregel" -->SR-16 | Recovery erfolgt **NUR** aus WAL (keine Blackbox-Recovery). |
| <!-- @safety-rule id="SR-17" category="grundregel" -->SR-17 | Ledger ist **READ-ONLY** nach Paket-Abschluss. |
| <!-- @safety-rule id="SR-18" category="grundregel" -->SR-18 | Kristallkandidat = Loop + Einstellungen + Ergebnis (nicht nur Messwert). |
| <!-- @safety-rule id="SR-19" category="grundregel" -->SR-19 | Bei SAFETY-Abbruch: Kristalle und Signale sind **leer**. |
| <!-- @safety-rule id="SR-20" category="grundregel" -->SR-20 | `vollstaendig_flag` ist **IMMER** true (Totalfunktion). |
| <!-- @safety-rule id="SR-21" category="grundregel" -->SR-21 | Questor verarbeitet **immer nur EIN** Paket sequentiell. |
| <!-- @safety-rule id="SR-22" category="grundregel" -->SR-22 | Questor ist ein **eigener Prozess** (los gelöst vom Gremium). |
| <!-- @safety-rule id="SR-23" category="grundregel" -->SR-23 | Pakete in `processing/` sind **nicht löschbar** (außer durch Shutdown/Recovery). |

<!-- @section id="3.B" title="Sanitization & LLM-Schutz" type="safety-rule" -->
### §3.B Sanitization & LLM-Schutz

<!-- @table schema="safety_rules" category="sanitization" -->
| ID | Regel |
|----|-------|
| <!-- @safety-rule id="SR-24" category="sanitization" -->SR-24 | Nur Whitelist-Felder (`ziel`, `kontext`, `bounds`) gelangen an das LLM. |
| <!-- @safety-rule id="SR-25" category="sanitization" -->SR-25 | Injection-Patterns werden erkannt und **quarantänen**. |
| <!-- @safety-rule id="SR-26" category="sanitization" -->SR-26 | LLM-Output wird gegen Constraints (`parameter_bounds`) validiert. |
| <!-- @safety-rule id="SR-27" category="sanitization" -->SR-27 | Safety-Claims im LLM-Output („ignore safety") werden **abgelehnt**. |
| <!-- @safety-rule id="SR-28" category="sanitization" -->SR-28 | Bei LLM-Fehler/Timeout: **Deterministischer Fallback**. |
| <!-- @safety-rule id="SR-29" category="sanitization" -->SR-29 | `security_mode` wird dem LLM **NICHT** mitgeteilt. |

<!-- @section id="3.C" title="Capability & Security Mode" type="safety-rule" -->
### §3.C Capability & Security Mode

<!-- @table schema="safety_rules" category="capability" -->
| ID | Regel |
|----|-------|
| <!-- @safety-rule id="SR-30" category="capability" -->SR-30 | Unbekannte Capability → **VETO**. |
| <!-- @safety-rule id="SR-31" category="capability" -->SR-31 | Deprecated Capability → **VETO**. |
| <!-- @safety-rule id="SR-32" category="capability" -->SR-32 | Leere `allowed_capabilities` → **KEINE** Capability erlaubt (Fail-Closed). |
| <!-- @safety-rule id="SR-33" category="capability" -->SR-33 | Security-Mode-Mismatch → **VETO**. |
| <!-- @safety-rule id="SR-34" category="capability" -->SR-34 | NaN/Infinity in Parametern → **Fail-Closed**. |
| <!-- @safety-rule id="SR-35" category="capability" -->SR-35 | Min-Rule: Der restriktivste Modus (Paket/Gate/System/Slot) gewinnt. |
| <!-- @safety-rule id="SR-36" category="capability" -->SR-36 | Kein Default auf `NORMAL` bei fehlendem Modus (`PACKAGE_INVALID`). |
| <!-- @safety-rule id="SR-37" category="capability" -->SR-37 | `RECOVERY` erlaubt nur `reconcile_*` und `read_*`. |
| <!-- @safety-rule id="SR-38" category="capability" -->SR-38 | Keine Modus-Eskalation während der Laufzeit. |
| <!-- @safety-rule id="SR-39" category="capability" -->SR-39 | Gate ist die **absolute Grenze** (Questor darf Gate nicht umgehen). |

<!-- @section id="3.D" title="Shutdown, Health & Ops" type="safety-rule" -->
### §3.D Shutdown, Health & Ops

<!-- @table schema="safety_rules" category="shutdown" -->
| ID | Regel |
|----|-------|
| <!-- @safety-rule id="SR-40" category="shutdown" -->SR-40 | Keine neuen Pakete bei Shutdown. |
| <!-- @safety-rule id="SR-41" category="shutdown" -->SR-41 | Keine neuen HAL-Kommandos bei Shutdown. |
| <!-- @safety-rule id="SR-42" category="shutdown" -->SR-42 | WAL-Flush ist **obligatorisch** vor Beendigung. |
| <!-- @safety-rule id="SR-43" category="shutdown" -->SR-43 | ESTOP **hat Vorrang** vor Shutdown. |
| <!-- @safety-rule id="SR-44" category="shutdown" -->SR-44 | Shutdown ist **immer OPERATIONAL** (nie SAFETY). |
| <!-- @safety-rule id="SR-45" category="shutdown" -->SR-45 | Health-Monitoring ist **immer OPERATIONAL**. |
| <!-- @safety-rule id="SR-46" category="shutdown" -->SR-46 | Health-Monitoring blockiert **nicht** die Ausführung. |
| <!-- @safety-rule id="SR-47" category="shutdown" -->SR-47 | Kein automatischer Neustart bei `WAITING_FOR_RELEASE` oder `SAFE_HOLD`. |
| <!-- @safety-rule id="SR-48" category="shutdown" -->SR-48 | Kein automatischer Neustart ohne WAL-Prüfung. |

<!-- @section id="3.E" title="Trail-Map & Queue" type="safety-rule" -->
### §3.E Trail-Map & Queue

<!-- @table schema="safety_rules" category="queue" -->
| ID | Regel |
|----|-------|
| <!-- @safety-rule id="SR-49" category="queue" -->SR-49 | Trail-Map ist **OPERATIONAL** (keine wissenschaftlichen Signale). |
| <!-- @safety-rule id="SR-50" category="queue" -->SR-50 | Trail-Map bleibt **lokal** (Blackbox). |
| <!-- @safety-rule id="SR-51" category="queue" -->SR-51 | Trail-Map ist **APPEND-ONLY**. |
| <!-- @safety-rule id="SR-52" category="queue" -->SR-52 | Trail-Map wird **nicht** vom LLM gelesen. |
| <!-- @safety-rule id="SR-53" category="queue" -->SR-53 | Kein Dispatch ohne `gate_record_ref`. |
| <!-- @safety-rule id="SR-54" category="queue" -->SR-54 | Keine Duplikate in der Queue (Idempotenz). |
| <!-- @safety-rule id="SR-55" category="queue" -->SR-55 | Atomare Schreiboperationen (temp + rename). |
| <!-- @safety-rule id="SR-56" category="queue" -->SR-56 | Registry-Lock ist Pflicht. |
| <!-- @safety-rule id="SR-57" category="queue" -->SR-57 | Kein Löschen von `processing/` durch Gremium. |
| <!-- @safety-rule id="SR-58" category="queue" -->SR-58 | Queue-Fehler sind **immer OPERATIONAL**. |

<!-- @section id="4" title="Gremium-Auslagerungen" type="prose" -->
## §4 Gremium-Auslagerungen (Der Kanon)

Aufgaben, die Questor NICHT selbst erledigt, sondern an das Gremium delegiert.

<!-- @table schema="gremium_delegations" -->
| ID | Thema | Verantwortlich |
|----|-------|----------------|
| G-01 | Template-Erstellung bei fehlendem Template | Quartiermeister + Experte |
| G-02 | Template-Korrektur nach Feedback | Domain-Experte |
| G-03 | Template-Versionierung (Archiv) | Archivar |
| G-04 | Ressourcen-Karte (Verbrauch) | Kartograph |
| G-05 | Prozess-Skizze mit Idee | Vordenker |
| G-06 | `template_feedback` protokollieren | Archivar |
| G-07 | Kosten-Schätzungen (Reagenzien) | System-Integrator |
| G-08 | Periodische Template-Übersicht | Kanzler |
| G-09 | `template_feedback` berücksichtigen | Quartiermeister |
| G-10 | `atlas_version_ref` Pass-Through | Questor (Intern) |
| G-11 | `loop_selection_weights` | Quartiermeister |
| G-12 | `planning_hints` | Quartiermeister |
| G-13 | Atlas-Update via Registry | Pipeline-Orchestrator |
| G-14 | Queue-Bereinigung | Archivar |
| G-15 | Löschanfragen stellen | Kanzler |
| G-16 | Capability-Definitionen pflegen | System-Integrator |
| G-17 | Health-Monitoring (Extern) | Pipeline-Orchestrator |
| G-18 | Recovery-Aktionen auslösen | Kanzler |
| G-19 | Shutdown-Signal senden | Kanzler |
| G-20 | Trail-Map lesen (Audit) | Domain-Experte |
| G-21 | CI/CD Pipeline | System-Integrator |
| G-22 | Phasen-Freigabe | Kanzler / Architekt |

<!-- @section id="5" title="Grundannahmen & Invarianten" type="prose" -->
## §5 Grundannahmen & Invarianten

<!-- @table schema="invariants" -->
| Thema | Invariante |
|-------|-----------|
| Nebenläufigkeit | Questor verarbeitet immer nur EIN Paket sequentiell. |
| LLM-Backend | Abstrahiert (Ollama/gemma), wechselbar, aber nie entscheidend. |
| Kosten-Tracking | Zeit + Reagenzien + Compute (normiert). |
| Kristallkandidat | Loop + Einstellungen + Ergebnis (NICHT der Messwert allein). |
| Signal | Fazit aus Kristallkandidaten (deterministisch erzeugt). |
| Budget-Logik | Ziel erreichen, nicht Budget ausgeben. |

<!-- @section id="6" title="Verbotene Patterns" type="prose" -->
## §6 Verbotene Patterns

Folgende Muster sind in der Zielarchitektur streng verboten:

<!-- @table schema="forbidden_patterns" -->
| # | Pattern | CHARTER-Referenz |
|---|---------|-----------------|
| VP-01 | Questor schreibt in Atlas/Archiv | <!-- @ref target="CHARTER §SR-04" type="security-rule" -->SR-04 |
| VP-02 | Questor setzt ESTOP zurück | <!-- @ref target="CHARTER §SR-05" type="security-rule" -->SR-05 |
| VP-03 | Gremium liest QuestorBlackbox | <!-- @ref target="CHARTER §SR-07" type="security-rule" -->SR-07 |
| VP-04 | Dispatcher sendet produktiv ohne `gate_record_ref` | <!-- @ref target="CHARTER §SR-53" type="security-rule" -->SR-53 |
| VP-05 | Produktive Adapterlogik zwischen alter (Swarm) und neuer (Questor) Welt | — |
| VP-06 | Operational wird als Scientific interpretiert | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->SR-08 |
| VP-07 | LEASE_DENIED wird als ESTOP behandelt | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |
| VP-08 | HAL vergibt Leases | <!-- @ref target="CHARTER §SR-06" type="security-rule" -->SR-06 |
| VP-09 | HAL interpretiert wissenschaftliche Ziele | <!-- @ref target="CHARTER §SR-08" type="security-rule" -->SR-08 |
| VP-10 | Zwei gleichwertige primäre Referenzdateien ohne Konflikthierarchie | — |

<!-- @section id="7" title="Idempotenz-Kanon" type="prose" -->
## §7 Idempotenz-Kanon

Der `idempotency_key` ist der Schlüssel zur Crash-Sicherheit und Duplikat-Vermeidung.

**Format:**

```
^[A-Za-z0-9._-]{1,128}$:^[A-Za-z0-9._-]{1,128}$:[0-9]{1,6}
```

**Komponenten:**
- `package_id` (String, max 128 Zeichen)
- `zyklus_id` (String, max 128 Zeichen)
- `attempt_id` (Integer, 0 bis 999999, keine führenden Nullen)

**Beispiele:**

<!-- @table schema="idempotency_examples" -->
| Beispiel | Status | Begründung |
|----------|--------|-----------|
| `pkg-001:zyklus-014:2` | ✅ Gültig | Korrektes Format |
| `pkg-001:zyklus-014:02` | ❌ Ungültig | Führende Null in attempt_id |
| `pkg 001:zyklus-014:2` | ❌ Ungültig | Leerzeichen in package_id |

<!-- @section id="8" title="Dokumentenhierarchie" type="prose" -->
## §8 Dokumentenhierarchie

Dieses Dokument steht an der Spitze der Pyramide.

<!-- @table schema="document_hierarchy" -->
| Layer | Dateien | Beschreibung |
|-------|---------|--------------|
| Layer 0 (Fundament) | `CHARTER.md` (dieses Dokument), `CONTRACTS.md`, `SPEC_FORMAT.md` | Verfassung, Datenverträge, Formatdefinition |
| Layer 1 (Spezifikation) | `QUESTOR.md`, `HAL.md`, `GREMIUM.md`, `GREMIUM_STRATEGY.md`, `CAROUSEL_TWIN.md` | System-Spezifikationen |
| Layer 2 (Operation) | `VALIDATION.md`, `VALIDATION_ATLAS.md`, `ROADMAP.md` | Teststrategie, Implementierungsplan |
| Layer 3 (Views) | `ROLE_VIEWS.md`, `DATAFLOW_MAP.md`, `TEST_MATRIX_BY_ROLE.md` | Abgeleitete Sichten (generiert) |

**Regel:** Ein Dokument in Layer N darf niemals ein Dokument in Layer N-1 widersprechen.

**Konfliktregel:** `CHARTER.md` > `CONTRACTS.md` > `specs/*` > `ops/*` > `views/*`