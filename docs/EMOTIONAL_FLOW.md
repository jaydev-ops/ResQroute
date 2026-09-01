# resQroute Emotional Flow & User Psychology Matrix

## Emotional Architecture
During natural disasters, users transition rapidly through intense emotional states. Interface design must actively alleviate panic, provide unambiguous direction, and build trust at every step.

```
+-------------------------------------------------------------------------------+
|                           USER EMOTIONAL JOURNEY                              |
+-------------------------------------------------------------------------------+
| ANXIETY & CONFUSION -> GUIDANCE & CLARITY -> ACTION & NAVIGATION -> RELIEF   |
+-------------------------------------------------------------------------------+
```

---

## 1. Step-by-Step Emotional Matrix & UI Responses

| Stage | User Psychological State | UI Tone & Design Response | System Action |
| :--- | :--- | :--- | :--- |
| **1. Hazard Discovery** | High Panic, Confusion, Fear | Calm, prominent top alert banner; high contrast red/green visual split | Instantly activates **Disaster Mode UI**; loads cached map tiles |
| **2. Seeking Direction** | Anxiety, Impatience | Single big primary button: **"GET SAFEST ROUTE"**; no form bloat | Automatically pulls GPS / Plus Code; applies user accessibility profile |
| **3. Route Evaluation** | Uncertainty, Skepticism | Transparent safety explanation; explicit list of avoided hazard points | Runs PostGIS overlay check; filters closed edges; selects accessible shelter |
| **4. Active Navigation** | High Focus, Stress | Solid green route line on dark map; large step-by-step direction text | Monitors Redis Pub/Sub WebSocket stream for dynamic edge closures |
| **5. Dynamic Reroute** | Acute Alarm (Road blocked) | Flash warning alert: **"AHEAD ROAD BLOCKED — REROUTING"** | Instantly recalculates alternative safe candidate route |
| **6. Shelter Arrival** | Relief, Exhaustion | Green confirmation screen: **"ARRIVED AT SHELTER B — CHECKED IN"** | Appends `shelter_updates` event; updates occupancy capacity |

---

## 2. Trust-Building Principles
1. **Never Show Unverified Predictions as Absolute Facts**: Distinguish clearly between authority-verified hard closures and unverified citizen reports.
2. **Always Show Data Timestamps**: Display `"Reported 2m ago"` to eliminate doubt about stale shelter occupancy.
3. **Provide Explicit Rejection Rationale**: When a route is rejected, tell the user *why* (e.g. `"Route A avoided: Water depth 45cm reported at Sector 17"`).
