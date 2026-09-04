# resQroute Design System & Visual Specification (DESIGN.md)

**Version:** 3.0.0 (SHIELD-Inspired Apple-Grade Edition)  
**System Name:** resQroute Human-Centric Safety & Reassurance Design System  
**Product Core Thesis:** *"The shortest route is not always the safest route."*

---

## 1. Executive Summary & Design Philosophy

`resQroute` is a mission-critical, intelligent disaster evacuation and shelter-intelligence platform built for SIH Problem Statement SIH26191 (*Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations*). 

The platform evaluates evacuation corridors based on multi-vector real-time safety telemetry (water inundation depth, bridge structural flags, shelter capacity event streams, data freshness) rather than raw road distance.

### 1.1 The Version 3.0 Visual Evolution
Version 3.0 represents a complete visual and interaction evolution inspired by open-source disaster design benchmarks (**SHIELD** visual language) combined with **Apple Human Interface Guidelines (HIG)** and **Material Design 3**. 

Historically, emergency interfaces have relied on aggressive dark themes, flashing red neon banners, or cluttered military dashboards that induce cognitive overload and panic. `resQroute` Version 3.0 establishes a **calm, bright, porcelain-light environment** engineered to:

1. **Actively Reduce Panic:** Replace startling visual alarms with serene whitespace, soft elevation, friendly typography, and reassuring visual feedback.
2. **Guarantee Outdoor Daylight Readability:** Provide pristine legibility under direct, harsh sunlight using a warm snow-white canvas (`#FAFBFD`), high-contrast slate typography (`#0F172A`), and vivid semantic state accents.
3. **Enforce 3-Second Actionability:** Every view instantly answers: *"Where am I safe, and what do I do right now?"* using dominant, thumb-friendly touch targets.
4. **Humanize Disaster Technology:** Treat evacuees not as passive data points, but as stressed human beings needing clear, trustworthy, and empathetic direction.

---

## 2. Design Tokens & System Foundations

### 2.1 Color Architecture & Semantic Mapping
The Version 3.0 color system enforces strict separation between **Identity & Wayfinding (Royal Blue)**, **Safe States (Emerald Green)**, **Cautionary States (Amber)**, and **Critical Life-Safety Threats (Crimson Red)**. Color is *never* used as the sole indicator; it is always paired with an unambiguous icon, plain-language text, and quantitative metadata.

```
+-------------------------------------------------------------------------------------------------------+
|                                    RESQROUTE v3.0 COLOR PALETTE                                      |
+----------------------+---------+--------------------+-------------------------------------------------+
| Role                 | HEX     | Surface / Tint     | Primary Use Case                                |
+----------------------+---------+--------------------+-------------------------------------------------+
| Canvas Base          | #FAFBFD | —                  | Primary application background                  |
| Surface Card         | #FFFFFF | —                  | Elevated interactive cards & bottom sheets      |
| Surface Muted        | #F1F5F9 | —                  | Grouped backdrops, segmented controls, tags     |
| Border Hairline      | #E2E8F0 | —                  | Card dividers & input outlines                  |
| Border Focus         | #93C5FD | —                  | Active focus states & selection outlines        |
| Text Primary         | #0F172A | —                  | Headings, primary labels, tabular metrics       |
| Text Secondary       | #475569 | —                  | Body copy, instructions, secondary metadata     |
| Text Muted           | #94A3B8 | —                  | Timestamps, inactive tabs, placeholder copy     |
| Brand Primary (Blue) | #2563EB | #EFF6FF (10% tint) | Primary brand marks, active routes, main CTAs  |
| Brand Hover / Dark   | #1D4ED8 | #DBEAFE            | Button pressed states, active navigation pins   |
| Safe Green           | #059669 | #ECFDF5 (12% tint) | Verified safe routes, open beds, clear roads    |
| Warning Amber        | #D97706 | #FFFBEB (12% tint) | Approaching capacity, single-lane debris delays |
| Critical Red         | #DC2626 | #FEF2F2 (12% tint) | Hard closures, flood polygons, SOS emergency    |
| Intelligence Purple  | #7C3AED | #F5F3FF (12% tint) | Shadow ML classifications, policy versions      |
+----------------------+---------+--------------------+-------------------------------------------------+
```

### 2.2 Complete CSS Design Tokens (`:root`)

