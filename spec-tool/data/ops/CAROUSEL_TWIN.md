---
doc_id: specs/CAROUSEL_TWIN.md
doc_type: spec
version: 1.1.0-patch.1
status: BINDEND
schema_version: spec-format-1.0
layer: specs
builds_on:
  - foundation/CHARTER.md@1.0.0
  - foundation/CONTRACTS.md@1.2.1-twin.1
  - specs/HAL.md@1.1.0-atlas-hyb.1
  - specs/QUESTOR.md@1.1.0-atlas-hyb.1
conflict_rule: [CHARTER, CONTRACTS, HAL, QUESTOR, THIS_DOC]
roles_defined:
  - carousel_dummy_hal
  - carousel_twin_des
  - carousel_twin_ode
  - carousel_twin_noise
roles_referenced:
  - quartiermeister
  - questor
  - hal_interface
dataflows_defined:
  - carousel_experiment_flow
  - carousel_calibration_flow
last_modified: 2026-08-21
---

<!-- @section id="0" title="Geltung und Änderungsregeln" type="meta" -->
# 🎠 CAROUSEL_TWIN — KARUSSELL-MVP HARDWARE-SPEZIFIKATION

## §0 Geltung und Änderungsregeln

Dieses Dokument definiert:
Die Hardware-Spezifikation des Karussell-MVP (Schicht 0/1)
Die HAL-Slot-Definitionen und Capabilities
Das Digital-Twin-Modell (3-Schichten-Architektur)
Das erste Experiment: Fluorescein-Photobleaching
Die Integration in das MYRMEX-System

Regel: Dieses Dokument referenziert Verträge aus `CONTRACTS.md` und Sicherheitsregeln aus `CHARTER.md`.
Es definiert keine neuen Sicherheitsregeln.

Konfliktregel: Bei Widersprüchen gilt `CHARTER.md` > `CONTRACTS.md` > `HAL.md` > `QUESTOR.md` > dieses Dokument.

<!-- @section id="0.1" title="Änderungsantrag CAROUSEL_TWIN_BLOCKFIX-1.0.0" type="change-request" -->
### §0.1 Änderungsantrag CAROUSEL_TWIN_BLOCKFIX-1.0.0 — Blocker-Behebung

Dieser Änderungsantrag behebt die 5 BLOCKER aus dem Langzeit-Dry-Test.

<!-- @table schema="blockfix_changes" -->
| CT-ID | Änderung | Schwere |
|-------|----------|---------|
| CT-01 | `max_command_timeout_s` im Manifest auf 3600.0 erhöht | BLOCKER |
| CT-02 | UV-Step von `HAL_COMMAND` auf `PROCESS_COMMAND` geändert | BLOCKER |
| CT-03 | `default_lease_ttl_s` auf 7200.0 erhöht | BLOCKER |
| CT-04 | Neuer `carousel-transport`-Slot für `carousel.rotate` und `carousel.discard` | BLOCKER |
| CT-05 | Alle Slots auf `sandbox_capable=True` gesetzt | BLOCKER |

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge.
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln.
- Die bestehende CHARTER-Hierarchie bleibt unberührt.

<!-- @section id="0.2" title="Änderungsantrag CAROUSEL_TWIN_REMAINING_FIXES-1.0.0" type="change-request" -->
### §0.2 Änderungsantrag CAROUSEL_TWIN_REMAINING_FIXES-1.0.0 — Verbleibende Funde

Dieser Änderungsantrag behebt die 11 verbleibenden Funde (CT-06 bis CT-18) und die CT-19-Korrektur.

<!-- @table schema="remaining_fixes_changes" -->
| CT-ID | Änderung | Schwere |
|-------|----------|---------|
| CT-06 | `parameter_schema` im LoopTemplate definiert | HOCH |
| CT-07 | `StageReleasePolicy` für UV-Step (K-03: UV > 3600s) | HOCH |
| CT-08 | `digital_twin_ref` im LoopTemplate hinzugefügt | HOCH |
| CT-09 | `twin_pairing_mode` entfernt; Planungszeit-Entscheidung durch Quartiermeister | HOCH |
| CT-10 | Interlock-Sensor im Manifest modelliert | HOCH |
| CT-11 | `estop_mechanism` auf `EXTERNAL_SAFETY_CHAIN` geändert | HOCH |
| CT-12 | `max_step_retries` auf 0 gesetzt | MITTEL |
| CT-13 | `on_lease_expiry_policy` für UV-Step gesetzt (in BLOCKFIX) | MITTEL |
| CT-14 | DES-Typen als interne Implementierungsdetails gekennzeichnet | MITTEL |
| CT-15 | `UNKNOWN_CAPABILITY` durch `COMMAND_INVALID` ersetzt | MITTEL |
| CT-16 | Zonen-Definition auf alle 5 Dimensionen erweitert | MITTEL |
| CT-17 | Dummy-HAL-Zustandsvariablen definiert | NIEDRIG |
| CT-18 | `estimated_cost` als Puffer gekennzeichnet | NIEDRIG |
| CT-19 | Dispatch-Strategie als Planungszeit-Entscheidung durch Quartiermeister | HOCH |

Regeln:
- Dieser Änderungsantrag definiert keine neuen Verträge.
- Dieser Änderungsantrag definiert keine neuen Sicherheitsregeln.
- Die bestehende CHARTER-Hierarchie bleibt unberührt.

<!-- @section id="0.3" title="Dispatch-Strategie (CT-19 Korrektur)" type="prose" -->
### §0.3 Dispatch-Strategie (CT-19 Korrektur)

Die Entscheidung, ob ein SIM-Paket, ein REAL-Paket oder beide erstellt werden, fällt der Quartiermeister (Stufe 6) während des Paket-Baus.

<!-- @table schema="dispatch_strategy" -->
| Strategie | Bedeutung | Wann |
|-----------|-----------|------|
| SIM_ONLY | Nur Simulation | Kalibrierung, Twin-Validierung, Gefahrenprüfung |
| REAL_ONLY | Nur physisch | Intakter Twin, VALIDATE, keine Twin-Referenz |
| SIM_THEN_REAL | Beide werden geplant, aber als unabhängige Pakete dispatched | Exploration in UNEXPLORED-Zonen, geringe support_confidence |
| REAL_THEN_SIM | Physisch zuerst, dann Simulationsvergleich | Nachkalibrierung nach neuem Experiment |

Regeln:
- Die Entscheidung ist deterministisch und erfolgt im Quartiermeister.
- Es gibt keine automatische SIM→REAL-Kette.
- Das SIM-Ergebnis fließt über den Archivar → Kartograph → Atlas zurück.
- Die FrontierEngine kann basierend auf dem SIM-Ergebnis einen FrontierCandidate erzeugen.
- Der Quartiermeister entscheidet basierend auf dem Atlas-Zustand, ob ein REAL-Paket gebaut wird.

<!-- @section id="1" title="Hardware-Übersicht" type="prose" -->
## §1 Hardware-Übersicht

<!-- @section id="1.1" title="Systembeschreibung" type="prose" -->
### §1.1 Systembeschreibung

