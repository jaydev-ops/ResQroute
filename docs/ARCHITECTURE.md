# resQroute System Architecture Specification

## Executive Overview & System Objective
`resQroute` is a Web-First, real-time disaster response, relocation, and shelter-intelligence system built for SIH Problem Statement SIH26191 (*Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations*).

The core technical premise of `resQroute` is: **"SHORTEST ROUTE ≠ SAFEST ROUTE"**.

During natural disasters (floods, landslides, storm surges), a shelter may technically exist and have open space, but citizens may be unable to reach or use it because:
- Connecting road segments are submerged or blocked by debris.
- Infrastructure (bridges, culverts) is compromised.
- Physical route attributes (steep incline, stairs, narrow paths) violate accessibility requirements.
- Shelter capacity data is stale or unverified.
- Real-time hazard conditions change faster than static map apps update.

`resQroute` replaces conventional shortest-path distance calculation with **Risk-Aware, Accessibility-Aware, and Capacity-Aware Relocation Recommendations**.

---

## 1. Scope & Feature Classification

Every architectural capability is tagged explicitly according to its implementation phase:

| Component | Scope Classification | Description |
| :--- | :--- | :--- |
| **Responsive Web Platform** | `[MVP]` | Core React + TypeScript + Tailwind CSS web experience |
| **Interactive GIS Map** | `[MVP]` | Leaflet / MapLibre visualization layer |
| **Everyday vs Disaster Mode** | `[MVP]` | Dual-state UI for normal preparation vs active emergency |
| **PostGIS Dynamic Overlay Engine** | `[MVP]` | Spatial intersection filtering of base OSRM routes against closed edges |
| **Append-Only Shelter Capacity** | `[MVP]` | Source-stamped event stream with optimistic locking & materialized current view |
| **Authority Command Dashboard** | `[MVP]` | Incident moderation, hard closure enforcement, & audit event logging |
| **Simulated SMS Fallback** | `[MVP]` | Simulated SMS input modal & compact text response parser for demonstration |
| **Shadow Mode ML Classification** | `[ENHANCED]` | NLP / Image report classification in shadow validation mode |
| **Custom Dynamic Graph Engine** | `[ENHANCED]` | Live edge re-weighting routing service (Valhalla / GraphHopper) |
| **Native Android Mobile App** | `[ENHANCED]` | Kotlin Android application with location polling & native SMS permissions |
| **BLE Mesh Emergency SOS** | `[ADVANCED / FUTURE]` | Peer-to-peer device mesh for zero-connectivity emergency signal hop |
| **Predictive Flood Inundation** | `[ADVANCED / FUTURE]` | Hydrodynamic model integration for predictive hazard polygon generation |
| **Nationwide Multi-Region Cluster**| `[LARGE-SCALE DEPLOYMENT]` | Distributed edge deployment with geo-partitioned PostgreSQL databases |

---

## 2. High-Level Modular Monolith Architecture

For the `[MVP]` phase, `resQroute` adopts a **Modular Monolith** pattern. Microservices are intentionally avoided to eliminate network overhead, distributed tracing complexity, and operational failure modes during hackathon demonstration.

```
                    +---------------------------------------+
                    |          CITIZENS & AUTHORITIES       |
                    |         (React + TypeScript Web)      |
                    +-------------------+-------------------+
                                        |
                                        v
                    +-------------------+-------------------+
                    |         API & WEBSOCKET GATEWAY       |
                    |           (FastAPI + Pydantic)        |
                    +-------------------+-------------------+
                                        |
       +--------------------------------+--------------------------------+
       |                                |                                |
       v                                v                                v
+------+-----------------+    +---------+--------+             +---------+--------+
|   HAZARD & RISK ENGINE |    |  OVERLAY ROUTING |             |  SHELTER ENGINE  |
|  - Confidence Scorer   |    |  - OSRM Candidates           |  - Append-Only Stream|
|  - Spatial De-duplication   |  - PostGIS ST_Intersects      |  - Accessibility Check |
|  - Audit Log Tracking  |    |  - Behavioral Safety          |  - Materialized View |
+------+-----------------+    +---------+--------+             +---------+--------+
       |                                |                                |
       +--------------------------------+--------------------------------+
                                        |
                                        v
                    +-------------------+-------------------+
                    |         DATA & STORAGE LAYER          |
                    |   PostgreSQL 16 + PostGIS 3.4         |
                    |   Redis 7 (Pub/Sub & Route Cache)     |
                    +---------------------------------------+
```

