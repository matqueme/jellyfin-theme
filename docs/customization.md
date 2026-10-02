# Customization

**English** · [Français](personnalisation.md)

Everything lives in [`../src/01-tokens.css`](../src/01-tokens.css). Modules
never hard-code a color, a radius or a duration: tweaking the theme means
editing that file.

| Token | Role |
|---|---|
| `--bg`, `--bg-raised`, `--bg-overlay` | Backgrounds: page, panels sitting on the page, floating things (menus, dialogs) |
| `--veil-1` to `--veil-3` | White veils: fields, secondary buttons, hovers. Correct on any background |
| `--line`, `--line-strong` | One-pixel rules |
| `--text`, `--text-2`, `--text-3` | Primary, secondary and muted text |
| `--primary`, `--on-primary` | Main action: white, with black text |
| `--danger`, `--success`, `--warning`, `--info` | The only saturated colors, all semantic |
| `--glass`, `--glass-strong`, `--glass-blur`, `--glass-edge` | Glass: header, drawer, playback bar (`--glass`); menus, dialogs (`--glass-strong`). The blur saturates what passes underneath, the edge carries a highlight |
| `--backdrop-dim` | Blur of the page behind an open dialog |
| `--shadow-float`, `--shadow-lift`, `--glow-primary` | Shadows for floating things and for a lifted card; glow of the main button on hover |
| `--hero-height`, `--hero-blur`, `--hero-veil` | Item page on desktop: height of the sharp image at the top, blur and veil of the content scrolling over it |
| `--card-lift`, `--card-zoom`, `--press` | Card hover (rise, image zoom) and pressed button. Disabled under `prefers-reduced-motion` |
| `--r-xs` to `--r-lg`, `--r-pill` | Radii: chips, fields, cards, dialogs, buttons |
| `--ring` | Focus ring, and hover ring of cards |
| `--icon-scale` | Size of Phosphor icons, which fill their box more than Material's |
| `--play-label` | Label of the Play button, written by the theme. `"Play"` by default, `"Lecture"` when the interface is in French (`:root:lang(fr)`). Keep the quotes: it is a `content` value |

Colors used with transparency also exist as channels
(`--primary-canal: 244 244 245`), the syntax MUI expects for its `*Channel`
variables. The two must stay in agreement.

To switch icons back to a thin stroke: replace `bold` with `regular` in the
`@import` of [`../src/00-imports.css`](../src/00-imports.css), and
`Phosphor-Bold` with `Phosphor` in
[`../src/90-icones.css`](../src/90-icones.css). Code points are identical
between the two weights. For MUI icons, replace `bold` with `regular` in the
`CORE` URL of [`../tools/icones-mui.py`](../tools/icones-mui.py) and run it
again.