Das Karussell-MVP ist ein 3D-gedrucktes Laborautomatisierungssystem mit:
1 rotierender Plattform (Schrittmotor + Zahnkranz)
Einweg-Petrischalen (Ø 35 mm, transparent, UV-durchlässig)
4 modularen Stationen (an festen Positionen um das Karussell)
Keiner aktiven Heizung (Raumtemperatur-Prozesse)
Keiner geschlossener Flüssigkeitsführung (offene Petrischale)

<!-- @section id="1.2" title="Stationen-Übersicht" type="prose" -->
### §1.2 Stationen-Übersicht

<!-- @table schema="station_overview" -->
| Station | Position | Funktion | Aktorik | Sensorik |
|---------|----------|----------|---------|----------|
| S1 | 0° | Probenzugabe | Peristaltische Pumpe | Volumen-Sensor (optional) |
| S2 | 90° | Mischen | Servo (Kipp-Mechanismus) | — |
| S3 | 180° | UV-Belichtung | UV-LED (365 nm) | Timer |
| S4 | 270° | Fluoreszenz-Messung | LED (488 nm) + Kamera | CMOS-Kamera + Filter |

<!-- @section id="1.3" title="Mechanische Parameter" type="prose" -->
### §1.3 Mechanische Parameter

<!-- @table schema="mechanical_parameters" -->
| Parameter | Wert | Einheit |
|-----------|------|---------|
| Karussell-Durchmesser | 200 | mm |
| Schalen-Durchmesser | 35 | mm |
| Schalen-Volumen (max) | 5 | mL |
| Rotationszeit (eine Position) | 3.0 | s |
| Rotationszeit (vollständige Umdrehung) | 12.0 | s |
| Positioniergenauigkeit | ±0.5 | mm |
| Kippwinkel (Mischen) | 15–30 | ° |
| Kippfrequenz (Mischen) | 0.5–2.0 | Hz |

<!-- @section id="1.4" title="Sicherheitsrelevante Aspekte" type="prose" -->
### §1.4 Sicherheitsrelevante Aspekte

<!-- @table schema="safety_aspects" -->
| Aspekt | Maßnahme | CHARTER-Referenz |
|--------|----------|-----------------|
| UV-Strahlung (365 nm) | Geschlossenes Gehäuse mit Interlock-Schalter | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |
| Bewegliche Teile (Karussell) | Schrittmotor mit Endschalter | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |
| Chemikalien (Fluorescein, NaOH) | Einweg-Schale, keine Wiederverwendung | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->SR-10 |
| Elektrische Sicherheit | Niederspannung (12V/5V) | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |

<!-- @section id="2" title="HAL-Slot-Definitionen" type="prose" -->
## §2 HAL-Slot-Definitionen

<!-- @section id="2.1" title="EnvironmentManifest" type="contract" contract="EnvironmentManifest" -->
### §2.1 EnvironmentManifest

<!-- @contract name="EnvironmentManifest" type="pydantic" section="2.1" -->
```python
EnvironmentManifest(
    environment_id="carousel-v1",
    environment_version="1.1.0",
    schema_version="1.1.0-atlas-hyb.1",
    estop_mechanism="EXTERNAL_SAFETY_CHAIN",  # ← CT-11: geändert von SOFTWARE
    max_command_timeout_s=3600.0,             # ← CT-01: erhöht von 60.0
    default_lease_ttl_s=7200.0,               # ← CT-03: erhöht von 300.0
    heartbeat_interval_s=5.0,
    supported_security_modes=["NORMAL", "SANDBOX", "DEV_SANDBOX_ONLY", "RECOVERY"],
    supported_resource_classes=["LAB_ACTUATOR", "SANDBOX_ENVIRONMENT"],
    interlock_sources=[                       # ← CT-10: neu hinzugefügt
        "uv-enclosure-switch",
        "carousel-end-switch",
        "estop-button",
    ],
    slots=[...],       # → §2.2
    mutex_zones=[...], # → §2.3
    capabilities=[...], # → §2.4
)
```

<!-- @section id="2.2" title="SlotDescriptors" type="prose" -->
### §2.2 SlotDescriptors

<!-- @section id="2.2.1" title="S1: Probenzugabe (Dispense)" type="contract" contract="SlotDescriptor" -->
#### S1: Probenzugabe (Dispense)

<!-- @contract name="SlotDescriptor_carousel_dispense" type="pydantic" section="2.2.1" -->
```python
SlotDescriptor(
    slot_id="carousel-dispense",
    display_name="Karussell Station 1: Probenzugabe",
    resource_class=ResourceClass.LAB_ACTUATOR,
    capabilities=["pump.dispense"],
    mutex_group="carousel-position",
    physical_zones=["carousel-zone-s1"],
    physical_actuation=True,
    compute_capable=False,
    sandbox_capable=True,  # ← CT-05: geändert von False
    requires_path_reservation=False,
    max_concurrent_commands=1,
    estop_controllable=True,
    max_command_timeout_s=60.0,
    max_process_duration_s=120.0,
    max_parameter_payload_bytes=4096,
    supported_process_modes=["START"],
)
```

<!-- @section id="2.2.2" title="S2: Mischen (Swirl)" type="contract" contract="SlotDescriptor" -->
#### S2: Mischen (Swirl)

<!-- @contract name="SlotDescriptor_carousel_mix" type="pydantic" section="2.2.2" -->
```python
SlotDescriptor(
    slot_id="carousel-mix",
    display_name="Karussell Station 2: Mischen",
    resource_class=ResourceClass.LAB_ACTUATOR,
    capabilities=["carousel.swirl"],
    mutex_group="carousel-position",
    physical_zones=["carousel-zone-s2"],
    physical_actuation=True,
    compute_capable=False,
    sandbox_capable=True,  # ← CT-05: geändert von False
    requires_path_reservation=False,
    max_concurrent_commands=1,
    estop_controllable=True,
    max_command_timeout_s=120.0,
    max_process_duration_s=300.0,
    max_parameter_payload_bytes=4096,
    supported_process_modes=["START"],
)
```

<!-- @section id="2.2.3" title="S3: UV-Belichtung" type="contract" contract="SlotDescriptor" -->
#### S3: UV-Belichtung

<!-- @contract name="SlotDescriptor_carousel_uv" type="pydantic" section="2.2.3" -->
```python
SlotDescriptor(
    slot_id="carousel-uv",
    display_name="Karussell Station 3: UV-Belichtung",
    resource_class=ResourceClass.LAB_ACTUATOR,
    capabilities=["uv.expose"],
    mutex_group="carousel-position",
    physical_zones=["carousel-zone-s3"],
    physical_actuation=True,
    compute_capable=False,
    sandbox_capable=True,  # ← CT-05: geändert von False
    requires_path_reservation=False,
    max_concurrent_commands=1,
    estop_controllable=True,
    max_command_timeout_s=3600.0,
    max_process_duration_s=3600.0,
    max_parameter_payload_bytes=4096,
    supported_process_modes=["START", "MONITOR", "ABORT"],
)
```

<!-- @section id="2.2.4" title="S4: Fluoreszenz-Messung" type="contract" contract="SlotDescriptor" -->
#### S4: Fluoreszenz-Messung