---

## 3. Detailed Component Responsibilities

### 3.1. API & WebSocket Gateway Layer (`FastAPI`)
- Exposes versioned REST endpoints (`/api/v1/`) for authentication, shelter listing, hazard reporting, and route generation.
- Manages authenticated persistent WebSockets (`/ws/v1/events`) backed by Redis Pub/Sub for sub-second hazard and capacity broadcasts.
- Enforces Role-Based Access Control (RBAC) via JWT middleware (`Citizen`, `Authority`, `Responder`, `Admin`).

### 3.2. Hazard & Risk Engine
- Receives raw hazard reports from citizens and authority feeds.
- Executes spatial clustering (`ST_ClusterDBSCAN`) to detect duplicate reports within 100 meters.
- Computes real-time **Hazard Confidence Scores** (0-100) based on source authority, proximity corroboration, and report freshness.
- Writes immutable evidence records to `hazard_evidence` and updates active `road_edge_overlays`.

### 3.3. Deterministic Overlay Routing Engine
- **Step 1 (Candidate Generation)**: Queries OSRM API to fetch $K$-shortest alternative paths between origin coordinates and target shelters.
- **Step 2 (PostGIS Overlay Check)**: Performs `ST_Intersects(route_geometry, buffer(overlay_geometry))` against active closed edges (`is_closed = TRUE` in `road_edge_overlays`).
- **Step 3 (Safety & Attribute Filter)**: Rejects candidate routes intersecting confirmed hard closures or violating accessibility limits (e.g. slope $> 5\%$ for wheelchair users).
- **Step 4 (Deterministic Re-ranking)**: Ranks surviving candidates by safety score, travel time, and road quality.
- **Step 5 (Fail-Safe Assertion)**: If zero routes survive overlay checks, the engine returns **`NO_SAFE_ROUTE_AVAILABLE`** accompanied by specific hazard explanations.

### 3.4. Shelter & Capacity Engine
- Maintains shelter metadata (location, wheelchair ramps, medical power backup, specialized facilities).
- Processes capacity changes exclusively via append-only `shelter_updates` events.
- Evaluates materialized shelter availability in real-time, displaying `"Reported at [timestamp]"` on all client views.

---

## 4. Emergency Communication & Resilience Fallbacks

```
+-----------------------------------------------------------------------+
|                       COMMUNICATION RESILIENCE                        |
+-----------------------------------------------------------------------+
| Level 1: Full Online WebSockets (Real-time live map & socket updates) |
| Level 2: Polling REST API Fallback (5s HTTP fallback when WS drops)   |
| Level 3: Simulated SMS Payload (Compact structured text recommendation) |
| Level 4: Stale Local Cache (IndexedDB offline map tiles + Warning UI) |
+-----------------------------------------------------------------------+
```

### SMS Resilience Design (`[MVP]` Demo / `[ENHANCED]` Native)
In disaster zones with degraded cellular data, citizens cannot open heavy web maps. 
- In `[MVP]`, the web UI features an **SMS Simulation Screen** where structured text commands (`"EMERGENCY LOC 19.0760,72.8777 WHEELCHAIR"`) are processed by backend regex parsers.
- The server extracts coordinates, runs overlay routing, and returns a compact 160-character SMS payload:
  `"resQroute: Safe Shelter B (3.2km). Status: SAFE. Lat:19.0812, Lon:72.8910. Map: https://maps.os.org/s/b. Freshness: 2m ago."`

---

## 5. Architectural Principles & Behavioral Safety Assertions

1. **AI Assists — Deterministic Rules Decide**: Machine learning models (NLP classifiers, computer vision debris detectors) act solely as shadow proposal generators. They **never** mutate graph edge states or declare hard closures directly without policy validation or authority approval.
2. **Behavioral Safety Assertion 1**: Confirmed closed road edges (`is_closed = TRUE`) **MUST NEVER** appear in returned relocation routes.
3. **Behavioral Safety Assertion 2**: Shelters with 100% occupancy or active hazard warnings **MUST NEVER** be recommended to citizens.
4. **Behavioral Safety Assertion 3**: Stale graph overlay states (> 30 minutes without refresh during active disaster) MUST trigger an explicit UI warning banner: `"WARNING: Routing data stale by X minutes."`
