# resQroute — Technical Architecture & Engineering Blueprint

> **SIH Problem Statement SIH26191**: Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations

`resQroute` is a **Web-First**, real-time disaster-response, relocation, and shelter-intelligence platform built on the foundational thesis:

**SHORTEST ROUTE ≠ SAFEST ROUTE**

During natural disasters (floods, landslides, storm surges), a shelter may technically exist and have open space, but citizens may be unable to reach or use it because road segments are submerged, bridges are compromised, or physical route attributes violate accessibility requirements. `resQroute` replaces conventional shortest-path routing with **Risk-Aware, Accessibility-Aware, and Capacity-Aware Relocation Recommendations**.

---

## 1. Primary Core Principles

1. **Shortest Route ≠ Safest Route**: Safety constraints, water level overlays, and hard road closures strictly override simple distance optimization.
2. **AI Assists — Validated Data & Deterministic Routing Decide**: Machine learning models (NLP classifiers, computer vision) act exclusively as shadow proposal generators. They **never** mutate graph edge states directly without policy verification or authority approval.
3. **SMS Provides a Fallback Communication Channel — resQroute Provides the Intelligence**: SMS enables compact text payload exchange over degraded 2G networks when web data drops.
4. **Append-Only Shelter Capacity**: Occupancy updates are processed as immutable, source-stamped event streams with optimistic locking and materialized availability views displaying `"Reported at [timestamp]"`.

---

## 2. Repository Documentation Structure

```
.
├── docs/                               # SOURCE OF TRUTH DOCUMENTATION
│   ├── ARCHITECTURE.md                 # High-level architecture, component responsibilities, OSRM overlay engine
│   ├── DATA_ARCHITECTURE.md            # PostgreSQL + PostGIS DDL schemas, spatial indexes, append-only capacity
│   ├── DECISIONS.md                    # ADR-001 through ADR-010 (Web-first, PostGIS, Deterministic Overlay, etc.)
│   ├── RELATIONSHIP_GRAPH.md           # System dependency graphs, Mermaid flowcharts, entity relationships
│   ├── DESIGN_REVIEW.md                # Crisis usability inspection, cognitive load, emergency UI patterns
│   ├── CONTENT.md                      # UI text copy, alerts, SMS payload templates, button labels
│   ├── DESIGN.md                       # Design system tokens, emergency color semantic system
│   ├── EMOTIONAL_FLOW.md               # User psychological journey during active disaster evacuations
│   ├── UX_DECISIONS.md                 # Rationale for Everyday vs Disaster Mode, accessibility priority
│   ├── API_CONTRACT.md                 # Comprehensive REST & WebSocket OpenAPI contracts
│   ├── THREAT_MODEL.md                 # STRIDE cybersecurity threat analysis & privacy boundaries
│   ├── RUNBOOK.md                      # Operational runbooks for outages, stale data, moderation surges
│   └── TEST_SCENARIOS.md               # 5 disaster test suites & behavioral safety assertions
├── diagrams/                           # 12 crisp visual PNG architecture diagrams
│   ├── diagram_01_system_overview.png
│   ├── diagram_02_data_flow_ingestion.png
│   ├── diagram_03_hazard_lifecycle_confidence.png
│   ├── diagram_04_routing_decision_overlay.png
│   ├── diagram_05_shelter_ranking_accessibility.png
│   ├── diagram_06_vulnerability_model.png
│   ├── diagram_07_offline_sms_architecture.png
│   ├── diagram_08_ml_guardrails_pipeline.png
│   ├── diagram_09_authority_audit_workflow.png
│   ├── diagram_10_security_rbac_architecture.png
│   ├── diagram_11_postgis_er_diagram.png
│   └── diagram_12_mvp_phased_roadmap.png
├── source/                             # GENERATOR SCRIPTS & CODE ENGINES
│   ├── generate_diagrams.py            # Python script generating all 12 essential visual diagrams
│   └── build_pdf.py                    # ReportLab script compiling master PDF deliverable
├── images/                             # Branding assets and visual graphics
├── references/                         # Citations and official documentation links
├── README.md                           # Master repository guide
└── resQroute_Technical_Architecture_and_Implementation_Guide.pdf # Master PDF deliverable
```

---

## 3. How to Reproduce & Regenerate Deliverables

### Prerequisites
- Python 3.10+
- Installed virtual environment with dependencies (`matplotlib`, `pillow`, `reportlab`)

### Step 1: Regenerate Architecture Diagrams
```bash
./venv/bin/python source/generate_diagrams.py
```
*Output*: Generates all 12 high-resolution architecture diagrams in `./diagrams/`.

### Step 2: Recompile Technical Architecture PDF
```bash
./venv/bin/python source/build_pdf.py
```
*Output*: Compiles `resQroute_Technical_Architecture_and_Implementation_Guide.pdf`.

---

## 4. Scope Classification Summary

| Feature / Component | Scope Classification | Notes |
| :--- | :--- | :--- |
| **Responsive Web Map Platform** | `[MVP]` | React + TypeScript + Leaflet / MapLibre |
| **PostGIS Dynamic Overlay Engine**| `[MVP]` | OSRM candidate routing + PostGIS ST_Intersects overlay filter |
| **Append-Only Shelter Capacity** | `[MVP]` | Event-stream updates with materialized view |
| **Authority Command Dashboard** | `[MVP]` | Incident moderation, hard closure enforcement & audit events |
| **Simulated SMS Gateway** | `[MVP]` | Web modal simulating SMS parser & text recommendation payload |
| **Shadow ML Classification** | `[ENHANCED]` | Shadow-mode NLP text report classifier |
| **Custom Dynamic Graph Engine** | `[ENHANCED]` | Dynamic edge-reweighting routing service (Valhalla / GraphHopper) |
| **Native Android Companion** | `[ENHANCED]` | Native mobile app with location service & SMS permissions |
| **BLE Mesh Emergency SOS** | `[ADVANCED / FUTURE]` | Experimental peer-to-peer device mesh |

---

## 5. Behavioral Safety Assertions

- **Assertion 1**: Confirmed closed road edges (`is_closed = TRUE`) **MUST NEVER** appear in returned relocation routes.
- **Assertion 2**: Shelters with 100% occupancy or active hazard warnings **MUST NEVER** be recommended to citizens.
- **Assertion 3**: Stale graph overlay states (> 30 minutes without refresh) **MUST** trigger an explicit UI warning banner: `"WARNING: Routing data stale by X minutes."`
- **Assertion 4**: Raw citizen community reports **CANNOT** declare hard closures without policy-qualified evidence or authority confirmation.

---

## 6. License & Hackathon Disclosures

Developed for **Smart India Hackathon (SIH 2026)**.  
All simulation data, weights, and test coordinates are clearly labeled prototype demo assets.