<!-- @contract name="SlotDescriptor_carousel_fluorometer" type="pydantic" section="2.2.4" -->
```python
SlotDescriptor(
    slot_id="carousel-fluorometer",
    display_name="Karussell Station 4: Fluoreszenz-Messung",
    resource_class=ResourceClass.LAB_ACTUATOR,
    capabilities=["fluorometer.measure", "camera.capture"],
    mutex_group="carousel-position",
    physical_zones=["carousel-zone-s4"],
    physical_actuation=False,  # Nur Messung, keine Aktorik
    compute_capable=False,
    sandbox_capable=True,  # ← CT-05: geändert von False
    requires_path_reservation=False,
    max_concurrent_commands=1,
    estop_controllable=True,
    max_command_timeout_s=30.0,
    max_process_duration_s=60.0,
    max_parameter_payload_bytes=4096,
    supported_process_modes=["START"],
)
```

<!-- @section id="2.2.5" title="Transport: Rotation & Entsorgung (NEU)" type="contract" contract="SlotDescriptor" -->
#### Transport: Rotation & Entsorgung (NEU — CT-04)

<!-- @contract name="SlotDescriptor_carousel_transport" type="pydantic" section="2.2.5" -->
```python
SlotDescriptor(
    slot_id="carousel-transport",
    display_name="Karussell Transport: Rotation & Entsorgung",
    resource_class=ResourceClass.LAB_ACTUATOR,
    capabilities=["carousel.rotate", "carousel.discard"],  # ← CT-04: Capabilities zugeordnet
    mutex_group="carousel-position",
    physical_zones=["carousel-zone-rotation"],
    physical_actuation=True,
    compute_capable=False,
    sandbox_capable=True,  # ← CT-05
    requires_path_reservation=False,
    max_concurrent_commands=1,
    estop_controllable=True,
    max_command_timeout_s=30.0,
    max_process_duration_s=60.0,
    max_parameter_payload_bytes=4096,
    supported_process_modes=["START"],
)
```

<!-- @section id="2.3" title="MutexZone" type="contract" contract="MutexZone" -->
### §2.3 MutexZone

<!-- @contract name="MutexZone_carousel_rotation" type="pydantic" section="2.3" -->
```python
MutexZone(
    zone_id="carousel-rotation",
    slots=[
        "carousel-dispense",
        "carousel-mix",
        "carousel-uv",
        "carousel-fluorometer",
        "carousel-transport",  # ← CT-04: Transport-Slot hinzugefügt
    ],
    lock_policy=LockPolicy.EXCLUSIVE,
)
```

Regel: Nur eine Station kann gleichzeitig aktiv sein. Das Karussell muss sich an der richtigen Position befinden, bevor eine Station aktiviert wird.

<!-- @section id="2.4" title="Capabilities" type="prose" -->
### §2.4 Capabilities

<!-- @table schema="capabilities_overview" -->
| Capability-ID | Slot-ID | Parameter | physical_actuation |
|---------------|---------|-----------|-------------------|
| carousel.rotate | carousel-transport | target_position: int (0–3) | True |
| pump.dispense | carousel-dispense | volume_ml: float, flow_rate_ml_min: float | True |
| carousel.swirl | carousel-mix | duration_s: float, intensity: str | True |
| uv.expose | carousel-uv | duration_s: float, intensity_percent: float | True |
| fluorometer.measure | carousel-fluorometer | excitation_nm: int, emission_nm: int, exposure_ms: int | False |
| camera.capture | carousel-fluorometer | exposure_ms: int, gain: float | False |
| carousel.discard | carousel-transport | — | True |

<!-- @section id="3" title="Capability-Definitionen (Questor-Registry)" type="prose" -->
## §3 Capability-Definitionen (Questor-Registry)

<!-- @section id="3.1" title="carousel.rotate" type="contract" contract="CapabilityDefinition" -->
### §3.1 `carousel.rotate`

<!-- @contract name="CapabilityDefinition_carousel_rotate" type="yaml" section="3.1" -->
```yaml
capability_id: carousel.rotate
version: "1.0"
schema_version: "1.0"
domain: general
display_name: "Karussell-Rotation"
description: "Dreht das Karussell zur Zielposition"
hal_capability_ref: carousel.rotate
parameter_schema:
  target_position:
    type: INTEGER
    required: true
    min: 0
    max: 3
    description: "Zielposition (0=S1, 1=S2, 2=S3, 3=S4)"
requires_physical_actuation: true
allowed_security_modes: [NORMAL, SANDBOX, DEV_SANDBOX_ONLY]
requires_lease: true
requires_dimension_approval: false
cost_estimate:
  time_cost_s: 3.0
  reagent_cost: 0.0
  compute_cost: 0.0
  energy_cost: 0.01
max_timeout_s: 15.0
max_concurrent_executions: 1
deprecated: false
```

<!-- @section id="3.2" title="pump.dispense" type="contract" contract="CapabilityDefinition" -->
### §3.2 `pump.dispense`

<!-- @contract name="CapabilityDefinition_pump_dispense" type="yaml" section="3.2" -->
```yaml
capability_id: pump.dispense
version: "1.0"
schema_version: "1.0"
domain: chemie
display_name: "Peristaltische Pumpe: Dispensierung"
description: "Gibt Flüssigkeit in die Petrischale ab"
hal_capability_ref: pump.dispense
parameter_schema:
  volume_ml:
    type: FLOAT
    required: true
    min: 0.1
    max: 10.0
    unit: mL
    description: "Zielvolumen"
  flow_rate_ml_min:
    type: FLOAT
    required: true
    min: 0.1
    max: 5.0
    unit: mL/min
    description: "Flussrate"
requires_physical_actuation: true
allowed_security_modes: [NORMAL, SANDBOX, DEV_SANDBOX_ONLY]
requires_lease: true
requires_dimension_approval: false
cost_estimate:
  time_cost_s: 30.0
  reagent_cost: 0.05
  compute_cost: 0.0
  energy_cost: 0.01
max_timeout_s: 60.0
max_concurrent_executions: 1
deprecated: false
```

<!-- @section id="3.3" title="carousel.swirl" type="contract" contract="CapabilityDefinition" -->
### §3.3 `carousel.swirl`

<!-- @contract name="CapabilityDefinition_carousel_swirl" type="yaml" section="3.3" -->
```yaml
capability_id: carousel.swirl
version: "1.0"
schema_version: "1.0"
domain: general
display_name: "Karussell: Schwenken/Mischen"
description: "Mischt die Probe durch Kippen der Petrischale"
hal_capability_ref: carousel.swirl
parameter_schema:
  duration_s:
    type: FLOAT
    required: true
    min: 5.0
    max: 300.0
    unit: s
    description: "Mischdauer"
  intensity:
    type: ENUM
    required: true
    values: [LOW, MEDIUM, HIGH]
    description: "Mischintensität"
requires_physical_actuation: true
allowed_security_modes: [NORMAL, SANDBOX, DEV_SANDBOX_ONLY]
requires_lease: true
requires_dimension_approval: false
cost_estimate:
  time_cost_s: 30.0
  reagent_cost: 0.0
  compute_cost: 0.0
  energy_cost: 0.01
max_timeout_s: 300.0
max_concurrent_executions: 1
deprecated: false
```

