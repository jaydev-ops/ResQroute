# resQroute Data Architecture & PostGIS Schema Specification

## Data Architecture & Lifecycle Strategy
The `resQroute` data model is engineered around **Geospatial Integrity, Immutable Safety Audits, and Event Lineage**. 

Disaster management applications face severe real-world data issues:
- Stale or conflicting community reports.
- Malicious or accidental false closure claims.
- Concurrency issues when multiple authorities update shelter occupancy simultaneously.
- Lack of auditability when evacuation routes fail.

To resolve these challenges, `resQroute` uses **PostgreSQL 16 with PostGIS 3.4 extensions**, structured around append-only event streams and spatial overlay tables.

---

## 1. Core Data Models & SQL DDL Schemas

```sql
-- Enable PostGIS Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ---------------------------------------------------------
-- 1. USERS & ACCESSIBILITY PROFILES
-- ---------------------------------------------------------
CREATE TYPE user_role AS ENUM ('CITIZEN', 'RESPONDER', 'AUTHORITY', 'ADMIN');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(100) NOT NULL,
    phone_hash VARCHAR(64) UNIQUE NOT NULL,
    role user_role NOT NULL DEFAULT 'CITIZEN',
    wheelchair_required BOOLEAN DEFAULT FALSE,
    electricity_required BOOLEAN DEFAULT FALSE, -- For oxygen concentrators/medical devices
    mobility_impaired BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------
-- 2. SOURCE REGISTRY & LINEAGE
-- ---------------------------------------------------------
CREATE TYPE source_trust_level AS ENUM ('UNTRUSTED_CITIZEN', 'VERIFIED_VOLUNTEER', 'IOT_SENSOR', 'OFFICIAL_AUTHORITY');

CREATE TABLE source_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_name VARCHAR(100) NOT NULL,
    trust_level source_trust_level NOT NULL,
    api_key_hash VARCHAR(64),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------
-- 3. ROAD EDGE OVERLAYS (Dynamic Hazard Overlays)
-- ---------------------------------------------------------
CREATE TABLE road_edge_overlays (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    edge_id BIGINT NOT NULL, -- Corresponds to OSRM / OSM Way ID
    geom GEOMETRY(LineString, 4326) NOT NULL,
    is_closed BOOLEAN NOT NULL DEFAULT FALSE,
    severity_level VARCHAR(20) NOT NULL, -- FLOODED, DEBRIS, STRUCTURAL_DAMAGE, CLOSED
    water_depth_cm INT DEFAULT 0,
    freshness_ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_id UUID REFERENCES source_registry(id),
    policy_version VARCHAR(20) NOT NULL DEFAULT 'v1.0'
);

CREATE INDEX idx_road_edge_geom ON road_edge_overlays USING GIST(geom);
CREATE INDEX idx_road_edge_freshness ON road_edge_overlays(freshness_ts);

-- ---------------------------------------------------------
-- 4. HAZARD EVIDENCE & CONFIDENCE
-- ---------------------------------------------------------
CREATE TABLE hazard_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hazard_id UUID NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    source_id UUID REFERENCES source_registry(id),
    confidence_score FLOAT NOT NULL CHECK (confidence_score BETWEEN 0.0 AND 100.0),
    description TEXT,
    evidence_payload JSONB, -- Stores image S3 URLs, raw text, or sensor readings
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_hazard_evidence_location ON hazard_evidence USING GIST(location);

-- ---------------------------------------------------------
-- 5. SHELTERS & APPEND-ONLY CAPACITY UPDATES
-- ---------------------------------------------------------
CREATE TABLE shelters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    location GEOMETRY(Point, 4326) NOT NULL,
    total_capacity INT NOT NULL CHECK (total_capacity > 0),
    has_wheelchair_ramp BOOLEAN DEFAULT FALSE,
    has_medical_generator BOOLEAN DEFAULT FALSE,
    has_accessible_toilets BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_shelter_location ON shelters USING GIST(location);

-- Append-only Capacity Stream (Atomic updates, optimistic concurrency)
CREATE TABLE shelter_updates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shelter_id UUID NOT NULL REFERENCES shelters(id),
    occupied_count INT NOT NULL CHECK (occupied_count >= 0),
    actor_id UUID REFERENCES users(id),
    idempotency_key VARCHAR(64) UNIQUE NOT NULL,
    reported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_shelter_updates_timeline ON shelter_updates(shelter_id, reported_at DESC);

-- Materialized View for Instant Capacity Retrieval
CREATE MATERIALIZED VIEW current_shelter_capacity AS
SELECT DISTINCT ON (s.id)
    s.id AS shelter_id,
    s.name,
    s.location,
    s.total_capacity,
    COALESCE(su.occupied_count, 0) AS occupied_count,
    (s.total_capacity - COALESCE(su.occupied_count, 0)) AS available_capacity,
    ROUND((COALESCE(su.occupied_count, 0)::NUMERIC / s.total_capacity::NUMERIC) * 100, 2) AS occupancy_pct,
    s.has_wheelchair_ramp,
    s.has_medical_generator,
    s.has_accessible_toilets,
    COALESCE(su.reported_at, s.created_at) AS last_reported_at
FROM shelters s
LEFT JOIN shelter_updates su ON s.id = su.shelter_id
ORDER BY s.id, su.reported_at DESC;

-- ---------------------------------------------------------
-- 6. SYSTEM AUDIT & LINEAGE LOGS
-- ---------------------------------------------------------
CREATE TABLE audit_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id UUID REFERENCES users(id),
    action_type VARCHAR(50) NOT NULL, -- HARD_CLOSURE_CREATED, SHELTER_CAPACITY_OVERRIDE, ROUTE_REJECTED
    affected_entity_id UUID NOT NULL,
    policy_version VARCHAR(20) NOT NULL,
    graph_version VARCHAR(20) NOT NULL,
    rationale TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------
-- 7. ROUTE SNAPSHOTS (Post-Disaster Evaluation)
-- ---------------------------------------------------------
CREATE TABLE route_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    target_shelter_id UUID REFERENCES shelters(id),
    route_geom GEOMETRY(LineString, 4326) NOT NULL,
    risk_score FLOAT NOT NULL,
    graph_version VARCHAR(20) NOT NULL,
    policy_version VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 2. Spatial Query Optimization & Indexing

### 2.1. Spatial Overlays (`ST_Intersects`)
To check if a candidate route intersects any active hard road closures:
```sql
SELECT EXISTS (
    SELECT 1 
    FROM road_edge_overlays r
    WHERE r.is_closed = TRUE
      AND ST_Intersects(r.geom, ST_Buffer(:candidate_route_geom::geography, 10)::geometry)
) AS contains_closed_road;
```

### 2.2. Accessibility Radial Shelter Lookup (`ST_DWithin`)
To find all available shelters within 5 kilometers that fulfill wheelchair requirements:
```sql
SELECT 
    c.shelter_id,
    c.name,
    ST_Distance(c.location::geography, ST_SetSRID(ST_MakePoint(:user_lon, :user_lat), 4326)::geography) AS distance_meters,
    c.available_capacity,
    c.occupancy_pct,
    c.last_reported_at
FROM current_shelter_capacity c
WHERE c.available_capacity > 0
  AND c.has_wheelchair_ramp = TRUE
  AND ST_DWithin(c.location::geography, ST_SetSRID(ST_MakePoint(:user_lon, :user_lat), 4326)::geography, 5000)
ORDER BY distance_meters ASC;
```

---

## 3. Data Lineage, Freshness & TTL Policies

1. **Freshness Timestamping**: Every shelter and road edge response explicitly returns `freshness_ts` and `"reported at [timestamp]"` so clients can identify stale data.
2. **TTL for Unverified Citizen Reports**: Raw citizen reports expire after 6 hours unless corroborated by secondary sources.
3. **Audit Immutability**: `audit_events` and `shelter_updates` tables are strictly append-only. UPDATE and DELETE operations are forbidden via database trigger guards.
