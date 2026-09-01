import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure diagrams directory exists
os.makedirs("diagrams", exist_ok=True)

# Set global styles
plt.style.use('dark_background')
BG_COLOR = '#0F172A'      # Dark Slate
CARD_BG = '#1E293B'       # Slate Card
BORDER_COLOR = '#334155'  # Border Slate
TEXT_COLOR = '#F8FAFC'    # Crisp White
TEXT_MUTED = '#94A3B8'    # Slate Gray
ACCENT_BLUE = '#38BDF8'   # Sky Blue
ACCENT_GREEN = '#34D399'  # Emerald Green
ACCENT_RED = '#F87171'    # Coral Red
ACCENT_ORANGE = '#FBBF24' # Amber
ACCENT_PURPLE = '#C084FC' # Purple

def draw_box(ax, x, y, w, h, title, subtitle="", bg=CARD_BG, border=ACCENT_BLUE, title_color=TEXT_COLOR):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", 
                                  linewidth=1.5, edgecolor=border, facecolor=bg)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.65 if subtitle else y + h/2, title, 
            color=title_color, weight='bold', fontsize=10, ha='center', va='center')
    if subtitle:
        ax.text(x + w/2, y + h*0.3, subtitle, color=TEXT_MUTED, fontsize=8, ha='center', va='center')

def draw_arrow(ax, x1, y1, x2, y2, label="", color=TEXT_MUTED):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5, mutation_scale=15))
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.02, label, color=TEXT_MUTED, fontsize=7, ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.2", facecolor=BG_COLOR, edgecolor='none', alpha=0.8))

# ---------------------------------------------------------
# DIAGRAM 01: System Overview & Architecture
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 01: System Overview & High-Level Architecture", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.75, 0.25, 0.15, "Citizens & Vulnerable", "Web / PWA Client", border=ACCENT_GREEN)
draw_box(ax, 0.375, 0.75, 0.25, 0.15, "Authorities & Responders", "Command Dashboard", border=ACCENT_BLUE)
draw_box(ax, 0.70, 0.75, 0.25, 0.15, "SMS / Offline Fallback", "Simulated SMS Gateway", border=ACCENT_ORANGE)

draw_box(ax, 0.20, 0.45, 0.60, 0.18, "API & WebSocket Gateway Layer (FastAPI)", "Auth / RBAC | Event Ingestion | Rate Limiter", border=ACCENT_PURPLE)

draw_box(ax, 0.05, 0.12, 0.26, 0.20, "PostGIS & DB Engine", "PostgreSQL + Audit Logs\nroad_edge_overlays", border=ACCENT_BLUE)
draw_box(ax, 0.375, 0.12, 0.25, 0.20, "PostGIS Overlay Routing", "OSRM Candidates +\nHard Closure Filter", border=ACCENT_RED)
draw_box(ax, 0.70, 0.12, 0.25, 0.20, "Shelter Engine", "Append-Only Updates\nCapacity & Accessibility", border=ACCENT_GREEN)

draw_arrow(ax, 0.175, 0.75, 0.30, 0.63, "Reports / Requests")
draw_arrow(ax, 0.50, 0.75, 0.50, 0.63, "Admin Actions")
draw_arrow(ax, 0.825, 0.75, 0.70, 0.63, "Fallback SMS")

draw_arrow(ax, 0.35, 0.45, 0.18, 0.32, "Persist / Spatial Query")
draw_arrow(ax, 0.50, 0.45, 0.50, 0.32, "Overlay Intersect")
draw_arrow(ax, 0.65, 0.45, 0.825, 0.32, "Check Capacity")