<!-- @section id="3.4" title="uv.expose" type="contract" contract="CapabilityDefinition" -->
### §3.4 `uv.expose`

<!-- @contract name="CapabilityDefinition_uv_expose" type="yaml" section="3.4" -->
```yaml
capability_id: uv.expose
version: "1.0"
schema_version: "1.0"
domain: chemie
display_name: "UV-Belichtung (365 nm)"
description: "Belichtet die Probe mit UV-Licht"
hal_capability_ref: uv.expose
parameter_schema:
  duration_s:
    type: FLOAT
    required: true
    min: 10.0
    max: 3600.0
    unit: s
    description: "Belichtungsdauer"
  intensity_percent:
    type: FLOAT
    required: true
    min: 10.0
    max: 100.0
    unit: "%"
    description: "UV-Intensität"
requires_physical_actuation: true
allowed_security_modes: [NORMAL, SANDBOX, DEV_SANDBOX_ONLY]
requires_lease: true
requires_dimension_approval: false
cost_estimate:
  time_cost_s: 60.0
  reagent_cost: 0.0
  compute_cost: 0.0
  energy_cost: 0.05
max_timeout_s: 3600.0
max_concurrent_executions: 1
deprecated: false
```

<!-- @section id="3.5" title="fluorometer.measure" type="contract" contract="CapabilityDefinition" -->
### §3.5 `fluorometer.measure`

<!-- @contract name="CapabilityDefinition_fluorometer_measure" type="yaml" section="3.5" -->
```yaml
capability_id: fluorometer.measure
version: "1.0"
schema_version: "1.0"
domain: physik
display_name: "Fluoreszenz-Messung"
description: "Misst die Fluoreszenz-Intensität der Probe"
hal_capability_ref: fluorometer.measure
parameter_schema:
  excitation_nm:
    type: INTEGER
    required: true
    min: 300
    max: 700
    unit: nm
    description: "Anregungswellenlänge"
  emission_nm:
    type: INTEGER
    required: true
    min: 350
    max: 800
    unit: nm
    description: "Emissionswelllänge"
  exposure_ms:
    type: INTEGER
    required: true
    min: 10
    max: 5000
    unit: ms
    description: "Belichtungszeit der Kamera"
requires_physical_actuation: false
allowed_security_modes: [NORMAL, SANDBOX, DEV_SANDBOX_ONLY]
requires_lease: true
requires_dimension_approval: false
cost_estimate:
  time_cost_s: 10.0
  reagent_cost: 0.0
  compute_cost: 0.01
  energy_cost: 0.01
max_timeout_s: 30.0
max_concurrent_executions: 1
deprecated: false
```

<!-- @section id="4" title="Digital-Twin-Modell" type="prose" -->
## §4 Digital-Twin-Modell

<!-- @section id="4.1" title="Architektur-Übersicht" type="prose" -->
### §4.1 Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│  SCHICHT 1: Discrete Event Simulation (DES)                 │
│  → Karussell-Rotation, Stations-Sequenzierung, Timing       │
│  → "WANN passiert WAS an WELCHER Station?"                  │
├─────────────────────────────────────────────────────────────┤
│  SCHICHT 2: Lumped-Parameter-Modelle (ODEs)                 │
│  → Photobleaching, Fluoreszenz, Pumpen, Mischen             │
│  → "WIE verändert sich die Probe an jeder Station?"         │
├─────────────────────────────────────────────────────────────┤
│  SCHICHT 3: Stochastische Rauschmodelle                     │
│  → Messrauschen, Pipettier-Ungenauigkeit, LED-Drift         │
│  → "WAS sieht der Sensor WIRKLICH?"                         │
└─────────────────────────────────────────────────────────────┘
```

<!-- @section id="4.2" title="DigitalTwinModel (CONTRACTS §6.10.19)" type="contract" contract="DigitalTwinModel" -->
### §4.2 DigitalTwinModel (CONTRACTS §6.10.19)

<!-- @contract name="DigitalTwinModel_carousel" type="pydantic" section="4.2" -->
```python
DigitalTwinModel(
    twin_model_id="carousel-fluorescein-photobleaching-v1",
    display_name="Karussell v1 — Fluorescein-Photobleaching",
    domain="chemie",
    model_artifact_ref="data/twins/carousel_photobleaching_v1_sim.py",
    model_version="1.0.0",
    parameter_schema_ref="data/twins/carousel_photobleaching_v1_params.yaml",
    calibration_method="sim_vs_real_fluorescence_decay",
    last_calibration_at=None,  # Noch nicht kalibriert
    calibration_history=[],
    divergence_threshold=0.10,
    drift_score=0.0,
    validity=None,
    created_at="2026-08-21T00:00:00Z",
    updated_at="2026-08-21T00:00:00Z",
)
```

<!-- @section id="4.3" title="Schicht 1: DES — Karussell-Skelett" type="prose" -->
### §4.3 Schicht 1: DES — Karussell-Skelett

<!-- @ref target="foundation/CONTRACTS.md §6.10.19" type="contract" -->
→ Siehe CONTRACTS §6.10.19 für den DigitalTwinModel-Vertrag.

<!-- @section id="4.3.1" title="Interne DES-Typen (CT-14)" type="prose" -->
#### §4.3.1 Interne DES-Typen (CT-14)

Die folgenden Typen werden von der DES verwendet und sind als interne Implementierungsdetails definiert (→ MASTER_INDEX §1).
Sie sind keine CONTRACTS-Verträge und werden nicht in CONTRACTS.md definiert.

<!-- @contract name="CarouselDES_types" type="python" section="4.3.1" -->
```python
class StationAction:
    """
    Abstrakte Basisklasse für eine Stations-Aktion.
    Jede Station (Dispense, Swirl, UV, Measure) implementiert
    eine konkrete StationAction.
    """
    station_id: str
    duration_s: float

    def execute(self, sample_state: "SampleState") -> "StationResult":
        raise NotImplementedError

class StationResult:
    """
    Ergebnis einer Stations-Aktion.
    """
    duration_s: float
    state_changes: dict[str, Any] = {}

class SampleState:
    """
    Zustand der Probe während des Zyklus.
    """
    volume_ml: float = 0.0
    fluorescein_concentration_uM: float = 0.0
    ph: float = 7.0
    fluorescence_intensity: float = 0.0
    uv_dose_j_cm2: float = 0.0
    is_mixed: bool = False

    def update(self, result: StationResult) -> None:
        """Aktualisiert den Probenzustand basierend auf dem Stationsergebnis."""
        for key, value in result.state_changes.items():
            if hasattr(self, key):
                setattr(self, key, value)

class CycleResult:
    """
    Ergebnis eines vollständigen Messzyklus.
    """
    total_time_s: float
    final_state: SampleState
