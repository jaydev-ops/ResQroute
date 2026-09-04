# resQroute Design System & Visual Specification (DESIGN.md)

**Version:** 2.0.0 (Light-First Modern Edition)  
**System Name:** resQroute Human-Centric Safety & Navigation Design System  
**Product Core Philosophy:** _"The shortest route is not always the safest route."_

---

## 1. Executive Summary & Design Philosophy

`resQroute` is a mission-critical, intelligent disaster evacuation platform that calculates escape corridors based on multi-vector real-time safety data (inundation levels, structural bridge integrity, shelter occupancy, live telemetry freshness) rather than raw road distance.

While emergency interfaces historically skew toward alarming, dark, or apocalyptic visual motifs, `resQroute` adheres to **calm authority, clarity under extreme cognitive load, and human reassurance**. Inspired by modern, human-centered UI benchmarks (Apple Human Interface Guidelines, Google Material 3, Flighty, Linear, Notion, Uber), the design system establishes a **clean, bright, high-legibility light environment** engineered to:

- **Minimize Panic:** Replace aggressive visual alarms with crisp, orderly information hierarchies.
- **Ensure Sunlight Visibility:** Deliver pristine contrast outdoors under harsh daytime sun using crisp white canvases (`#FFFFFF`), cool neutral slate text (`#1F2937`), and vibrant, verified semantic tokens.
- **Guarantee 3-Second Actionability:** Every view instantly resolves to _"What do I do next?"_ with one dominant, thumb-friendly touch target.

---

## 2. Color System & Semantic Palette

The color system strictly separates **Identity & Navigation (Blue)** from **Semantic Life-Safety States (Green, Orange, Red)**. Color is _never_ used alone; it is always coupled with an unambiguous icon, a plain-language status label, and quantitative context.

### 2.1 Core Palette Tokens

```
+-----------------------------------------------------------------------------------------+
|                               RESQROUTE COLOR ARCHITECTURE                              |
+----------------------+---------+--------------------+-----------------------------------+
| Role                 | HEX     | Surface / Tint     | Primary Use Case                  |
+----------------------+---------+--------------------+-----------------------------------+
| Primary Blue (Brand) | #1E88E5 | #E3F2FD (10% tint) | Brand mark, primary CTAs, active  |
|                      |         |                    | navigation, live route vectors    |
| Primary Dark (Hover) | #1565C0 | #BBDEFB            | Button pressed/hover states       |
| Primary Light (Tint) | #42A5F5 | #F0F7FF            | Telemetry tags, sync badges       |
| Safe Green           | #43A047 | #E8F5E9 (12% tint) | Verified clear routes, open beds  |
| Warning Orange       | #FFA726 | #FFF3E0 (12% tint) | Approaching capacity, road delays |
| Critical Red         | #E53935 | #FFEBEE (12% tint) | Hard closures, flood polygons, SOS|
| Background (Canvas)  | #FFFFFF | —                  | Primary screen canvas             |
| Surface Dim / Muted  | #F7F9FC | —                  | Grouped backdrops, map chrome     |
| Surface Card         | #FFFFFF | —                  | Elevated interactive cards        |
| Border Subtle        | #E5E7EB | —                  | Hairline card/modal dividers      |
| Border Focus / Active| #93C5FD | —                  | Input focus ring, active card     |
| Text Primary         | #1F2937 | —                  | Headings, metrics, directions     |
| Text Secondary       | #6B7280 | —                  | Supporting metadata, timestamps   |
| Text Inactive/Muted  | #9CA3AF | —                  | Placeholder copy, past logs       |
| Disabled Fill        | #E5E7EB | —                  | Deactivated action states         |
| Disabled Text        | #9CA3AF | —                  | Deactivated button labels         |
+----------------------+---------+--------------------+-----------------------------------+
```

### 2.2 Semantic Life-Safety Mapping Rules

| State                  | Hex Accent | Background Fill | Border    | Icon            | Strict Rule                                                                                   |
| ---------------------- | ---------- | --------------- | --------- | --------------- | --------------------------------------------------------------------------------------------- |
| **Safe / Verified**    | `#43A047`  | `#E8F5E9`       | `#C8E6C9` | `CheckCircle2`  | Only used for officially confirmed safe paths, open shelters, and intact infrastructure.      |
| **Warning / Caution**  | `#FFA726`  | `#FFF3E0`       | `#FFE0B2` | `AlertTriangle` | Used for single-lane passability, rapidly rising water, or unverified crowdsourced reports.   |
| **Danger / Critical**  | `#E53935`  | `#FFEBEE`       | `#FFCDD2` | `AlertOctagon`  | Exclusively indicates impassable routes, collapsed bridges, active fire/flood zones, and SOS. |
| **Brand / Navigation** | `#1E88E5`  | `#E3F2FD`       | `#BBDEFB` | `Navigation`    | Directing movement, system controls, GPS lock, and user wayfinding.                           |
| **Neutral / Stale**    | `#6B7280`  | `#F3F4F6`       | `#E5E7EB` | `Clock`         | Telemetry pending verification or reports older than 15 minutes.                              |