plt.savefig("diagrams/diagram_01_system_overview.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 02: Complete Data Flow & Real-Time Ingestion
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 02: Real-Time Data Ingestion & Event Pipeline", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.70, 0.22, 0.18, "Raw Ingestion", "Citizen Reports / SMS\nAuthority Feeds", border=ACCENT_BLUE)
draw_box(ax, 0.38, 0.70, 0.24, 0.18, "Validation & De-duplication", "Spatial Proximity Join\nConfidence Engine", border=ACCENT_ORANGE)
draw_box(ax, 0.73, 0.70, 0.22, 0.18, "Event Persistence", "Append-only hazard_evidence\naudit_events", border=ACCENT_PURPLE)

draw_box(ax, 0.05, 0.25, 0.26, 0.22, "PostGIS Edge Overlays", "Active road_edge_overlays\nHard closure flags", border=ACCENT_RED)
draw_box(ax, 0.37, 0.25, 0.26, 0.22, "WebSocket Event Bus", "Redis Pub/Sub\nLive broadcast to clients", border=ACCENT_GREEN)
draw_box(ax, 0.69, 0.25, 0.26, 0.22, "Client UI Sync", "Map layer refresh\nDynamic route invalidation", border=ACCENT_BLUE)

draw_arrow(ax, 0.27, 0.79, 0.38, 0.79, "Raw Payload")
draw_arrow(ax, 0.62, 0.79, 0.73, 0.79, "Validated Event")
draw_arrow(ax, 0.84, 0.70, 0.84, 0.47, "Update State")
draw_arrow(ax, 0.73, 0.36, 0.63, 0.36, "Broadcast Event")
draw_arrow(ax, 0.37, 0.36, 0.31, 0.36, "Overlay Invalidation")
draw_arrow(ax, 0.18, 0.47, 0.18, 0.70, "Refreshed Overlays")

plt.savefig("diagrams/diagram_02_data_flow_ingestion.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 03: Hazard Report Lifecycle & Confidence Pipeline
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 03: Hazard Report Verification & Confidence Pipeline", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.03, 0.40, 0.16, 0.25, "REPORTED\n(Score: 0-30)", "Raw Citizen Report\nUnverified", border=TEXT_MUTED)
draw_box(ax, 0.27, 0.40, 0.18, 0.25, "PROBABLE\n(Score: 31-60)", "Multiple Reports / Sensor\nSpatial Cluster", border=ACCENT_ORANGE)
draw_box(ax, 0.54, 0.40, 0.18, 0.25, "CONFIRMED\n(Score: 61-100)", "Authority Verified\nHard Road Closure", border=ACCENT_RED)
draw_box(ax, 0.80, 0.40, 0.17, 0.25, "RESOLVED / EXPIRED", "Debris Cleared / TTL\nDeactivated", border=ACCENT_GREEN)

draw_arrow(ax, 0.19, 0.525, 0.27, 0.525, "+25 Multi-report")
draw_arrow(ax, 0.45, 0.525, 0.54, 0.525, "+35 Authority")
draw_arrow(ax, 0.72, 0.525, 0.80, 0.525, "Hazard Cleared")

plt.savefig("diagrams/diagram_03_hazard_lifecycle_confidence.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 04: Routing Decision Engine & Overlay Logic
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 04: Routing Decision Engine & PostGIS Dynamic Overlay Logic", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.65, 0.25, 0.20, "1. Candidate Generation", "OSRM Engine returns\nK-Shortest Paths", border=ACCENT_BLUE)
draw_box(ax, 0.375, 0.65, 0.25, 0.20, "2. Spatial Overlay Check", "PostGIS ST_Intersects\nvs road_edge_overlays", border=ACCENT_ORANGE)
draw_box(ax, 0.70, 0.65, 0.25, 0.20, "3. Safety & Attribute Filter", "Slope/Step Constraints &\nAccessibility Matching", border=ACCENT_PURPLE)

draw_box(ax, 0.20, 0.15, 0.25, 0.25, "REJECT UNSAFE PATHS", "Confirmed Closed Edges / \nHigh Hazard Risk", border=ACCENT_RED)
draw_box(ax, 0.55, 0.15, 0.25, 0.25, "RECOMMEND SAFEST ROUTE", "Lowest Risk Score +\nFull Accessibility", border=ACCENT_GREEN)

draw_arrow(ax, 0.30, 0.75, 0.375, 0.75, "Candidate Geometries")
draw_arrow(ax, 0.625, 0.75, 0.70, 0.75, "Filtered Candidates")

draw_arrow(ax, 0.825, 0.65, 0.675, 0.40, "Survives Safety Rules")
draw_arrow(ax, 0.50, 0.65, 0.325, 0.40, "Contains Hard Hazard")

ax.text(0.5, 0.05, "CRITICAL GUARDRAIL: If zero routes survive overlay checks, return 'NO SAFE ROUTE AVAILABLE' + Hazard Explanation.",
        color=ACCENT_RED, weight='bold', fontsize=8, ha='center')

plt.savefig("diagrams/diagram_04_routing_decision_overlay.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 05: Shelter Ranking Algorithm & Accessibility
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 05: Shelter Ranking & Vulnerability Matching Engine", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.70, 0.25, 0.18, "Candidate Shelters", "PostGIS Radial Query\n(ST_DWithin)", border=ACCENT_BLUE)
draw_box(ax, 0.375, 0.70, 0.25, 0.18, "Capacity Filter", "Materialized View Check\n(Occupancy < 100%)", border=ACCENT_ORANGE)
draw_box(ax, 0.70, 0.70, 0.25, 0.18, "Accessibility Match", "Wheelchair/Ramp/Medical\nMandatory Filter", border=ACCENT_PURPLE)

draw_box(ax, 0.20, 0.20, 0.60, 0.30, "Multi-Factor Scoring Matrix", 
         "Score = 0.4*(100 - RouteRisk) + 0.3*(AvailableCapacity%) + 0.2*(AccessibilityMatch) + 0.1*(FreshnessScore)\n"
         "Displays explicit timestamp: 'Reported at [timestamp]'", border=ACCENT_GREEN)

draw_arrow(ax, 0.30, 0.79, 0.375, 0.79, "Nearby Shelters")
draw_arrow(ax, 0.625, 0.79, 0.70, 0.79, "Available Shelters")
draw_arrow(ax, 0.825, 0.70, 0.60, 0.50, "Accessible Shelters")

plt.savefig("diagrams/diagram_05_shelter_ranking_accessibility.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 06: Vulnerability & Accessibility Model
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 06: Minimal Vulnerability & Accessibility Matching Model", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.55, 0.26, 0.30, "User Profile\n(Minimal Flags)", "wheelchair_required = true\nelectricity_for_oxygen = true\nelderly_mobility = true", border=ACCENT_GREEN)
draw_box(ax, 0.37, 0.55, 0.26, 0.30, "Route Constraints", "Max slope <= 5%\nNo step barriers\nMin path width >= 1.5m", border=ACCENT_BLUE)
draw_box(ax, 0.69, 0.55, 0.26, 0.30, "Shelter Capabilities", "Ramp access = true\nMedical generator = true\nAccessible toilets = true", border=ACCENT_PURPLE)

draw_box(ax, 0.20, 0.10, 0.60, 0.25, "Deterministic Matching Engine", "Hard filter rejects non-compliant routes/shelters prior to ranking score calculation", border=ACCENT_ORANGE)

draw_arrow(ax, 0.18, 0.55, 0.35, 0.35)
draw_arrow(ax, 0.50, 0.55, 0.50, 0.35)
draw_arrow(ax, 0.82, 0.55, 0.65, 0.35)

plt.savefig("diagrams/diagram_06_vulnerability_model.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 07: Offline Fallback & Simulated SMS Architecture
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 07: Offline Degradation & Simulated SMS Fallback Architecture", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.65, 0.25, 0.22, "Web PWA Client", "Cached Offline Map Tiles\nLast Known Shelters (IndexedDB)", border=ACCENT_BLUE)
draw_box(ax, 0.375, 0.65, 0.25, 0.22, "Simulated SMS Parser", "Extract Lat/Lon / Plus Code\nfrom Emergency Payload", border=ACCENT_ORANGE)
draw_box(ax, 0.70, 0.65, 0.25, 0.22, "Compact SMS Dispatch", "Return Shelter Name, Lat/Lon,\nMap URL & Freshness Timestamp", border=ACCENT_GREEN)

draw_box(ax, 0.15, 0.15, 0.70, 0.25, "Graceful Degradation Model", 
         "Level 1: Full Online WebSockets -> Level 2: Polling REST -> Level 3: Simulated SMS Payload -> Level 4: Stale Local Cache + Alert",
         border=ACCENT_PURPLE)

draw_arrow(ax, 0.30, 0.76, 0.375, 0.76, "Loss of Internet")
draw_arrow(ax, 0.625, 0.76, 0.70, 0.76, "Structured Location")

plt.savefig("diagrams/diagram_07_offline_sms_architecture.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 08: ML Guardrails & Shadow Mode Pipeline
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 08: AI / ML Shadow Pipeline & Deterministic Guardrails", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.65, 0.25, 0.20, "Unstructured Input", "Citizen Text / Image\nReport Payload", border=ACCENT_BLUE)
draw_box(ax, 0.375, 0.65, 0.25, 0.20, "Shadow ML Classifier", "NLP / Image Model\nClassify Hazard Type & Urgency", border=ACCENT_PURPLE)
draw_box(ax, 0.70, 0.65, 0.25, 0.20, "Confidence & Policy Check", "Check Model Confidence\n(Must be >= 0.85)", border=ACCENT_ORANGE)

draw_box(ax, 0.20, 0.15, 0.60, 0.25, "Deterministic Safety & PostGIS Overlay Engine", 
         "ML proposals NEVER alter graph edge states directly without policy verification or authority confirmation",
         border=ACCENT_GREEN)

draw_arrow(ax, 0.30, 0.75, 0.375, 0.75)
draw_arrow(ax, 0.625, 0.75, 0.70, 0.75)
draw_arrow(ax, 0.825, 0.65, 0.60, 0.40, "Proposal")

plt.savefig("diagrams/diagram_08_ml_guardrails_pipeline.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 09: Authority Dashboard & Audit Workflow
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 09: Authority Incident Command & Audit Event Workflow", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.65, 0.25, 0.20, "Incident Command UI", "Live Map | Hazard Moderation\nShelter Capacity Updates", border=ACCENT_BLUE)
draw_box(ax, 0.375, 0.65, 0.25, 0.20, "Authority Action", "Mark Hard Closure /\nVerify Hazard / Override", border=ACCENT_RED)
draw_box(ax, 0.70, 0.65, 0.25, 0.20, "Audit Logger", "Append-Only audit_events\nActor ID, Timestamp, Policy", border=ACCENT_GREEN)

draw_box(ax, 0.20, 0.15, 0.60, 0.25, "System-Wide State Propagation", 
         "Invalidates cached routes, triggers PostGIS overlay recalculation, broadcasts WebSockets to active citizens",
         border=ACCENT_PURPLE)

draw_arrow(ax, 0.30, 0.75, 0.375, 0.75)
draw_arrow(ax, 0.625, 0.75, 0.70, 0.75)
draw_arrow(ax, 0.825, 0.65, 0.60, 0.40)

plt.savefig("diagrams/diagram_09_authority_audit_workflow.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 10: Security Architecture & RBAC
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 10: Security Architecture, RBAC & Privacy Boundaries", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.05, 0.50, 0.26, 0.35, "Roles & RBAC", "Citizen (Read / Report)\nAuthority (Moderation / Closure)\nResponder (Read / Task Update)\nAdmin (System Audit)", border=ACCENT_BLUE)
draw_box(ax, 0.37, 0.50, 0.26, 0.35, "Auth & Transport", "JWT Bearer Tokens\nHTTPS / TLS 1.3\nWSS Encrypted Sockets\nRate Limiting (100 req/min)", border=ACCENT_PURPLE)
draw_box(ax, 0.69, 0.50, 0.26, 0.35, "Privacy & Lineage", "Minimal profile flags\nNo exact location retention\nFull audit log traceability\nPolicy & Graph Versioning", border=ACCENT_GREEN)

plt.savefig("diagrams/diagram_10_security_rbac_architecture.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 11: PostgreSQL + PostGIS ER Diagram
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 11: PostgreSQL + PostGIS Entity-Relationship Diagram", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.03, 0.60, 0.28, 0.30, "users & profiles", "id (PK)\nrole (ENUM)\nwheelchair_required (BOOL)\nelectricity_required (BOOL)", border=ACCENT_BLUE)
draw_box(ax, 0.36, 0.60, 0.28, 0.30, "road_edge_overlays", "id (PK)\nedge_id (BIGINT)\ngeom (GEOMETRY)\nis_closed (BOOL)\nfreshness_ts (TIMESTAMPTZ)", border=ACCENT_RED)
draw_box(ax, 0.69, 0.60, 0.28, 0.30, "shelter_updates (Append-only)", "id (PK)\nshelter_id (FK)\noccupied_count (INT)\nactor_id (FK)\ntimestamp (TIMESTAMPTZ)", border=ACCENT_GREEN)

draw_box(ax, 0.03, 0.12, 0.28, 0.30, "hazard_evidence", "id (PK)\nhazard_id (FK)\nsource_type (ENUM)\nconfidence_score (FLOAT)\nevidence_data (JSONB)", border=ACCENT_ORANGE)
draw_box(ax, 0.36, 0.12, 0.28, 0.30, "audit_events", "id (PK)\nactor_id (FK)\naction (TEXT)\npolicy_version (TEXT)\ngraph_version (TEXT)\ntimestamp (TIMESTAMPTZ)", border=ACCENT_PURPLE)
draw_box(ax, 0.69, 0.12, 0.28, 0.30, "route_snapshots", "id (PK)\nuser_id (FK)\nroute_geom (GEOMETRY)\nrisk_score (FLOAT)\nfreshness_ts (TIMESTAMPTZ)", border=ACCENT_BLUE)

plt.savefig("diagrams/diagram_11_postgis_er_diagram.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# DIAGRAM 12: MVP -> Enhanced -> Advanced Roadmap
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_facecolor(BG_COLOR)
fig.patch.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

plt.title("DIAGRAM 12: Phased Engineering Roadmap", color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

draw_box(ax, 0.03, 0.35, 0.28, 0.45, "PHASE 1: MVP\n(Web-First Core)", 
         "- React + FastAPI + PostGIS\n- Deterministic Overlay Engine\n- Append-only Shelter Capacity\n- Authority Dashboard & Audit\n- Simulated SMS Demo Screen", border=ACCENT_GREEN)

draw_box(ax, 0.36, 0.35, 0.28, 0.45, "PHASE 2: ENHANCED\n(Expanded Intelligence)", 
         "- Custom Dynamic Graph Engine\n- Shadow Mode ML Classifier\n- Automated Weather Ingestion\n- Native Android Companion\n- Volunteer QR Check-in", border=ACCENT_BLUE)

draw_box(ax, 0.39+0.28, 0.35, 0.28, 0.45, "PHASE 3: ADVANCED\n(Disaster Resilience)", 
         "- Experimental BLE Mesh SOS\n- Predictive Inundation Models\n- Autonomous Drone Feeds\n- Nationwide Edge Clustering\n- Sat-link Fallback Gateway", border=ACCENT_PURPLE)

draw_arrow(ax, 0.31, 0.575, 0.36, 0.575)
draw_arrow(ax, 0.64, 0.575, 0.67, 0.575)

plt.savefig("diagrams/diagram_12_mvp_phased_roadmap.png", bbox_inches='tight')
plt.close()

print("All 12 essential architecture diagrams generated successfully in 'diagrams/'!")