```css
:root {
  /* Surface & Base Canvas */
  --bg-canvas: #fafbfd;
  --bg-surface-card: #ffffff;
  --bg-surface-muted: #f1f5f9;
  --bg-surface-glass: rgba(255, 255, 255, 0.85);

  /* Typography Colors */
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-on-brand: #ffffff;

  /* Brand Palette (Royal Blue) */
  --brand-primary: #2563eb;
  --brand-hover: #1d4ed8;
  --brand-surface: #eff6ff;
  --brand-border: #dbeafe;

  /* Semantic Emergency Accents */
  --color-safe: #059669;
  --color-safe-surface: #ecfdf5;
  --color-safe-border: #a7f3d0;

  --color-warning: #d97706;
  --color-warning-surface: #fffbeb;
  --color-warning-border: #fde68a;

  --color-danger: #dc2626;
  --color-danger-surface: #fef2f2;
  --color-danger-border: #fecaca;

  --color-purple: #7c3aed;
  --color-purple-surface: #f5f3ff;
  --color-purple-border: #ddd6fe;

  /* Neutral Borders */
  --border-subtle: #e2e8f0;
  --border-medium: #cbd5e1;

  /* Corner Radius Hierarchy (SHIELD Large-Rounded System) */
  --radius-xs: 8px;
  --radius-sm: 12px;
  --radius-md: 16px;
  --radius-lg: 20px;
  --radius-xl: 24px;
  --radius-2xl: 32px;
  --radius-full: 9999px;

  /* Soft Ambient Elevation (Apple / SHIELD Soft Shadows) */
  --shadow-sm: 0 1px 3px 0 rgba(15, 23, 42, 0.03);
  --shadow-card: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.02);
  --shadow-floating: 0 16px 36px -6px rgba(15, 23, 42, 0.08), 0 8px 16px -4px rgba(15, 23, 42, 0.03);
  --shadow-cta: 0 10px 24px -4px rgba(37, 99, 235, 0.35);
  --shadow-emergency: 0 10px 24px -4px rgba(220, 38, 38, 0.35);

  /* Layout Spacing */
  --space-3xs: 2px;
  --space-2xs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 20px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --space-3xl: 48px;

  /* Motion & Easing */
  --motion-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
  --motion-standard: 250ms cubic-bezier(0.16, 1, 0.3, 1);
  --motion-spring: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 3. Typography Scale & Hierarchies

`resQroute` Version 3.0 uses a modern system sans-serif font stack (`Inter`, `SF Pro Display`, `-apple-system`) tuned for extreme optical legibility.

```
+---------------+-----------+-------------+-----------------+----------------------------------------+
| Level         | Size      | Weight      | Line Height     | Context                                |
+---------------+-----------+-------------+-----------------+----------------------------------------+
| Display XL    | 34px      | 800 (Bold)  | 40px (1.17)     | Hero Emergency Headings, Big Metrics  |
| Display Large | 28px      | 700 (Bold)  | 34px (1.21)     | Onboarding titles, Major Status Banner |
| Heading 1     | 22px      | 700 (Bold)  | 28px (1.27)     | Screen Titles (e.g., "Safe Havens")    |
| Heading 2     | 18px      | 600 (Semibd)| 24px (1.33)     | Card Titles, Shelter Names, Hazards    |
| Subhead       | 16px      | 600 (Semibd)| 22px (1.37)     | Section Headings, CTA Labels           |
| Body Primary  | 15px      | 400/500     | 22px (1.46)     | Instruction copy, Explainability text  |
| Body Small    | 13px      | 400/500     | 18px (1.38)     | Metadata, Coordinates, Explanations    |
| Caption / Tag | 11px      | 600 (Semibd)| 14px (1.27)     | Status Pills, Verified Badges          |
| Microcopy     | 10px      | 500 (Medium)| 12px (1.20)     | Footers, Timestamp Labels              |
+---------------+-----------+-------------+-----------------+----------------------------------------+
```

### 3.1 Tabular Numbers & Dynamic Type
- **Tabular Numbers:** All ETAs, bed counts, occupancy percentages, and coordinates enforce `font-variant-numeric: tabular-nums` to eliminate layout jitter during live updates.
- **Dynamic Type Support:** Text scales up to 200% without layout clipping, accommodating low-vision users.

---

## 4. Complete Production Component Library

### 4.1 Dominant Action Buttons (Thumb-First 56px CTAs)

#### Primary Action Button (Filled Royal Blue)
- Height: `56px` (Surpasses 48px Apple/Android accessibility guidelines)
- Border Radius: `var(--radius-lg)` (`20px`)
- Background: `var(--brand-primary)` (`#2563EB`)
- Text: `var(--text-on-brand)` (`#FFFFFF`), `16px`, Weight `700`
- Shadow: `var(--shadow-cta)`
- Touch Target: Full width with `16px` horizontal padding.

