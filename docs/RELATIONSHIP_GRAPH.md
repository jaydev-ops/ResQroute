# resQroute Relationship Graph & System Dependencies

This document details the inter-component relationships, data lineage, and user interaction flows within `resQroute`.

---

## 1. High-Level Service & Component Dependency Graph

```mermaid
graph TD
    subgraph Client Layer
        WebClient[React Web / PWA Client]
        SMSModal[Simulated SMS Modal]
        AuthDash[Authority Command Dashboard]
    end

    subgraph API & WebSocket Layer
        Gateway[FastAPI Gateway]
        AuthMiddleware[JWT / RBAC Middleware]
        WSBus[Redis Pub/Sub WebSocket Bus]
    end

    subgraph Core Processing Engines
        RiskEngine[Hazard & Confidence Engine]
        OverlayEngine[PostGIS Overlay Routing Engine]
        ShelterEngine[Append-Only Shelter Engine]
    end

    subgraph External & Storage Layer
        OSRM[OSRM Routing Service]
        PostGIS[(PostgreSQL + PostGIS)]
        Redis[(Redis Cache)]
    end

    WebClient -->|HTTP REST| Gateway
    AuthDash -->|HTTP REST| Gateway
    SMSModal -->|Simulated Payload| Gateway
    Gateway --> AuthMiddleware
    Gateway <--> WSBus

    AuthMiddleware --> RiskEngine
    AuthMiddleware --> OverlayEngine
    AuthMiddleware --> ShelterEngine

    RiskEngine -->|Write hazard_evidence| PostGIS
    RiskEngine -->|Update road_edge_overlays| PostGIS
    
    OverlayEngine -->|Fetch Candidate Geometries| OSRM
    OverlayEngine -->|ST_Intersects Check| PostGIS
    
    ShelterEngine -->|Write shelter_updates| PostGIS
    ShelterEngine -->|Read Materialized View| PostGIS

    WSBus <-->|Cache & Pub/Sub| Redis
    WSBus -->|Live Broadcasts| WebClient
    WSBus -->|Live Broadcasts| AuthDash
```

---

## 2. End-to-End Emergency Evacuation Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Citizen
    actor Authority
    participant WebUI as React Web Map
    participant API as FastAPI Gateway
    participant DB as PostgreSQL/PostGIS
    participant OSRM as OSRM Engine
    participant Redis as Redis Pub/Sub

    Authority->>WebUI: Moderates & Confirms Flood Hazard on Edge #402
    WebUI->>API: POST /api/v1/hazards/confirm (Edge #402)
    API->>DB: INSERT INTO road_edge_overlays (is_closed=TRUE)
    API->>DB: INSERT INTO audit_events (HARD_CLOSURE_CREATED)
    API->>Redis: PUBLISH event (HAZARD_UPDATED)
    Redis-->>WebUI: Broadcast WebSocket invalidation event
    
    Citizen->>WebUI: Requests Safe Evacuation Route (Wheelchair Profile)
    WebUI->>API: POST /api/v1/routes/calculate (Origin, Wheelchair=True)
    API->>OSRM: Query K-Shortest Candidates to Nearby Shelters
    OSRM-->>API: Return Candidate Geometries (Route A, Route B)
    API->>DB: Query ST_Intersects(Route A, closed road_edge_overlays)
    DB-->>API: Route A intersects Edge #402 (REJECTED)
    API->>DB: Query ST_Intersects(Route B, closed road_edge_overlays)
    DB-->>API: Route B Safe (0 Closed Intersections)
    API->>DB: Query current_shelter_capacity (Wheelchair Ramp = True)
    DB-->>API: Shelter B Accessible & Has Available Capacity (45/100)
    API-->>WebUI: Return Route B + Shelter B Recommendation + Explanation
    WebUI->>Citizen: Renders Safe Route B on Map with Safety Badge
```

---

## 3. Data Entity Relationship Summary

| Entity | Primary Key | Foreign Keys | Relationship Summary |
| :--- | :--- | :--- | :--- |
| `users` | `id` | - | Parent user record holding RBAC role and accessibility flags |
| `source_registry` | `id` | - | Lineage tracking entity defining trust levels for data feeds |
| `road_edge_overlays` | `id` | `source_id` | Stores spatial geometries of closed edges & severity levels |
| `hazard_evidence` | `id` | `source_id` | Stores spatial point reports, confidence scores, and raw evidence payloads |
| `shelters` | `id` | - | Static metadata for shelters (location, total capacity, accessibility flags) |
| `shelter_updates` | `id` | `shelter_id`, `actor_id` | Append-only event stream recording timestamped occupancy changes |
| `audit_events` | `id` | `actor_id` | Immutable security log of authority overrides & closures |
| `route_snapshots` | `id` | `user_id`, `target_shelter_id` | Post-disaster audit snapshot of evaluated geometries & risk scores |