```

Regeln:
- Diese Typen sind Karussell-spezifisch und gehören NICHT in CONTRACTS.md.
- Sie werden in `src/twins/carousel/` implementiert.
- Sie sind nicht Pydantic-Modelle, sondern einfache Python-Klassen.
- Die DES nutzt diese Typen intern. Die HAL-Bridge und Questor verwenden ausschließlich CONTRACTS-Verträge.

<!-- @section id="4.3.2" title="CarouselDES-Klasse" type="prose" -->
#### §4.3.2 CarouselDES-Klasse

<!-- @contract name="CarouselDES" type="python" section="4.3.2" -->
```python
class CarouselDES:
    """
    Discrete Event Simulation des Karussells.
    Modelliert: Rotationszeit, Stations-Sequenzierung, Timing.
    """
    ROTATION_TIME_S = 3.0
    STATION_COUNT = 4

    def simulate_cycle(self, protocol: list[StationAction]) -> CycleResult:
        """
        Simuliert einen vollständigen Messzyklus.
        protocol = [Dispense(...), Swirl(...), UV(...), Measure(...)]
        """
        total_time_s = 0.0
        sample_state = SampleState()

        for action in protocol:
            # Rotation zur Station
            total_time_s += self.ROTATION_TIME_S

            # Prozess an der Station
            station_result = action.execute(sample_state)
            sample_state.update(station_result)
            total_time_s += station_result.duration_s

        return CycleResult(
            total_time_s=total_time_s,
            final_state=sample_state,
        )
```

<!-- @section id="4.4" title="Schicht 2: ODEs — Photobleaching-Kinetik" type="prose" -->
### §4.4 Schicht 2: ODEs — Photobleaching-Kinetik

<!-- @contract name="PhotobleachingODE" type="python" section="4.4" -->
```python
class PhotobleachingODE:
    """
    Lumped-Parameter-Modell für Fluorescein-Photobleaching.
    dF/dt = -k_bleach * I_uv * F
    → Exponentieller Zerfall der Fluoreszenz
    """
    # Kalibrierbare Parameter
    K_BLEACH = 1.2e-3       # s⁻¹ (pro UV-Einheit)
    QUANTUM_YIELD = 0.92    # Fluorescein
    EPSILON = 83000.0       # M⁻¹cm⁻¹ (Extinktionskoeffizient)
    PATH_LENGTH_CM = 0.3    # cm (Schalenhöhe)

    def simulate_bleaching(
        self,
        concentration_uM: float,
        uv_duration_s: float,
        uv_intensity_percent: float,
        ph: float,
    ) -> FluorescenceResult:
        """
        Berechnet die Fluoreszenz-Intensität nach UV-Belichtung.
        """
        # pH-abhängiger Extinktionskoeffizient
        # Fluorescein: pKa ≈ 6.4
        pKa = 6.4
        epsilon_eff = self.EPSILON / (1 + 10**(pKa - ph))

        # Initiale Fluoreszenz (vereinfacht)
        F0 = concentration_uM * 1e-6 * self.QUANTUM_YIELD * epsilon_eff * self.PATH_LENGTH_CM

        # Photobleaching-Rate
        I_uv = uv_intensity_percent / 100.0
        k = self.K_BLEACH * I_uv

        # Exponentieller Zerfall
        import math
        F_t = F0 * math.exp(-k * uv_duration_s)

        return FluorescenceResult(
            initial_fluorescence=F0,
            final_fluorescence=F_t,
            decay_fraction=1.0 - (F_t / F0) if F0 > 0 else 0.0,
        )

    def simulate_fluorescence_signal(
        self,
        concentration_uM: float,
        ph: float,
        excitation_nm: int = 488,
        emission_nm: int = 520,
    ) -> float:
        """
        Berechnet das erwartete Fluoreszenz-Signal (Photonenzählung).
        """
        pKa = 6.4
        epsilon_eff = self.EPSILON / (1 + 10**(pKa - ph))

        # Vereinfachtes Signal-Modell
        signal_photons = (
            concentration_uM * 1e-6
            * self.QUANTUM_YIELD
            * epsilon_eff
            * self.PATH_LENGTH_CM
            * 1e6  # Skalierung auf Photonenzählung
        )
        return signal_photons
```

<!-- @section id="4.5" title="Schicht 3: Rauschmodelle" type="prose" -->
### §4.5 Schicht 3: Rauschmodelle

<!-- @contract name="CarouselNoiseModel" type="python" section="4.5" -->
```python
class CarouselNoiseModel:
    """
    Stochastische Rauschmodelle für den Karussell-Twin.
    """
    # Kalibrierbare Parameter
    CAMERA_READ_NOISE = 5.0       # e⁻ (RMS)
    CAMERA_DARK_CURRENT = 0.1     # e⁻/s
    PIPETTE_CV_PERCENT = 2.0      # % (Coefficient of Variation)
    LED_INTENSITY_DRIFT = 0.5     # % pro Stunde
    UV_INTENSITY_DRIFT = 1.0      # % pro Stunde

    def apply_camera_noise(self, signal_photons: float) -> float:
        """Poisson-Rauschen + Read-Noise + Dark Current."""
        import numpy as np
        poisson_noise = np.random.poisson(max(0, int(signal_photons)))
        read_noise = np.random.normal(0, self.CAMERA_READ_NOISE)
        return max(0, poisson_noise + read_noise)

    def apply_pipette_noise(self, volume_target_ml: float) -> float:
        """Normalverteilung für Pipettier-Ungenauigkeit."""
        import numpy as np
        sigma = self.PIPETTE_CV_PERCENT / 100.0 * volume_target_ml
        return np.random.normal(volume_target_ml, sigma)

    def apply_uv_drift(self, intensity_percent: float, elapsed_hours: float) -> float:
        """Langzeit-Drift der UV-LED."""
        import numpy as np
        drift = np.random.normal(0, self.UV_INTENSITY_DRIFT * elapsed_hours)
        return max(0, intensity_percent + drift)