#### Emergency Danger CTA (e.g., Immediate SOS / Hard Closure)
- Background: `var(--color-danger)` (`#DC2626`)
- Text: `#FFFFFF`, `16px`, Weight `700`
- Shadow: `var(--shadow-emergency)`

#### Secondary Outlined Button
- Height: `48px`
- Border Radius: `var(--radius-md)` (`16px`)
- Background: `#FFFFFF`
- Border: `1.5px solid var(--border-subtle)`
- Text: `var(--text-primary)` (`#0F172A`), Weight `600`

---

### 4.2 Cards & Surface Containers

```
+-------------------------------------------------------------------------+
|                        SHIELD-INSPIRED CARD ANATOMY                     |
+-------------------------------------------------------------------------+
| [Top Header: Icon + Category Badge + Distance Tag]                      |
| [Main Title: Heading 2, #0F172A]                                        |
| [Body Content: High-contrast explanation / Capacity Progress Bar]        |
| [Feature Pills: Soft tags #F1F5F9 with icons (Wheelchair, Power, Med)]  |
| [Bottom Footer: Timestamp "Reported 45s ago" + Action Button]          |
+-------------------------------------------------------------------------+
```

#### Shelter Safe Haven Card
- Container: `#FFFFFF`, Radius `24px` (`--radius-xl`), Shadow `var(--shadow-card)`, Border `1px solid #E2E8F0`
- Header: Shelter Name (`Heading 2`) + Distance Pill (`13px`, `#475569`)
- Occupancy Bar: Dual-tone progress track:
  - Fill: `var(--color-safe)` (`#059669`) if `< 80%`
  - Fill: `var(--color-warning)` (`#D97706`) if `80% - 95%`
  - Fill: `var(--color-danger)` (`#DC2626`) if full (`100%`)
- Feature Chips: Soft pill badges `#F1F5F9` with SVG icons: `Wheelchair` (ADA Accessible), `Zap` (Medical Generator), `HeartPulse` (Triage), `Utensils` (Meals).
- Freshness Stamp: *"Reported at 21:44:00 (15s ago)"* with live green pulsing indicator.

---

### 4.3 Algorithmic Route Explainability Card (The Core Trust Component)

`resQroute`'s most critical UI component explaining **why** a route was chosen:

```html
<div class="bg-white rounded-3xl p-5 border border-slate-200 shadow-card space-y-4">
  <!-- Header -->
  <div class="flex items-center justify-between">
    <span class="text-xs font-semibold px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
      Route Evaluation Lineage
    </span>
    <span class="text-xs text-slate-500 font-mono">Graph v2.4 • Policy v1.0</span>
  </div>

  <!-- Rejection Block (Route A) -->
  <div class="p-3.5 rounded-2xl bg-rose-50/60 border border-rose-200 space-y-2">
    <div class="flex items-center justify-between">
      <span class="text-sm font-bold text-rose-800">Route A (Direct Canal Path)</span>
      <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-rose-200 text-rose-900">REJECTED</span>
    </div>
    <p class="text-xs text-rose-700 leading-relaxed">
      • Intersects active hard closure at Edge #402 (Water depth 45cm exceeds 15cm threshold).
    </p>
  </div>

  <!-- Selection Block (Route B) -->
  <div class="p-3.5 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-2">
    <div class="flex items-center justify-between">
      <span class="text-sm font-bold text-emerald-800">Route B (Ridge Road Corridor)</span>
      <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-200 text-emerald-900">VERIFIED SAFE</span>
    </div>
    <p class="text-xs text-emerald-700 leading-relaxed">
      • Zero hazard intersections • +35m elevation above flood basin • Full wheelchair accessibility.
    </p>
  </div>
</div>
```

---

### 4.4 Status Badges & Telemetry Chips

```html
<!-- Safe Chip -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold">
  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
  Verified Safe Corridor
</span>

<!-- Warning Chip -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-semibold">
  <span class="w-2 h-2 rounded-full bg-amber-500"></span>
  Single Lane Debris (Caution)
</span>

<!-- Danger Chip -->
<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold">
  <span class="w-2 h-2 rounded-full bg-rose-500"></span>
  Road Impassable
</span>
```

---

## 5. Apple-Grade Map UX Specification

The evacuation map looks like a clean, high-end consumer map (Apple Maps light mode) optimized for high cognitive stress:

