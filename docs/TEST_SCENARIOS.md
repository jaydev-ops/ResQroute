# resQroute Test Scenarios & Safety Verification Suites

## Verification Strategy & Safety Assertions
Emergency relocation algorithms cannot rely solely on standard unit tests. `resQroute` is validated against **Behavioral Safety Assertions** to ensure life-safety guarantees under simulated disaster conditions.

---

## 1. Safety Assertion Test Matrix

| Test Suite ID | Disaster Scenario | Primary Condition | Behavioral Safety Assertion | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TS-001** | Flash Flood Inundation | Road Edge #402 has active `is_closed = TRUE` | **ASSERTION 1**: Edge #402 MUST NEVER appear in candidate route geometry returned to citizen. | `PASSED` |
| **TS-002** | Shelter Overcrowding | Shelter A `occupied_count == total_capacity` | **ASSERTION 2**: Shelter A MUST NEVER be recommended; system must redirect to Shelter B. | `PASSED` |
| **TS-003** | Wheelchair Relocation | User profile `wheelchair_required = TRUE` | **ASSERTION 3**: Returned route MUST NOT contain stairs/steep slopes; target shelter MUST have ramp. | `PASSED` |
| **TS-004** | Degraded Network Sync | Overlays un-updated for 30 minutes | **ASSERTION 4**: System MUST append explicit stale warning banner or return `NO_SAFE_ROUTE`. | `PASSED` |
| **TS-005** | Community Spam Report | Single unverified citizen report created | **ASSERTION 5**: Unverified report CANNOT create hard closure without policy evidence or authority action. | `PASSED` |

---

## 2. End-to-End Disaster Simulation Walkthrough

### Synthetic Test Scenario Setup (District 17 Flood)
- **Time 00:00**: System in Everyday Mode. Shelters A, B, C active with 10% baseline occupancy.
- **Time 05:00**: Heavy rainfall begins. Citizen uploads report: `"Water accumulation near Sector 17 main bridge"`. System assigns status `REPORTED` (Confidence Score: 20).
- **Time 07:00**: Authority verifies hazard on Command Dashboard. Edge #402 marked `is_closed = TRUE`, status elevated to `CONFIRMED` (Confidence Score: 95). `audit_events` logs action.
- **Time 08:00**: Citizen at Sector 17 requests evacuation route with `wheelchair_required = true`.
- **Engine Execution**:
  1. OSRM returns Candidate Route 1 (via Edge #402, 1.2km) and Candidate Route 2 (via High Ridge Road, 2.8km).
  2. PostGIS overlay check detects `ST_Intersects(Candidate Route 1, Edge #402) = TRUE`. Candidate Route 1 is **REJECTED**.
  3. Candidate Route 2 evaluates safe (`ST_Intersects = FALSE`).
  4. Shelter capacity check verifies Shelter B has ramp access and 45 open spaces.
  5. System outputs **Candidate Route 2 -> Shelter B** with explanation: `"Route 1 avoided due to flood closure on Edge #402"`.
- **Time 10:00**: Shelter B receives 45 evacuees. Operator submits append-only update `occupied_count = 100`. Materialized view updates `available_capacity = 0`.
- **Time 11:00**: Subsequent user requests route. System rejects full Shelter B and automatically reroutes to Shelter C (3.5km, open capacity).
- **Time 15:00**: Internet connection drops. Client switches to Simulated SMS fallback, parsing compact text recommendations seamlessly.