---

## 3. Design Tokens (CSS Variables)

```css
:root {
  /* Surface & Base Canvas */
  --bg-canvas: #ffffff;
  --bg-surface-secondary: #f7f9fc;
  --bg-card: #ffffff;
  --bg-modal: #ffffff;

  /* Text & Typography */
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --text-on-primary: #ffffff;
  --text-on-safe: #ffffff;
  --text-on-danger: #ffffff;

  /* Brand Primary */
  --brand-primary: #1e88e5;
  --brand-hover: #1565c0;
  --brand-light: #42a5f5;
  --brand-surface: #e3f2fd;
  --brand-border: #bbdefb;

  /* Semantic Emergency States */
  --color-safe: #43a047;
  --color-safe-surface: #e8f5e9;
  --color-safe-border: #c8e6c9;

  --color-warning: #ffa726;
  --color-warning-surface: #fff3e0;
  --color-warning-border: #ffe0b2;

  --color-danger: #e53935;
  --color-danger-surface: #ffebee;
  --color-danger-border: #ffcdd2;

  --color-info: #42a5f5;
  --color-info-surface: #f0f7ff;
  --color-info-border: #dbeafe;

  /* Neutral Borders & Dividers */
  --border-subtle: #e5e7eb;
  --border-medium: #d1d5db;
  --border-strong: #9ca3af;

  /* Corner Radii */
  --radius-xs: 6px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-2xl: 24px;
  --radius-full: 9999px;

  /* Box Shadows (Soft, Diffuse, Ambient) */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-card:
    0 2px 8px -2px rgba(15, 23, 42, 0.06), 0 1px 4px -1px rgba(15, 23, 42, 0.04);
  --shadow-floating:
    0 10px 25px -5px rgba(15, 23, 42, 0.08),
    0 8px 10px -6px rgba(15, 23, 42, 0.04);
  --shadow-emergency: 0 12px 32px -4px rgba(229, 57, 53, 0.25);
  --shadow-primary-cta: 0 8px 20px -4px rgba(30, 136, 229, 0.35);

  /* Layout Spacing */
  --space-2xs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 20px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --space-3xl: 40px;

  /* Transitions */
  --motion-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --motion-standard: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --motion-enter: 300ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 4. Typography Scale & Hierarchies

`resQroute` specifies system-native, highly legible sans-serif typefaces (`Inter`, `-apple-system`, `SF Pro Display`, `Manrope`) tuned for high-stress optical recognition outdoors.

```
+---------------+-----------+-------------+-----------------+----------------------------------------+
| Level         | Size      | Weight      | Line Height     | Context                                |
+---------------+-----------+-------------+-----------------+----------------------------------------+
| Display (XL)  | 32px      | 800 (Bold)  | 38px (1.18)     | Emergency Banner Headline, Big Metrics |
| Heading 1     | 24px      | 700 (Bold)  | 30px (1.25)     | Screen Title (e.g. "Safe Havens")      |
| Heading 2     | 20px      | 600 (Semibd)| 26px (1.30)     | Shelter Names, Hazard Category         |
| Subhead       | 16px      | 600 (Semibd)| 22px (1.38)     | Card section header, Metric labels     |
| Body Primary  | 15px      | 400/500     | 22px (1.46)     | Route explainability, instruction copy |
| Body Small    | 13px      | 400/500     | 18px (1.38)     | Metadata, timestamps, geo-coordinates  |
| Caption / Tag | 11px      | 600 (Semibd)| 14px (1.27)     | Status chips, verified badges, pills   |
+---------------+-----------+-------------+-----------------+----------------------------------------+
```

### Typography Rules

- **No thin font weights:** Never use font weights below 400 (`normal`). Headings must be `600` or `700`.
- **High optical contrast:** Text primary (`#1F2937`) on pure white provides a 13.5:1 contrast ratio, far exceeding WCAG AAA requirements.
- **Numbers are tabular:** All telemetry data, ETAs, and bed counts use `font-variant-numeric: tabular-nums` to prevent layout jumps during live updates.

---

## 5. Layout, Spacing & Elevation

### 5.1 Spacing Scale