- **Base Canvas:** Warm porcelain / light silver (`#FAFBFD` terrain, `#FFFFFF` road vectors, `#CBD5E1` arterial boundaries).
- **Water Bodies & Inundation Contours:** Soft baby blue (`#DBEAFE`) with dashed warning flood borders (`#EF4444`).
- **Safe Evacuation Corridor:** High-visibility Solid Royal Blue line (`#2563EB`), weight `6px`, with glowing directional dots leading to an Emerald shelter pin (`#059669`).
- **Blocked / Impassable Roads:** Solid Crimson line (`#DC2626`), weight `5px`, overlaid with diagonal barrier hashes.
- **Shelter Pins:** White rounded pill pins showing bed count chips (e.g., `[Shelter B • 45 open beds]`).
- **User Location Indicator:** Pulsing royal blue dot with directional field cone (`#2563EB`).
- **Floating Controls:** Minimal pill buttons (Recenter, Layer Toggle, Satellite, Zoom) floating on the right edge.

---

## 6. Screen-by-Screen Visual Architecture

### 6.1 Onboarding & Permissions Flow
- **3-Slide Reassuring Carousel:** Friendly vector illustrations explaining Everyday Preparedness, Hazard-Aware Routing, and Accessibility Matching.
- **Location Permission Card:** Soft modal emphasizing: *"resQroute processes location ephemerally during evacuations. Your raw GPS is never sold or tracked."*

### 6.2 Everyday Mode Screen
- **Clean White Header:** Local weather & river telemetry chip (*"District 17 • Normal Status"*).
- **Primary Search Bar:** Large rounded search input (`52px` height) with voice input icon.
- **Grid Categories:** Nearby Shelters, Hospitals, Fire Stations, Preparedness Checklist, Community Volunteers.

### 6.3 Disaster Mode Screen (High Alert)
- **Top Red Zone Alert Banner:** Soft coral surface (`#FEF2F2`) with red accent bar, pulsing warning icon, and clear summary: *"FLASH FLOOD EMERGENCY: SECTOR 17"*.
- **Floating Evacuation Card:** Bottom sheet displaying recommended shelter, ETA, distance, and dominant primary CTA: **`[GET SAFEST EVACUATION ROUTE]`**.

### 6.4 Authority Incident Command Dashboard
- **Split-Screen Desktop Layout:** Live incident map on left; real-time report queue on right.
- **Moderation Actions:** Prominent **`[CONFIRM HARD CLOSURE]`** and **`[REJECT REPORT]`** buttons.
- **Audit Lineage Dialog:** Prompts operator to attach policy category (`FLOOD_SUBMERGED`, `LANDSLIDE_DEBRIS`) to maintain append-only audit event integrity.

### 6.5 Simulated SMS Fallback Screen
- Dedicated web modal demonstrating text payload parsing when internet drops:
  - Input field simulating incoming SMS: `EMERGENCY LOC 19.0760,72.8777 WHEELCHAIR`
  - Output display: `Recommended: Shelter B (3.4km). Status: SAFE. Lat:19.0812, Lon:72.8910. Map: https://maps.os.org/s/b`

---

## 7. Motion & Panic-Reduction Transitions

1. **Panic-Reduction Transitions:**
   - Alerts do **not** flash violently. Banners use a smooth slide-and-fade entry (`300ms`, `cubic-bezier(0.16, 1, 0.3, 1)`).
   - Live telemetry status badges use a gentle `2s` opacity pulse (`1.0` to `0.4` to `1.0`), never rapid blinking.
2. **Card Tap Feedback:**
   - Active tap: Subtle scale `scale(0.985)` with `100ms` duration for tactile confirmation.
3. **Route Recalculation:**
   - When a safer corridor is found, the old path dissolves to faded red while the newly cleared ridge path draws forward in vibrant blue (`600ms` stroke animation).
4. **Accessibility Override:**
   - All animations automatically deactivate when `prefers-reduced-motion: reduce` is enabled.

---

## 8. Human Factors & Accessibility Defense

- **WCAG Compliance:** All text elements achieve **WCAG 2.1 AA** (4.5:1 ratio); core emergency instructions achieve **WCAG AAA** (7:1+).
- **Triple Redundancy for Color Blindness:**
  - Red danger elements are *always* paired with an octagon icon and text **"BLOCKED"**.
  - Green safe elements are *always* paired with a shield check icon and text **"VERIFIED SAFE"**.
  - Amber warning elements are *always* paired with a triangle icon and text **"CAUTION"**.
- **One-Handed Thumb Reachability:** All critical action controls are anchored in the bottom 40% of the screen.

---

_resQroute Design System Specification v3.0 Authored for Civil Defense, Municipal Responders, and Public Citizens._
