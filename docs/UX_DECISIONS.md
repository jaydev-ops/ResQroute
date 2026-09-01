# resQroute UX Rationale & Architectural Decisions

This document outlines the design decisions behind the user experience of `resQroute`.

---

## 1. Primary UX Rationale Index

### 1.1. Why Safest Route Over Shortest Distance?
- **User Mental Model**: Standard navigation tools (Google Maps, Waze) optimize aggressively for minimum travel time or shortest distance. In disaster scenarios, this shortest path often directs citizens directly into submerged low-lying roads or active landslide channels.
- **resQroute UX**: The safest route is highlighted as the primary green path. Shortest distance is explicitly subordinated to hazard overlay safety checks.

### 1.2. Why Dual-State (Everyday vs Disaster Mode)?
- **Problem**: Applications designed purely for rare emergency events suffer from zero user familiarity when actual crises strike.
- **UX Solution**: Everyday Mode offers community emergency contacts, hospital locations, and disaster preparation checklists. When an official emergency is declared, the UI transitions to high-alert Disaster Mode with live red-zone overlays.

### 1.3. Why Show Explicit Data Freshness Timestamps?
- **Problem**: Citizens during evacuations distrust static map applications because occupancy numbers or road status may be hours out of date.
- **UX Solution**: All shelter chips and hazard warnings prominently display data freshness (`"Reported 2 mins ago"`). If sync drops, an explicit yellow banner notifies the user of degraded freshness.

### 1.4. Why Deterministic Guardrails over AI Chatbots?
- **Problem**: AI chatbots during disasters can output polite but dangerous hallucinations (e.g. recommending non-existent bridges).
- **UX Solution**: Direct map visualization and deterministic step-by-step route guidance backed by audited PostGIS overlay queries. AI is relegated to shadow NLP processing.