- Page gutters: `16px` or `20px` (mobile viewport edges).
- Card internal padding: `16px` to `20px` to give vital emergency facts room to breathe.
- Stack gap between cards: `12px` to `16px`.
- Inter-item gap inside cards: `8px` to `12px`.

### 5.2 Elevation & Border Radius

1. **Cards:** `16px` radius (`--radius-lg`), subtle hairline border `1px solid var(--border-subtle)`, ambient drop shadow `var(--shadow-card)`.
2. **Action Buttons:** `14px` or full pill `9999px` radius, minimum touch target `52px` height.
3. **Pills & Status Badges:** `9999px` full radius, `4px 10px` padding.
4. **Bottom Sheets & Floating Panels:** `24px` top radius (`--radius-2xl`), shadow `var(--shadow-floating)`.

---

## 6. Component Specifications

### 6.1 Dominant Action Buttons (The 3-Second Rule)

Emergency decision-making requires zero ambiguity. Every screen features **one dominant primary CTA** anchored at the bottom.

#### Primary CTA (Filled)

- Background: `var(--brand-primary)` (`#1E88E5`)
- Hover/Pressed: `var(--brand-hover)` (`#1565C0`)
- Text: `#FFFFFF`, `16px`, weight `700`, center-aligned
- Height: `54px` (touch target well above 48px Apple/Android minimums)
- Radius: `14px` (`--radius-md`)
- Shadow: `var(--shadow-primary-cta)`
- Left icon: Action icon (e.g. `Navigation`, `Send`, `ShieldCheck`), `20px`

#### Emergency Danger CTA (e.g., SOS / Immediate Report)

- Background: `var(--color-danger)` (`#E53935`)
- Text: `#FFFFFF`, `16px`, weight `700`
- Shadow: `var(--shadow-emergency)`

#### Secondary Button (Outlined)

- Background: `#FFFFFF`
- Border: `1.5px solid var(--border-subtle)`
- Text: `var(--text-primary)` (`#1F2937`), weight `600`
- Height: `48px`

---

### 6.2 Emergency Status Cards & Banners

#### Critical Hazard Alert Banner

- Background: `#FFEBEE` (`var(--color-danger-surface)`)
- Border: `1.5px solid var(--color-danger-border)` (`#FFCDD2`)
- Left accent bar: `4px solid var(--color-danger)`
- Header: Text `#C62828`, weight `700`, paired with pulsing `AlertOctagon` icon
- Subtext: `#B71C1C`, readable summary (e.g. _"Flash Flood Stage 3: North Basin Breached at Mile 4"_).

#### Safe Haven / Shelter Card

- Background: `#FFFFFF`
- Border: `1px solid var(--border-subtle)`
- Top Header: Shelter Name (`Heading 2`, `#1F2937`) + Distance chip (`14px`, `#6B7280`)
- Capacity Indicator: Dual-tone bar:
  - Fill: `var(--color-safe)` (`#43A047`) if `< 80%`
  - Fill: `var(--color-warning)` (`#FFA726`) if `80% - 95%`
  - Fill: `var(--color-danger)` (`#E53935`) if full (`100%`)
- Feature Chips: Soft pill badges `#F7F9FC` with icons:
  - `Wheelchair` (ADA Accessible)
  - `Zap` (Generator 100%)
  - `HeartPulse` (Medical Triage)
  - `Utensils` (Warm Meals)
- Freshness Stamp: _"Verified 45s ago by County Civil Defense"_ in `var(--color-safe)` text with miniature green dot.

---

### 6.3 Algorithmic Explainability Card (Why Route B was selected)

The cornerstone of user trust in `resQroute`:

- Outer container: `#F7F9FC` (`--bg-surface-secondary`) with `16px` radius.
- Rejection block (Route A):
  - Border: `1px solid #FFCDD2`
  - Fill: `#FFFFFF`
  - Badge: `REJECTED` in red pill `#FFEBEE` / `#E53935`
  - Bulleted explanations with red cross icons (e.g., _"Lower Canal overtopped (1.2m depth)"_).
- Selection block (Route B):
  - Border: `1.5px solid #C8E6C9`
  - Fill: `#FFFFFF`
  - Badge: `VERIFIED SAFE` in green pill `#E8F5E9` / `#2E7D32`
  - Bulleted justifications with green checkmarks (e.g., _"+35m Ridge elevation above surge line"_, _"100% Starlink relay mesh coverage"_).

---

### 6.4 Status Badges & Telemetry Chips

```html
<!-- Safe Chip -->
<span
  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold"
>
  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
  Verified Safe Corridor
</span>

<!-- Warning Chip -->
<span
  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-semibold"
>
  <span class="w-2 h-2 rounded-full bg-amber-500"></span>
  Single Lane Only (Debris)
</span>

<!-- Danger Chip -->
<span
  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold"
>
  <span class="w-2 h-2 rounded-full bg-rose-500"></span>
  Road Impassable
</span>
```