```

<!-- @section id="4.6" title="Kalibrierbare Parameter (Übersicht)" type="prose" -->
### §4.6 Kalibrierbare Parameter (Übersicht)

<!-- @table schema="calibratable_parameters" -->
| Parameter | Schicht | Bedeutung | Literaturwert | Kalibrierbar? |
|-----------|---------|-----------|---------------|---------------|
| K_BLEACH | ODE | Photobleaching-Rate | ~10⁻³ s⁻¹ | ✅ |
| QUANTUM_YIELD | ODE | Quantenausbeute Fluorescein | 0.92 | ✅ |
| EPSILON | ODE | Extinktionskoeffizient | 83 000 M⁻¹cm⁻¹ | ✅ |
| PATH_LENGTH_CM | ODE | Optische Pfadlänge | 0.3 cm | ✅ |
| CAMERA_READ_NOISE | Rauschen | Kamera-Rauschen | ~5 e⁻ | ✅ |
| PIPETTE_CV_PERCENT | Rauschen | Pipettier-Ungenauigkeit | 2% CV | ✅ |
| LED_INTENSITY_DRIFT | Rauschen | LED-Drift | 0.5%/h | ✅ |
| UV_INTENSITY_DRIFT | Rauschen | UV-Drift | 1%/h | ✅ |
| ROTATION_TIME_S | DES | Rotationszeit | 3.0 s | ✅ |

<!-- @section id="5" title="Experiment: Fluorescein-Photobleaching" type="prose" -->
## §5 Experiment: Fluorescein-Photobleaching

<!-- @section id="5.1" title="Chemischer Hintergrund" type="prose" -->
### §5.1 Chemischer Hintergrund

Reaktion: Fluorescein + UV (365 nm) → Photobleaching (irreversibel)

```
Fluorescein (fluoreszierend) + hν → Photoprodukte (nicht-fluoreszierend)
```

Messgröße: Fluoreszenz-Intensität bei 520 nm (Anregung 488 nm)

Erwartung: Exponentieller Abfall der Fluoreszenz mit UV-Dauer

<!-- @section id="5.2" title="Parameter-Raum (für Atlas/ML-Optimierung)" type="prose" -->
### §5.2 Parameter-Raum (für Atlas/ML-Optimierung)

<!-- @table schema="parameter_space" -->
| Dimension | Typ | Bereich | Einheit | Beschreibung |
|-----------|-----|---------|---------|--------------|
| fluorescein_conc | kontinuierlich | 1–50 | µM | Fluorescein-Konzentration |
| uv_duration | kontinuierlich | 10–600 | s | UV-Belichtungsdauer |
| uv_intensity | kontinuierlich | 10–100 | % | UV-Intensität |
| ph_value | kontinuierlich | 7–13 | pH | pH-Wert der Lösung |
| measure_delay | kontinuierlich | 0–300 | s | Verzögerung vor Messung |

<!-- @section id="5.3" title="ObjectiveFamily (für Atlas)" type="contract" contract="ObjectiveFamily" -->
### §5.3 ObjectiveFamily (für Atlas)

<!-- @ref target="foundation/CONTRACTS.md §6.10.10" type="contract" -->
→ Siehe CONTRACTS §6.10.10 für den ObjectiveFamily-Vertrag.

<!-- @contract name="ObjectiveFamily_fluorescein" type="pydantic" section="5.3" -->
```python
ObjectiveFamily(
    objective_family_id="fluorescein-photobleaching-v1",
    name="Fluorescein Photobleaching Optimierung",
    metrics=[
        MetricDefinition(
            metric_id="fluorescence_decay_rate",
            display_name="Fluoreszenz-Zerfallsrate",
            direction=MetricDirection.MAXIMIZE,
            weight=0.6,
            tolerance=0.05,
            unit="fraction/s",
        ),
        MetricDefinition(
            metric_id="signal_to_noise",
            display_name="Signal-zu-Rausch-Verhältnis",
            direction=MetricDirection.MAXIMIZE,
            weight=0.4,
            tolerance=1.0,
            unit="dB",
        ),
    ],
    constraints=[
        MetricConstraint(
            metric_id="fluorescein_conc",
            operator=ConstraintOperator.LE,
            value=50.0,  # Nicht zu konzentriert (Inner-Filter-Effekt)
        ),
    ],
    priority_mode=PriorityMode.WEIGHTED_SUM,
)
```

<!-- @section id="5.4" title="Ablauf auf dem Karussell" type="dataflow" dataflow="carousel_experiment_flow" -->
### §5.4 Ablauf auf dem Karussell

<!-- @dataflow id="carousel_experiment_flow" trigger="QUESTOR_START" source_role="questor" target_role="hal_interface" -->

<!-- @dataflow-step order="1" -->
ZYKLUS 1: Probenzugabe
   ├─ carousel.rotate(target_position=0)     # Zur Station S1
   ├─ pump.dispense(volume_ml=2.0, flow_rate_ml_min=1.0)
   │   → Fluorescein-Lösung (variable Konzentration)
   └─ pump.dispense(volume_ml=0.5, flow_rate_ml_min=0.5)
       → NaOH-Lösung (pH-Einstellung)

<!-- @dataflow-step order="2" -->
ZYKLUS 2: Mischen
   ├─ carousel.rotate(target_position=1)     # Zur Station S2
   └─ carousel.swirl(duration_s=15, intensity=MEDIUM)
       → Homogenisierung

<!-- @dataflow-step order="3" -->
ZYKLUS 3: UV-Belichtung
   ├─ carousel.rotate(target_position=2)     # Zur Station S3
   └─ uv.expose(duration_s=variable, intensity_percent=variable)
       → Photobleaching läuft ab

<!-- @dataflow-step order="4" -->
ZYKLUS 4: Fluoreszenz-Messung
   ├─ carousel.rotate(target_position=3)     # Zur Station S4
   └─ fluorometer.measure(excitation_nm=488, emission_nm=520, exposure_ms=100)
       → Fluoreszenz-Intensität wird gemessen

<!-- @dataflow-step order="5" -->
ZYKLUS 5: Entsorgung
   └─ carousel.discard()
       → Einweg-Schale wird verworfen

<!-- @section id="5.5" title="LoopTemplate (Questor)" type="contract" contract="LoopTemplate" -->
### §5.5 LoopTemplate (Questor)

<!-- @ref target="foundation/CONTRACTS.md §5.1" type="contract" -->
→ Siehe CONTRACTS §5.1 für den LoopTemplate-Vertrag.

<!-- @contract name="LoopTemplate_fluorescein_photobleaching" type="yaml" section="5.5" -->
```yaml
template_id: fluorescein_photobleaching_v1
template_version: "1.0"
schema_version: "1.0"
domain: chemie
created_by: SYSTEM_INTEGRATOR
created_at: "2026-08-21T00:00:00Z"
last_modified: "2026-08-21T00:00:00Z"
objective_types: [OPTIMIZE, EXPLORE, VALIDATE]
description: "Fluorescein-Photobleaching auf dem Karussell-MVP"
# ── CT-08: Digital-Twin-Referenz hinzugefügt ──
digital_twin_ref: "carousel-fluorescein-photobleaching-v1"
# ── CT-09: twin_pairing_mode entfernt; Planungszeit-Entscheidung durch Quartiermeister ──
required_capabilities:
  - carousel.rotate
  - pump.dispense
  - carousel.swirl
  - uv.expose
  - fluorometer.measure
required_slot_count: 5  # ← CT-04: Transport-Slot hinzugefügt
requires_physical_actuation: true
requires_long_running_process: false
is_recovery_template: false
# ── CT-06: parameter_schema definiert ──
parameter_schema:
  fluorescein_volume_ml:
    type: FLOAT
    required: true
    min: 0.1
    max: 10.0
    unit: mL
    description: "Volumen der Fluorescein-Lösung"
  uv_duration_s:
    type: FLOAT
    required: true
    min: 10.0
    max: 600.0
    unit: s
    description: "UV-Belichtungsdauer"
  uv_intensity_percent:
    type: FLOAT
    required: true
    min: 10.0
    max: 100.0
    unit: "%"
    description: "UV-Intensität"
