# Development

**English** · [Français](developpement.md)

Guide for contributing to or modifying the theme. To simply use it, the [README](../README.md) is enough.

## Structure

```
src/
  00-imports.css        remote fonts, the only @imports of the built file
  01-tokens.css         every value of the theme
  02-palette-jf.css     tokens wired to the client's and MUI's --jf-* variables
  10-base.css           background, font, text, links, scrolling, focus
  20-boutons.css        primary, secondary, quiet, destructive, icons, groups
  21-champs.css         text inputs and dropdowns
  22-cases.css          checkboxes, radio buttons, switches, sliders
  23-surfaces.css       menus, dialogs, action sheets, tooltips, alerts
  24-listes.css         lists, tables, MUI cards, pagination, loading
  25-onglets-puces.css  tabs, chips, badges
  30-entete-tiroir.css  MUI header, library navigation, drawer
  40-cartes.css         posters: hover, indicators, progress, selection
  41-rangees.css        section titles, rows, alphabet picker
  50-page-item.css      movie, series and season pages
  51-connexion.css      login page
  60-lecteur.css        OSD, playback bars, now playing, "Up next"
  80-tv.css             remote-control navigation
  90-icones.css         Material icons (font) remapped to Phosphor
  91-icones-mui.css     MUI's SVG icons redrawn in Phosphor (generated)
  95-plugins.css        what plugins add, brought into line
tools/icones-mui.py     generates 91-icones-mui.css from its table
js/                     behaviors that cannot be done in CSS
dist/theme.css          built and committed file: this is what the CDN serves
```

(Module file names are in French, as the code comments are.)

**Module order matters.** The numeric prefixes set the concatenation order,
hence the cascade: tokens first, then generic components, then pages, which
can specialize them.

### Two families of components

Jellyfin 12 mixes two generations of components, and the theme aligns one
with the other, module by module:

- the **legacy** ones (`.emby-button`, `.emby-input`, `.emby-select`,
  `.actionSheet`, `.listItem`…), on the pages 12 still renders with its
  older controllers, **Modern layout included**: item page, login, lists,
  part of the preferences;
- the **MUI** ones: header, drawer, library toolbars, display preferences,
  dashboard.

Two levers, in this order:

1. the **`--jf-*` variables** (`02-palette-jf.css`). The client builds its
   MUI theme out of CSS variables, and its base theme also colors the legacy
   components from the same variables. Setting them themes a good part of the
   app at once;
2. the **component classes**: `.emby-*` on one side, `.MuiButton-root`,
   `.MuiFilledInput-root`, `.Mui-selected`… on the other. They are part of
   MUI's public API. Never target the `css-xxxxxx` classes that Emotion
   generates alongside: they are hashes recomputed on every release.

`dist/theme.css` is a built file: never edit it, it is rewritten on every
build. jsDelivr serves from the git tree, which is why it is in the commits.

## Working on the theme

```bash
./build.py
```

Concatenates `src/` into `dist/theme.css`, then checks the result. The checks
are blocking: balanced braces, no `@import` after a rule, and every `display`
with `!important` guarded by `:not(.hide)`.

```bash
./apply-local.sh
```

Builds, writes `dist/theme.css` into the server's `branding.xml`, restarts the
container, then checks that `/Branding/Css` returns **exactly** the expected
file. The default path is `~/docker/jellyfin`; otherwise
`JELLYFIN_DIR=/srv/jellyfin ./apply-local.sh`.

```bash
./apply-js.sh js/*.js
```

Injects the scripts into the JavaScript Injector plugin's configuration:

