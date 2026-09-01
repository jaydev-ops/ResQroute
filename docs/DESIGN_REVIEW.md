# resQroute Design Review & Emergency Usability Audit

## Emergency Usability Principles
Designing interfaces for high-stress disaster situations requires radical departure from standard web application design. During natural disasters:
- Users experience cognitive overload, panic, and reduced attention spans.
- Mobile screens are subjected to harsh outdoor sunlight, heavy rain drops, or cracked glass.
- Network connections are slow, causing intermittent loading.

`resQroute` adheres to **Disaster Usability Engineering**: Every UI element must communicate safety status instantly without requiring deep menu navigation.

---

## 1. Heuristic Evaluation for Crisis Usability

| Usability Heuristic | Common Web App Mistake | resQroute Crisis Standard | Status |
| :--- | :--- | :--- | :--- |
| **Cognitive Load** | Displaying dense text paragraphs & complex settings menus | Single primary action button (**"Find Safe Route"**); prominent status badges | `PASS` |
| **Visual Contrast** | Subtle gray-on-gray text and low-contrast buttons | High-contrast WCAG AAA compliance (Contrast ratio > 7:1); dark slate background | `PASS` |
| **Data Freshness** | Hidden timestamps or assumed live data | Explicit freshness banners (**"Reported 2 mins ago"**); warning for stale graph data | `PASS` |
| **Accessibility Focus** | Hidden accessibility toggles in settings | Immediate accessibility profile selection on onboarding screen | `PASS` |
| **Confidence Transparency**| Unexplained AI or system recommendations | Clear textual rationale (**"Route A rejected: Submerged road at Sector 4"**) | `PASS` |
| **Color System Reliability**| Relying on color alone to signal danger | Dual-coding: Icon + Text Label + Color (e.g. `[!] RED ZONE - CLOSED`) | `PASS` |

---

## 2. Emergency UX UI Inspection

### 2.1. Disaster Mode Interface Layout
- **Top Banner**: Global Status Indicator (`[EMERGENCY ACTIVE: FLOODING IN SECTOR 17]`) with data freshness timestamp (`Last sync: 10s ago`).
- **Center Canvas**: High-contrast vector map displaying verified hazard polygons (Red), closed edge overlays (Orange stripes), accessible shelters (Green markers with capacity chips), and recommended safe route (Solid Cyan line).
- **Bottom Drawer**: Prominent card displaying selected shelter name, distance, ETA, accessibility status (`Wheelchair Ramp Available`), and primary navigation action.

### 2.2. Authority Dashboard Moderation UI
- **Split-Screen Layout**: Live map on left; incoming report queue on right.
- **Single-Click Actions**: Prominent `[CONFIRM HARD CLOSURE]` and `[REJECT REPORT]` buttons to minimize moderation delays.
- **Audit Lineage Modal**: Every closure prompt requires selecting a policy category (`FLOOD_SUBMERGED`, `LANDSLIDE_DEBRIS`) to maintain audit event integrity.
