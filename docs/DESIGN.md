# resQroute Design System & Visual Specification

## Design Philosophy & Color Palette
The visual identity of `resQroute` is designed around **Trust, High Contrast, and Immediate Visual Clarity**. 

The color system uses dark mode default backgrounds (`#0F172A`) to conserve mobile battery on OLED screens and minimize eye fatigue in dark disaster environments.

```
+-------------------------------------------------------------------------+
|                         RESQROUTE COLOR PALETTE                         |
+-------------------------------------------------------------------------+
| DEEP BLUE (#0F172A / #1E293B) : Backgrounds & Container Cards           |
| EMERALD GREEN (#34D399)      : Safe Routes / Verified Shelters / Action |
| CRIMSON RED (#F87171)        : Critical Danger / Hard Closures          |
| WARNING ORANGE (#FBBF24)     : Medium Risk / Unverified Reports / Stale |
| INTELLIGENCE PURPLE (#C084FC): Shadow ML Proposals / System Metadata    |
| SKY BLUE / CYAN (#38BDF8)    : Real-Time Information / Active Route     |
| CRISP WHITE (#F8FAFC)        : Primary High-Contrast Text               |
+-------------------------------------------------------------------------+
```

---

## 1. Design Tokens (CSS Variables)

```css
:root {
  /* Surface Colors */
  --bg-primary: #0f172a;
  --bg-card: #1e293b;
  --bg-border: #334155;

  /* Text Colors */
  --text-primary: #f8fafc;
  --text-muted: #94a3b8;

  /* Semantic State Colors */
  --color-safe: #34d399;
  --color-danger: #f87171;
  --color-warning: #fbbf24;
  --color-info: #38bdf8;
  --color-purple: #c084fc;

  /* Typography */
  --font-family: 'Inter', system-ui, -apple-system, sans-serif;
  --radius-card: 0.75rem;
  --shadow-emergency: 0 4px 20px rgba(0, 0, 0, 0.5);
}
```

---

## 2. Component Design Standards

### 2.1. Emergency Cards
- Background: `var(--bg-card)` (`#1E293B`)
- Border: `1.5px solid var(--bg-border)` or semantic color border for emergency state.
- Padding: `1.25rem` (20px)
- Border Radius: `var(--radius-card)` (12px)

### 2.2. Map Vector Styling Rules
- **Closed Road Edges**: Solid Red line (`#F87171`), weight 6px, with striped pattern overlay.
- **Active Hazard Polygons**: Semi-transparent Coral Red fill (`rgba(248, 113, 113, 0.25)`), border weight 2px.
- **Recommended Safe Route**: Solid Emerald Green line (`#34D399`), weight 7px, glowing aura.
- **Alternative Unsafe Route**: Dashed Slate line (`#64748B`), weight 4px.
- **Shelter Markers**: Custom SVG pins with green capacity chips displaying available count.