- `theme-dashboard.js`: applies the theme to the dashboard (see
  [Installation](../README.md#dashboard));
- `replace-sync-button.js`: replaces the header's SyncPlay button with an
  entry in the preferences menu.

> The plugin patches the `index.html` served by the server. The Tizen app
> embeds its own copy of the web client and never receives it: only
> `/Branding/Css` reaches it. Everything TV-related is therefore done in CSS.

### On a Windows drive mounted in WSL

The repository asks for `core.filemode false`: `drvfs` reports every file as
777, and without this setting git would see permission changes everywhere.
Corollary: `chmod +x` has no effect on what git records. For any new script:

```bash
git update-index --chmod=+x my-script.sh
```

## Releasing a version

The tag and the release are created by GitHub Actions from the `VERSION`
file. There is nothing to tag by hand:

1. Edit `VERSION` and add the matching section to `CHANGELOG.md`.
2. `./build.py`: the header of `dist/theme.css` carries the new number.
3. Commit, push to `main`.

The `publier` workflow checks the build, refuses a version without notes in
the `CHANGELOG`, creates the `vX.Y.Z` tag, then the release whose notes are
that section. It does nothing if the tag already exists.

Tagged jsDelivr URLs are **immutable and cached forever**: no purge needed,
and rolling back means putting the old tag back. To follow `main` anyway,
purge after every push:

```bash
curl -s https://purge.jsdelivr.net/gh/matqueme/jellyfin-theme@main/dist/theme.css
```

## Pitfalls

Written down after running into them. Each one fails silently, with no
console error.

**The dashboard does not receive the branding CSS.** See
[Installation](../README.md#dashboard). Without `theme-dashboard.js`, the
admin area stays on the default theme, Jellyfin blue included.

**The `--jf-*` variables go on `:root[data-theme]`, not on `:root`.** MUI
declares them on `:root, [data-theme="dark"]` and inserts its stylesheet at
runtime, after ours: at equal specificity, its variables win.
`:root[data-theme]` weighs 0-2-0 and comes out ahead, whichever theme is
chosen in the preferences.

**MUI hard-codes its font.** The `--jf-font-*` variables exist but components
do not read them: the font is set again component by component in
`10-base.css`.

**Every `display` with `!important` must be guarded by `:not(.hide)`.**
Jellyfin hides its pages with `.hide { display: none !important }`. An ID
selector beats a class at equal `!important`: without this guard, the login
page stayed displayed on top of the home page. `build.py` refuses to build
without it.

**The links on the details sheet are buttons.** Tags, external links,
director: these are `a.button-link.emby-button`. Any rule set on
`.emby-button` reaches them; `50-page-item.css` flattens them back.

**MUI icons are recognized by their `data-testid`.** MUI renders its icons as
SVG, with `data-testid="CastIcon"`, kept in production. It is the only hook
that depends neither on the language (`aria-label`) nor on the component's
state: the Cast button becomes a labelled button while casting.
`91-icones-mui.css` hides the SVG's paths and paints it in `currentColor`
through a Phosphor mask: size and color stay MUI's. An icon missing from the
`tools/icones-mui.py` table keeps its Material drawing.

**A ligature icon cannot be remapped.** `90-icones.css` acts on the class
(`.material-icons.play_arrow`). An icon written as a ligature, whose name is
the tag's text (`<span class="material-icons">key</span>`, common in
plugins), stays Material: no selector can match an element's text.

**The layout is chosen from the user-agent.** With "Display mode: Auto", a
desktop browser shrunk to 390 px stays in `layout-desktop`. To test the phone
rendering, you need a mobile user-agent, not just a narrow window.

**The `background` shorthand resets `background-image` to `none`.** The
header's profile button, whose avatar is an inline `background-image`, lost
its image on hover. Write `background-color` whenever only the color is
wanted.

**TV is not a layout, it is also a slowness detection.** `cardBuilder`
tells `.show-focus` from `.show-animation` with
`!browser.slow && !browser.edge`, and Tizen is classed as "slow". Check which
of the two classes is set before overriding a focus state.

**Nothing marks a selected card in the DOM.** The only signal is
`input.chkItemSelect:checked`, lower in the tree than what you want to paint:
hence `:has()`, under `@supports selector(:has(*))` for TV browsers older
than Chromium 105.

**`<` and `&` are allowed.** The CSS is stored as text in `branding.xml`;
`apply-local.sh` escapes it and checks the unescaping by reading it back.