---

### 6.5 Form Elements & Hazard Reporting Pickers

- **Tactile Grid Buttons:** `2-column` grid with `64px` tap targets.
- State Default: Background `#FFFFFF`, border `1.5px solid var(--border-subtle)`, text `#1F2937`.
- State Selected: Background `var(--brand-surface)` (`#E3F2FD`), border `2px solid var(--brand-primary)` (`#1E88E5`), text `var(--brand-primary)`.
- Live Photo Upload Box: Dashed border `2px dashed #93C5FD`, background `#F0F7FF`, centered camera icon with high-contrast label.

---

### 6.6 Light-Themed Map Specification

The evacuation map must look like a high-end, clean consumer map (Apple Maps light mode) optimized for rapid spatial comprehension:

- **Map Base Canvas:** Warm porcelain / light silver (`#F3F4F6` terrain, `#FFFFFF` road vectors, `#D1D5DB` arterial boundaries).
- **Water Bodies / Inundation Contours:** Soft baby blue (`#BFDBFE`) with warning flood borders (`#EF5350` dashed).
- **Safe Evacuation Path:** High-visibility Solid Royal Blue line (`#1E88E5`), weight `6px`, with glowing directional chevrons or dots leading to a vibrant Green destination shelter beacon (`#43A047`).
- **Unsafe / Flooded Roads:** Solid Red line (`#E53935`), weight `5px`, overlaid with small diagonal white barrier hashes.
- **Shelter Pins:** White pill pins with blue border, showing green bed count badge (e.g. `[Pavilion • 280 beds]`).
- **User Location:** Pulsing cyan/blue dot with directional field indicator (`#1E88E5`).

---

### 6.7 Navigation Bar (Thumb-First Bottom Navigation)

Fixed at the bottom of the viewport:

- Height: `64px` (+ safe area inset for iOS home bar).
- Background: `#FFFFFF` with top border `1px solid var(--border-subtle)` and soft top shadow `0 -2px 10px rgba(0,0,0,0.03)`.
- Layout: 5 equal-spaced tabs:
  1. **Home** (`Home` icon)
  2. **Map** (`Compass` / `Map` icon)
  3. **Report** (Raised circular red button with emergency triangle, `48px` diameter)
  4. **Shelters** (`ShieldCheck` / `Building` icon)
  5. **Profile** (`User` icon)
- Active Tab: Icon and text in `var(--brand-primary)` (`#1E88E5`), font weight `700`.
- Inactive Tab: Icon and text in `var(--text-secondary)` (`#6B7280`), font weight `500`.

---

## 7. Motion & Interaction Standards

1. **Panic-Reduction Transitions:**
   - Alerts do **not** flash violently. Critical banners use a calm, smooth slide-and-fade in (`300ms`, `cubic-bezier(0.16, 1, 0.3, 1)`).
   - Live telemetry status badges use a gentle `2s` opacity pulse (`1.0` to `0.4` to `1.0`), never sharp blinking.
2. **Card Tap Feedback:**
   - Active tap: Subtle scale `scale(0.985)` with `100ms` duration for tactile confirmation under trembling fingers.
3. **Route Recalculation:**
   - When a safer corridor is found, the old path dissolves to faded red while the newly cleared ridge path draws forward in vibrant blue (`600ms` stroke animation).
4. **Accessibility Override:**
   - All animations automatically deactivate when `prefers-reduced-motion: reduce` is enabled.

---

## 8. Accessibility & Environmental Defense

- **WCAG Compliance:** Every text and interactive element achieves at least **WCAG 2.1 AA** (4.5:1 for normal text, 3:1 for large text); all core emergency instructions achieve **WCAG AAA** (7:1+).
- **Minimum Touch Targets:** `48px × 48px` absolute floor; primary action buttons standard at `54px` height with generous padding.
- **Color Blindness Redundancy:**
  - Red danger elements are _always_ paired with an octagon / warning cross and the word **"BLOCKED"** or **"IMPASSABLE"**.
  - Green safe elements are _always_ paired with a shield check and the word **"VERIFIED SAFE"**.
  - Amber warning elements are _always_ paired with a triangle and the word **"CAUTION"**.
- **Offline & Low-Bandwidth Mode:**
  - When connection degrades, header turns from live sync to a clean amber pill: _"Offline Mesh Relay Active • Cached 2m ago"_.

---

_resQroute Specification Authored for Civil Defense, Municipal Responders, and Public Citizens._