steps:
  - step_id: rotate_to_dispense
    step_type: HAL_COMMAND
    capability: carousel.rotate
    operation: ROTATE_TO_POSITION
    parameters: {target_position: 0}
    timeout_s: 15.0
    cost: {time_cost_s: 3.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.01}
  - step_id: dispense_fluorescein
    step_type: HAL_COMMAND
    capability: pump.dispense
    operation: DISPENSE
    parameters:
      volume_ml: "{{fluorescein_volume_ml}}"
      flow_rate_ml_min: 1.0
    timeout_s: 60.0
    cost: {time_cost_s: 30.0, reagent_cost: 0.05, compute_cost: 0.0, energy_cost: 0.01}
  - step_id: rotate_to_mix
    step_type: HAL_COMMAND
    capability: carousel.rotate
    operation: ROTATE_TO_POSITION
    parameters: {target_position: 1}
    timeout_s: 15.0
    cost: {time_cost_s: 3.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.01}
  - step_id: swirl_mix
    step_type: HAL_COMMAND
    capability: carousel.swirl
    operation: SWIRL
    parameters:
      duration_s: 15.0
      intensity: MEDIUM
    timeout_s: 120.0
    cost: {time_cost_s: 15.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.01}
  - step_id: rotate_to_uv
    step_type: HAL_COMMAND
    capability: carousel.rotate
    operation: ROTATE_TO_POSITION
    parameters: {target_position: 2}
    timeout_s: 15.0
    cost: {time_cost_s: 3.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.01}
  # ── CT-02: UV-Step von HAL_COMMAND auf PROCESS_COMMAND geändert ──
  - step_id: uv_expose
    step_type: PROCESS_COMMAND
    capability: uv.expose
    operation: EXPOSE
    process_mode: START
    parameters:
      duration_s: "{{uv_duration_s}}"
      intensity_percent: "{{uv_intensity_percent}}"
    timeout_s: 60.0  # ← CT-01: RPC-Timeout, nicht Prozess-Dauer
    expected_process_duration_s: "{{uv_duration_s}}"  # ← CT-02: Prozess-Dauer
    on_lease_expiry_policy: ABORT_TO_SAFE_STATE  # ← CT-13
    # ── CT-07: StageReleasePolicy für K-03 ──
    stage_release_policy:
      stages:
        - stage_id: uv_expose
          release_required: CONDITIONAL
          release_authority: SAFETY_PROCESS_OR_HUMAN
          auto_start_allowed: CONDITIONAL
          release_condition:
            parameter: duration_s
            operator: GT
            threshold: 3000.0
            when_true:
              release_required: true
              auto_start_allowed: false
            when_false:
              release_required: false
              auto_start_allowed: true
    cost: {time_cost_s: 60.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.05}
  - step_id: rotate_to_measure
    step_type: HAL_COMMAND
    capability: carousel.rotate
    operation: ROTATE_TO_POSITION
    parameters: {target_position: 3}
    timeout_s: 15.0
    cost: {time_cost_s: 3.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.01}
  - step_id: measure_fluorescence
    step_type: HAL_COMMAND
    capability: fluorometer.measure
    operation: MEASURE
    parameters:
      excitation_nm: 488
      emission_nm: 520
      exposure_ms: 100
    timeout_s: 30.0
    cost: {time_cost_s: 10.0, reagent_cost: 0.0, compute_cost: 0.01, energy_cost: 0.01}
  - step_id: evaluate_result
    step_type: EVALUATE
    depends_on: [measure_fluorescence]
    timeout_s: 5.0
    cost: {time_cost_s: 1.0, reagent_cost: 0.0, compute_cost: 0.0, energy_cost: 0.0}
max_internal_iterations: 1
# ── CT-12: max_step_retries auf 0 gesetzt ──
on_step_failure: ABORT_LOOP
max_step_retries: 0
termination_conditions:
  - condition_id: all_steps_completed
    metric: null
    operator: null
    threshold: null
# ── CT-18: estimated_cost als Puffer gekennzeichnet ──
estimated_cost:
  total_time_s: 216.0  # Puffer: (128 + 60 + 12) × 1.2 ≈ 240, konservativ 216
  total_reagent_cost: 0.05
  total_compute_cost: 0.01
  total_energy_cost: 0.12
  cost_calculation: DYNAMIC  # Kennzeichnung: Kosten sind parameterabhängig
```

<!-- @section id="6" title="Atlas-Zonen (Initial)" type="prose" -->
## §6 Atlas-Zonen (Initial)

<!-- @section id="6.1" title="Zonen-Definition" type="prose" -->
### §6.1 Zonen-Definition

<!-- @ref target="foundation/CONTRACTS.md §6.10.7" type="contract" -->
→ Siehe CONTRACTS §6.10.7 für den AtlasZoneSummary-Vertrag.

<!-- @table schema="zone_definitions" -->
| Zone-ID | Beschreibung | Dimensionen | Initialzustand |
|---------|--------------|-------------|---------------|
| conc-low | Niedrige Konzentration (1–10 µM) | fluorescein_conc | UNEXPLORED |
| conc-mid | Mittlere Konzentration (10–30 µM) | fluorescein_conc | UNEXPLORED |
| conc-high | Hohe Konzentration (30–50 µM) | fluorescein_conc | UNEXPLORED |
| uv-short | Kurze UV-Belichtung (10–60 s) | uv_duration | UNEXPLORED |
| uv-mid | Mittlere UV-Belichtung (60–300 s) | uv_duration | UNEXPLORED |
| uv-long | Lange UV-Belichtung (300–600 s) | uv_duration | UNEXPLORED |
| uv-int-low | Niedrige UV-Intensität (10–40 %) | uv_intensity | UNEXPLORED |
| uv-int-mid | Mittlere UV-Intensität (40–70 %) | uv_intensity | UNEXPLORED |
| uv-int-high | Hohe UV-Intensität (70–100 %) | uv_intensity | UNEXPLORED |
| ph-neutral | Neutraler pH (7–9) | ph_value | UNEXPLORED |
| ph-basic | Basischer pH (9–11) | ph_value | UNEXPLORED |
| ph-strong-basic | Stark basischer pH (11–13) | ph_value | UNEXPLORED |
| delay-none | Keine Verzögerung (0–30 s) | measure_delay | UNEXPLORED |
| delay-short | Kurze Verzögerung (30–120 s) | measure_delay | UNEXPLORED |
| delay-long | Lange Verzögerung (120–300 s) | measure_delay | UNEXPLORED |

Regel: Alle 5 Dimensionen des Parameter-Raums sind abgedeckt (→ CT-16).

<!-- @section id="6.2" title="FrontierEngine-Trigger" type="prose" -->
### §6.2 FrontierEngine-Trigger

<!-- @ref target="specs/GREMIUM.md §6.10" type="spec" -->
→ Siehe GREMIUM.md §6.10 für die FrontierEngine-Spezifikation.

Nach jedem Experiment wird die FrontierEngine aktualisiert:
Weißraum-Zonen → `WEISSRAUM`-Frontier
Zonen mit hohem `uncertainty_score` → `DEEP_UNCERTAIN`-Frontier
Zonen mit niedrigem `fracture_score` und hoher `support_confidence` → `LOW_COST_FRONTIER`

<!-- @section id="7" title="Sicherheitsregeln (Karussell-spezifisch)" type="prose" -->
## §7 Sicherheitsregeln (Karussell-spezifisch)

<!-- @table schema="carousel_safety_rules" -->
| # | Regel | CHARTER-Referenz |
|---|-------|-----------------|
| K-01 | UV-Belichtung nur bei geschlossenem Gehäuse (Interlock) | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |
| K-02 | Karussell-Stop bei geöffnetem Gehäuse | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |
| K-03 | Keine UV-Belichtung > 3600 s ohne menschliche Freigabe | <!-- @ref target="CHARTER §SR-11" type="security-rule" -->SR-11 |
| K-04 | NaOH-Konzentration ≤ 0.1 M (Sicherheitsgrenze) | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->SR-10 |
| K-05 | Einweg-Schale wird nach jedem Experiment verworfen | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->SR-10 |
| K-06 | Fluorescein-Konzentration ≤ 50 µM (Inner-Filter-Effekt) | <!-- @ref target="CHARTER §SR-10" type="security-rule" -->SR-10 |
| K-07 | ESTOP stoppt Karussell UND UV-LED sofort | <!-- @ref target="CHARTER §SR-09" type="security-rule" -->SR-09 |
| K-08 | Keine physische Ausführung in SANDBOX-Modus | <!-- @ref target="CHARTER §SR-35" type="security-rule" -->SR-35 |

<!-- @section id="7.1" title="K-03 Software-Durchsetzung" type="prose" -->
### §7.1 K-03 Software-Durchsetzung

Die StageReleasePolicy im UV-Step (§5.5) erzwingt K-03 software-seitig:
Wenn `duration_s > 3000.0`: `release_required = true`, `auto_start_allowed = false`
Wenn `duration_s <= 3000.0`: `release_required = false`, `auto_start_allowed = true`

Die HAL-Bridge wertet die Bedingung aus und setzt die tatsächlichen `bool`-Werte, bevor der `ProcessCommand` an HAL gesendet wird.

<!-- @section id="8" title="Dummy-HAL-Konfiguration" type="prose" -->
## §8 Dummy-HAL-Konfiguration

<!-- @section id="8.1" title="Simulationsverhalten" type="prose" -->
### §8.1 Simulationsverhalten

<!-- @role id="carousel_dummy_hal" layer="1" llm="false" writes_to="dummy_results" reads_from="dummy_commands" -->
Für Tests ohne echte Hardware (SANDBOX / DEV_SANDBOX_ONLY):

<!-- @contract name="CarouselDummyHAL" type="python" section="8.1" -->
```python
class CarouselDummyHAL:
    """
    Dummy-HAL für das Karussell-MVP.
    Simuliert alle Stationen deterministisch.
    """
    def execute_command(self, command: HALCommand) -> HALCommandResult:
        if command.capability == "carousel.rotate":
            return self._simulate_rotation(command)
        elif command.capability == "pump.dispense":
            return self._simulate_dispense(command)
        elif command.capability == "carousel.swirl":
            return self._simulate_swirl(command)
        elif command.capability == "uv.expose":
            return self._simulate_uv(command)
        elif command.capability == "fluorometer.measure":
            return self._simulate_measurement(command)
        else:
            # ← CT-15: UNKNOWN_CAPABILITY durch COMMAND_INVALID ersetzt
            return HALCommandResult(
                command_id=command.command_id,
                status="DENIED",
                error_code="COMMAND_INVALID",
                error_class="OPERATIONAL",
            )

    def _simulate_measurement(self, command: HALCommand) -> HALCommandResult:
        """
        Simuliert eine Fluoreszenz-Messung.
        Verwendet das Twin-Modell für die Signalberechnung.
        """
        # Twin-Modell aufrufen
        twin = PhotobleachingODE()
        signal = twin.simulate_fluorescence_signal(
            concentration_uM=self._current_concentration,
            ph=self._current_ph,
        )

        # Rauschen anwenden
        noise = CarouselNoiseModel()
        noisy_signal = noise.apply_camera_noise(signal)

        return HALCommandResult(
            command_id=command.command_id,
            status="SUCCESS",
            slot_state=SlotState(slot_id="carousel-fluorometer", status="FREE", ...),
            operational_metrics={"fluorescence_photons": noisy_signal},
        )
