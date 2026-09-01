# resQroute Content & Copywriting Specification

This document contains the standardized UI copy, emergency alert texts, button labels, empty states, confirmation prompts, and SMS payload templates for `resQroute`. 

---

## 1. Primary Action Buttons & Status Badges

| Location | Component | Standardized UI Text |
| :--- | :--- | :--- |
| **Everyday Mode** | Hero Button | `[FIND NEARBY EMERGENCY SHELTERS]` |
| **Disaster Mode** | Primary CTA | `[GET SAFEST EVACUATION ROUTE]` |
| **Hazard Report** | Submit Button | `[REPORT ROAD HAZARD NOW]` |
| **Authority Dashboard**| Action Button | `[VERIFY & ENFORCE HARD CLOSURE]` |
| **Route Result** | Safety Badge | `[VERIFIED SAFE & ACCESSIBLE ROUTE]` |
| **Route Result** | Reject Badge | `[UNSAFE - HAZARD OVERLAY INTERSECTION]` |
| **Shelter Chip** | Available State | `[AVAILABLE: 45 / 100 SPACES - Reported 2m ago]` |
| **Shelter Chip** | Full State | `[AT CAPACITY: 100 / 100 SPACES - DO NOT PROCEED]` |

---

## 2. System Alerts & Warning Messages

### 2.1. Safe Route Recommendation Banner
> **RECOMMENDED ROUTE GENERATED**  
> **Destination**: Shelter B — Community Center (3.4 km)  
> **Route Status**: Safe (0 Hazard Intersections)  
> **Accessibility**: Fully Accessible (Wheelchair Ramp Verified)  
> *Data Freshness: Synchronized 15 seconds ago.*

### 2.2. No Safe Route Available Alert
> **CRITICAL ALERT: NO SAFE ROUTE CURRENTLY AVAILABLE**  
> All candidate routes to nearby shelters intersect verified flood zones or hard road closures.  
> **Action Required**: Remain in place on high ground if safe, or request direct authority rescue assistance.  
> *Refreshed: 5 seconds ago.*

### 2.3. Stale Data Warning Banner
> **WARNING: DATA FRESHNESS DEGRADED**  
> Weather and hazard feeds have not synchronized for 25 minutes due to network instability.  
> Proceed with extreme caution and follow local physical authority instructions.

---

## 3. Standardized SMS Payload Templates

### 3.1. Incoming Simulated SMS Input Example
```text
EMERGENCY LOC 19.0760,72.8777 WHEELCHAIR
```

### 3.2. Outgoing Compact SMS Response Template
```text
resQroute Emergency Assistance:
Target: Shelter B (3.4km)
Status: SAFE & ACCESSIBLE (Ramp Available)
Coords: 19.0812, 72.8910
Map: https://maps.os.org/s/b
Reported: 2m ago
```

### 3.3. SMS Location Unclear Response Template
```text
resQroute Error: Could not confidently extract coordinates from SMS payload. 
Please resend using format: 'EMERGENCY LOC [Lat],[Lon]' or 'EMERGENCY [Plus Code]'.
```
