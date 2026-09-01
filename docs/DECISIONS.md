# resQroute Architectural Decision Records (ADRs)

This document records the critical architectural choices, technical trade-offs, and engineering rationale for `resQroute`.

---

## ADR-001: Web-First Architecture Baseline
- **Status**: Accepted
- **Context**: Disasters require immediate accessibility across desktop command centers, mobile browser users, and authority laptops without requiring app store installation.
- **Alternatives Considered**: Native Android/iOS mobile-first app, Desktop Electron app.
- **Decision**: Build `resQroute` as a Web-First Progressive Web App (PWA) using React + TypeScript + Tailwind CSS. Native mobile companion apps are deferred to Phase 2 (`[ENHANCED]`).
- **Consequences**: Instant accessibility via standard URLs; requires browser-compatible map rendering (Leaflet/MapLibre); SMS inbox reading cannot be performed natively inside standard web browsers and must be simulated in web MVP.

---

## ADR-002: Modular Monolith Framework Choice (FastAPI)
- **Status**: Accepted
- **Context**: The team requires high-performance asynchronous REST and WebSocket handling in Python (for rapid GIS and ML library integration) without microservice deployment friction.
- **Alternatives Considered**: Django REST Framework, Node.js Express, Go Fiber, Microservices architecture.
- **Decision**: Use FastAPI in a **Modular Monolith** pattern.
- **Consequences**: Asynchronous event loop (`async/await`) handles hundreds of concurrent WebSocket connections; Pydantic ensures strict runtime schema validation; single codebase deployment via Docker simplified hackathon evaluation.

---

## ADR-003: Spatial Database Engine (PostgreSQL + PostGIS)
- **Status**: Accepted
- **Context**: Evacuation logic requires complex spatial queries (buffer intersections, radial lookups, spatial clustering, edge geometries).
- **Alternatives Considered**: MongoDB GeoJSON indexes, MySQL Spatial, SQLite Spatialite.
- **Decision**: Standardize on PostgreSQL 16 with PostGIS 3.4 extensions.
- **Consequences**: Provides battle-tested spatial indexes (`GiST`), rich spatial SQL functions (`ST_Intersects`, `ST_DWithin`, `ST_Buffer`), transaction safety for audit logging, and materialized views for shelter capacity caching.

---

## ADR-004: Candidate Route Generation Strategy (OSRM + PostGIS Overlays)
- **Status**: Accepted
- **Context**: Preprocessed OSRM road graphs are extremely fast for distance matrix calculations but static. Dynamic disaster road closures cannot instantly re-weight OSRM graphs without expensive graph re-compilation.
- **Alternatives Considered**: Full dynamic GraphHopper/Valhalla custom edge-reweighting service (`[ENHANCED]`), Pure PostGIS pgRouting (slow for large road networks).
- **Decision**: Use OSRM for fast $K$-shortest candidate route generation, followed by PostGIS dynamic spatial overlay checks (`ST_Intersects`) against active closed edge buffers (`road_edge_overlays`).
- **Consequences**: Combines sub-50ms OSRM route generation with sub-10ms PostGIS hazard overlay rejection; if all OSRM candidates intersect hazards, system safely returns `NO_SAFE_ROUTE_AVAILABLE`.

---

## ADR-005: Deterministic Routing Guardrails over AI-Controlled Routing
- **Status**: Accepted
- **Context**: Emergency evacuation routing is safety-critical. Neural network models and LLMs can hallucinate non-existent roads or recommend submerged paths.
- **Alternatives Considered**: End-to-end RL/LLM pathfinder model.
- **Decision**: AI models are strictly limited to shadow-mode NLP report extraction and hazard confidence scoring. Final evacuation routes are computed strictly by deterministic spatial algorithms and validated safety rules.
- **Consequences**: Guaranteed auditability, explainability, and elimination of AI hallucination risks during life-threatening disaster evacuations.

---

## ADR-006: Append-Only Event Logging for Shelter Capacity
- **Status**: Accepted
- **Context**: Mutable `UPDATE shelters SET occupied = X` queries cause race conditions, lost updates, and lack historical audit trails.
- **Alternatives Considered**: Direct table updates, Redis-only counters.
- **Decision**: Record capacity changes as immutable append-only `shelter_updates` events with optimistic concurrency keys. Expose current capacity via `current_shelter_capacity` materialized view.
- **Consequences**: Complete timestamped lineage for every occupancy change; easy calculation of data freshness (`"Reported at [timestamp]"`); total protection against data corruption.

---

## ADR-007: Dual-State Operating Modes (Everyday vs Disaster Mode)
- **Status**: Accepted
- **Context**: Disaster apps are often abandoned if useless during non-disaster times. Users also suffer cognitive overload if emergency UI elements are shown during normal operation.
- **Alternatives Considered**: Single static emergency dashboard.
- **Decision**: Implement Everyday Mode (preparedness checklists, nearby emergency infrastructure) and Disaster Mode (red zone alerts, live hazard reporting, dynamic rerouting).
- **Consequences**: Increases everyday engagement; Disaster Mode activates cleanly via authority trigger or verified hazard thresholds.

---

## ADR-008: Fallback SMS Architecture Strategy
- **Status**: Accepted
- **Context**: Direct cellular data drops during disasters, breaking web connectivity.
- **Alternatives Considered**: Require active 4G/5G connection at all times, BLE mesh as primary fallback.
- **Decision**: Implement compact text-based SMS payload parsing as the primary communication fallback. Web MVP features a **Simulated SMS Gateway** modal to prove parsing feasibility.
- **Consequences**: Enables lifeline location extraction and shelter recommendation over 2G text networks; native mobile inbox integration deferred to Phase 2 (`[ENHANCED]`).

---

## ADR-009: Vulnerability & Accessibility First-Class Matching
- **Status**: Accepted
- **Context**: Standard emergency shelters frequently lack wheelchair access or medical generator power, endangering vulnerable individuals.
- **Alternatives Considered**: Generic proximity routing without accessibility parameters.
- **Decision**: Embed accessibility constraints (`wheelchair_required`, `electricity_required`) directly into the mandatory filter pipeline before shelter ranking.
- **Consequences**: Prevents vulnerable citizens from being routed to inaccessible shelters; requires minimal user privacy flags without collecting sensitive medical history.

---

## ADR-010: Containerized Micro-Deployment Strategy (Docker Compose)
- **Status**: Accepted
- **Context**: SIH evaluators and developers require instant, zero-configuration local deployment of frontend, backend, PostgreSQL/PostGIS, Redis, and OSRM services.
- **Alternatives Considered**: Manual local service installation, complex Kubernetes manifests.
- **Decision**: Package the entire system into a single `docker-compose.yml` stack with health checks and seeded district demo data.
- **Consequences**: Enables single-command reproducibility (`docker-compose up`); guarantees environment consistency across macOS, Linux, and Windows.