```

<!-- @section id="8.1.1" title="Dummy-HAL-Zustandsvariablen (CT-17)" type="prose" -->
#### §8.1.1 Dummy-HAL-Zustandsvariablen (CT-17)

<!-- @contract name="CarouselDummyHALState" type="python" section="8.1.1" -->
```python
class CarouselDummyHALState:
    """
    Interner Zustand des Dummy-HAL.
    Simuliert den Probenzustand über mehrere Kommandos hinweg.
    """
    current_concentration_uM: float = 0.0
    current_ph: float = 7.0
    current_volume_ml: float = 0.0
    uv_dose_j_cm2: float = 0.0
    is_mixed: bool = False
    carousel_position: int = 0  # 0=S1, 1=S2, 2=S3, 3=S4
```

Regeln:
- Die Zustandsvariablen werden durch HAL-Kommandos aktualisiert:
  - `pump.dispense` → `current_concentration_uM`, `current_ph`, `current_volume_ml`
  - `carousel.swirl` → `is_mixed = True`
  - `uv.expose` → `uv_dose_j_cm2 += dose`
  - `carousel.rotate` → `carousel_position = target_position`
- Die Zustandsvariablen werden NICHT an Questor oder das Gremium weitergegeben. Sie sind rein intern.
- Die Zustandsvariablen werden bei jedem neuen Paket zurückgesetzt.

<!-- @section id="8.2" title="Simulierbare Fehlermodi" type="prose" -->
### §8.2 Simulierbare Fehlermodi

Der Dummy-HAL muss folgende Fehler simulieren können:
- `COMMAND_TIMEOUT` (UV-Belichtung dauert zu lange)
- `SLOT_UNAVAILABLE` (Station ist besetzt)
- `PARAMETER_INVALID` (Volumen außerhalb Bounds)
- `ESTOP` (Not-Aus)

<!-- @section id="9" title="Implementierungsphasen" type="implementation-phase" -->
## §9 Implementierungsphasen

<!-- @table schema="implementation_phases" -->
| Phase | Aufgabe | Dauer | Abhängigkeit |
|-------|---------|-------|--------------|
| C-1 | HAL-Slots + MutexZone definieren | 1 Tag | CONTRACTS §3 |
| C-2 | Capability-Registry (7 Capabilities) | 1 Tag | C-1 |
| C-3 | Dummy-HAL implementieren | 2 Tage | C-1, C-2 |
| C-4 | Twin-Modell (ODE + Rauschen) | 2 Tage | C-1 |
| C-5 | LoopTemplate (fluorescein_photobleaching_v1) | 1 Tag | C-2 |
| C-6 | End-to-End-Test (SANDBOX) | 2 Tage | C-3, C-4, C-5 |
| C-7 | Erste echte Messung (Station S4) | 1 Tag | C-6, Hardware |
| Gesamt | | ~10 Tage | |

<!-- @section id="10" title="Dokumentenhierarchie" type="prose" -->
## §10 Dokumentenhierarchie

Dieses Dokument steht in der Schicht `specs/` und referenziert:
- `foundation/CHARTER.md` für Sicherheitsregeln (CHARTER §SR-XX)
- `foundation/CONTRACTS.md` für Datenverträge (CONTRACTS §3, §5, §6.10.19–20)
- `specs/HAL.md` für HAL-Spezifikation
- `specs/QUESTOR.md` für Questor-LoopTemplates und Capability-Registry
- `specs/GREMIUM.md` für Atlas-Zonen und FrontierEngine
- `specs/GREMIUM_STRATEGY.md` für Achsen-Steuerung und Briefing

Regel: Änderungen an Karussell-Modulen in diesem Dokument erfordern eine Versionsänderung und eine Überprüfung der referenzierten Dokumente.