# resQroute API Specification & OpenAPI Contract

Version: `v1.0.0`  
Base URL: `/api/v1`  
Protocol: `HTTPS` / `WSS`

---

## 1. Core Endpoints Overview

### 1.1. Health Check
`GET /api/v1/health`
- **Response `200 OK`**:
```json
{
  "status": "healthy",
  "database": "connected (PostgreSQL 16 + PostGIS 3.4)",
  "redis": "connected",
  "osrm": "connected",
  "timestamp": "2026-08-31T21:46:11Z"
}
```

---

### 1.2. Calculate Safe Evacuation Route
`POST /api/v1/routes/calculate`

- **Request Payload**:
```json
{
  "origin_latitude": 19.0760,
  "origin_longitude": 72.8777,
  "accessibility_profile": {
    "wheelchair_required": true,
    "electricity_required": false,
    "mobility_impaired": false
  },
  "preferred_shelter_id": null
}
```

- **Response `200 OK` (Safe Route Found)**:
```json
{
  "status": "SUCCESS",
  "recommended_shelter": {
    "shelter_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "name": "Shelter B — Community Center",
    "latitude": 19.0812,
    "longitude": 72.8910,
    "available_capacity": 45,
    "total_capacity": 100,
    "occupancy_pct": 55.0,
    "has_wheelchair_ramp": true,
    "reported_at": "2026-08-31T21:44:00Z"
  },
  "route": {
    "distance_meters": 3420,
    "estimated_duration_seconds": 1240,
    "risk_score": 12.5,
    "avoided_hazards_count": 2,
    "geometry_geojson": {
      "type": "LineString",
      "coordinates": [[72.8777, 19.0760], [72.8800, 19.0790], [72.8910, 19.0812]]
    }
  },
  "explanation": "Route B selected. Direct Route A avoided due to verified hard closure at Edge #402 (Submerged road)."
}
```

- **Response `200 OK` (No Safe Route Available)**:
```json
{
  "status": "NO_SAFE_ROUTE_AVAILABLE",
  "recommended_shelter": null,
  "route": null,
  "explanation": "CRITICAL ALERT: All candidate paths to nearby shelters intersect verified flood zones or hard closures. Seek immediate high ground."
}
```

---

### 1.3. Append Shelter Capacity Update
`POST /api/v1/shelters/{id}/capacity`  
*Authorization: Authority / Responder Role*

- **Request Payload**:
```json
{
  "occupied_count": 65,
  "idempotency_key": "evt-20260831-sh02-004",
  "rationale": "Group arrival from Sector 4 bus evacuation"
}
```

- **Response `201 Created`**:
```json
{
  "status": "RECORDED",
  "shelter_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "occupied_count": 65,
  "available_capacity": 35,
  "idempotency_key": "evt-20260831-sh02-004",
  "reported_at": "2026-08-31T21:46:10Z"
}
```

---

### 1.4. Create / Verify Road Edge Closure
`POST /api/v1/hazards/overlay`  
*Authorization: Authority Role*

- **Request Payload**:
```json
{
  "edge_id": 402,
  "is_closed": true,
  "severity_level": "FLOODED",
  "water_depth_cm": 45,
  "rationale": "Water level exceeding safe vehicular/pedestrian clearance"
}
```

- **Response `200 OK`**:
```json
{
  "status": "OVERLAY_ENFORCED",
  "overlay_id": "c71a3d90-8e12-402a-9fbc-123456789abc",
  "edge_id": 402,
  "audit_event_id": "aud-99887766",
  "freshness_ts": "2026-08-31T21:46:11Z"
}
```

---

### 1.5. WebSocket Real-Time Event Bus
`WSS /ws/v1/events`

- **Connection Message**: `{"token": "JWT_BEARER_TOKEN"}`
- **Server Event Payload (Hazard Update)**:
```json
{
  "event_type": "HAZARD_UPDATED",
  "edge_id": 402,
  "is_closed": true,
  "severity": "FLOODED",
  "timestamp": "2026-08-31T21:46:11Z"
}
```
