# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Semantic versioning, independent of Jellyfin's: compatibility is stated in the
title of each version.

The history up to 3.1.2 was originally written in French and translated
afterwards. File names under `src/` are French, and appear as they are.

## [3.2.3] - 2026-10-06 - Jellyfin 12.x, Modern layout

### Fixed

- Jellyfin 12.2 gave the "Reset filters" button of library pages a new
  icon (`FilterAltOff`) and changed the icon of mixed libraries from `Quiz`
  to `OndemandVideo` (`ondemand_video` in the older markup). Both were left
  as Material icons among the Phosphor ones; they are now a crossed-out
  funnel and a play screen, matching the rest of the interface.

## [3.2.2] - 2026-10-05 - Jellyfin 12.x, Modern layout

### Changed

- The "Skip intro / Skip credits" button (the client's media segment button,
  fed by Intro Skipper) kept the client's flat grey rectangle. It is now a
  frosted-glass pill with white text, like the theme's other floating
  surfaces, and turns solid white on hover like the primary buttons.

### Fixed

- Near the end of a film, the skip button sat right over the time bubble and
  trickplay thumbnail of the position bar, so you could not see where you
  were seeking (to watch the credits, for instance). As on Netflix, the button
  now fades out and ignores clicks while the bubble is shown, when hovering or
  dragging the bar, and comes back as soon as it hides.

## [3.2.1] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Fixed

- The theme was missing on the plugin configuration pages (`#/configurationpage?...`)
  and on `#/metadata`. `js/theme-dashboard.js` only recognised `#/dashboard`;
  it now covers the three prefixes of the client's admin pages.

## [3.2.0] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Changed

- Episode rows (season and collection pages), redesigned:
  - The thumbnails touched each other and had the corners of `.listItemImage`.
    They now have a gap and the 14px radius of the cards, and the row has a
    rounded hover background (20px) that wraps the thumbnail.
  - The thumbnail is smaller on desktop: 15.75vw (236px at 1500px) instead of
    19.5vw (293px), same proportions. Below 64em the client's own sizes apply.
  - Play button: the client draws a dark disc with a grey triangle that turns
    cyan and grows on hover, which is neither the theme's colour nor its
    motion. At rest it is a dark disc with a white icon; when the thumbnail is
    hovered it becomes the white disc with a black icon of the cards' play
    button, without growing.

### Fixed

- On desktop, only the small play button started an episode, although the
  whole thumbnail reacted to hover (the client wires no action on the
  thumbnail there). The button's `::before` now covers the whole thumbnail, so
  a click anywhere on it plays the episode. The button has no
  `backdrop-filter` for that: it would make the button the containing block of
  the `::before`.

## [3.1.9] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Changed

- Smaller profile picture in the header: 40px, against 22px for the icons next
  to it (in 46px buttons), so it dominated the bar. It is now 30px, in a 46px
  button like the others to keep the same hit area and spacing; a negative
  margin gives back the 8px of padding on the right so the picture's edge
  stays on the page's.

## [3.1.8] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Changed

- Smaller Jellyfin logo: the client sets it at 1.25em in the header (28px) and
  2.5rem in the drawer (37px), next to menu icons of 18px and 24px. In plain
  white it outweighed everything around it. It is now 20px in the header and
  26px in the drawer, a little above the icons because its shape is solid.

## [3.1.7] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Fixed

- Right margin of libraries, for real this time: the cards are percentages of
  the grid, but each one has a right margin of `.6em` of its own font size
  (17.9px, the last card of a row included), so the posters stopped 18px
  before the right margin while the first one touches the left one. That
  margin is now taken off the grid's right padding. Measured at 700, 1100,
  1500 and 1920px: left and right margins are equal. Not applied on TV, where
  the client uses a different card margin.

### Changed

- Active "played" and "favorite" buttons on cards: the client turns their icon
  red (`MuiSvgIcon-colorError`), the only loud colour on a card, and red read
  as an error. The active button is now a solid white pill with a dark icon,
  like on the item page, dimmed on hover. Same rule for the older cards of the
  home page.

## [3.1.6] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Changed

- Jellyfin logo in white: the client's default logo (header, drawer, loading
  screen, title of the TV app) is a purple-blue gradient, the last brand colour
  in a theme whose colour comes from the posters. It is now plain white
  (`brightness(0) invert(1)`); the gap between the two shapes is transparent,
  so the drawing stays readable. A custom logo set in the branding keeps its
  colours. The favicon and the TV app icon are outside the theme's reach.

## [3.1.5] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Fixed

- Uneven side margins in libraries: the client keeps the 7.5% right padding it
  reserved for the A to Z index (`padded-right-withalphapicker`) even when the
  index is hidden, against 3.3% on the left. The grid now has 3.3% on both
  sides.
- Active "played" and "favorite" buttons on the item page had no hover: their
  white fill was written after, and with the same weight as, the icon buttons'
  hover rule. They now dim to 78% on hover (60% when pressed), on pointer
  devices only.
- Same buttons on TV: the active fill was the same solid white as the focused
  button, so the two could not be told apart. The active button is now a veil
  with a white outline and a white icon; the focused one stays solid.
- Cast row of the item page on TV: the first card touched the edge of its
  scroller, whose `overflow: hidden` clipped the ring and the zoom of the
  focused card. On TV the client slides this row with a transform (no
  `scrollX` class), so the box is now widened by 1.25rem on each side and the
  space given back as padding; the edge fade is removed there.

## [3.1.4] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Fixed

- Hover of the first row of a library: the card rises by 6px and its ring
  overflows by 4px, but the page scrolls under the toolbar, which clips
  whatever goes past it, and the client only leaves 11px between the two: the
  top of the hovered card was cut off. The grid now starts 1.25rem below the
  toolbar. The home page was not affected.

## [3.1.3] - 2026-10-02 - Jellyfin 12.x, Modern layout

### Fixed

- Progress bar of library cards: it was blue (the client hard-codes
  `#00a4dc` on its MUI progress bar) on a thin white rail stuck to the edges
  of the poster, unlike the one on the home page. It now uses the same
  design: white bar on a dark blurred rail, 5px high, set off from the edges.
- Menus stuck to their trigger: MUI places a menu right under its button, so
  the profile menu and the library's view menu (Movies, Suggestions…) touched
  the edge of the button. They now sit 0.75rem lower.

- Library title ("Movies ▾"): the text and the arrow sat low in their pill.
  The boxes are centered, but Plus Jakarta Sans puts its baseline low in its
  line box: measured on the ink at 4x, the text was 0.75px under the center of
  the pill and the arrow 0.4px. Both are moved back up. On a phone (2x and 3x
  screens) they are now within one screen pixel of the center.

- Play button label always in French: the theme writes it itself
  (`--play-label`) and it read "Lecture" whatever the interface language. It is
  now "Play", and "Lecture" when the interface is in French.

### Removed

- The A to Z index on the right of libraries (`.alphaPicker-fixed-right`). It
  took a column of the page, overflowed the screen on some phones, and adds
  little next to search and sorting.

## [3.1.2] - 2026-09-30 - Jellyfin 12.x, Modern layout

### Fixed

Samsung (Tizen) app: it does not use the server's client but embeds its own,
a 10.11 client in TV layout. Checked by serving the 10.11.11 client with a
Tizen 9 user-agent.

- Big black frame between the poster and the white ring of the focused card:
  the client puts a transparent 0.5em border on every `.show-focus` card, and
  the page background showed through it. It is removed, the ring replaces it;
  the ring goes to 3px + 3px on TV so it reads from afar.
- Cropped header (logo, icons and clock cut off at the bottom): the tabs are
  pulled up into it by a -4.3em margin computed for the client's large tabs,
  and the header collapsed to 63px for 118px of content. The tabs now leave
  the flow and center on the top line.
- Header frozen above the content when scrolling: the home page's
  `overflow-x: hidden` made the page its own scroll container, whereas the
  10.11 client scrolls the window. On TV, `overflow-x: clip`.
- Glass without blur on TV (header, dialogs, chips): a `backdrop-filter`,
  recomputed on every scroll frame, stutters or renders in blocks on a TV. It
  becomes a nearly opaque flat fill, and the header, which scrolls with the
  page, is transparent. The wallpaper keeps its blur: a `filter` on the image
  is only computed once.
- Item page without an image on TV: the TV client hides the banner
  (`.itemBackdrop`). As on desktop, the background image stays sharp there and
  serves as the large poster, under a gradient; the content carries a
  blur-free veil that fades in under the buttons.
- Focused tab: the focus ring was doubled on top of the solid white.
- Settings unreadable with the remote: the focused row turned solid white, but
  its label and secondary texts stayed white. All the content of the focused
  element now takes black text.

## [3.1.1] - 2026-09-30 - Jellyfin 12.x, Modern layout

### Fixed

- MUI icons left in Material next to the Phosphor icons: Cast and SyncPlay in
  the header depending on their state (the Cast button becomes a labelled
  button during casting, and was only recognized by its French `aria-label`),
  library card buttons, menus and dashboard. The 130 SVG icons MUI can display
  are recognized by their `data-testid`, kept in production, and redrawn in
  Phosphor through a mask: size and color stay MUI's.
- Header never glass: in 12 it always carries the `MuiAppBar-colorTransparent`
  variant, which v3.0 turned into a blur-free gradient. And the content never
  passed underneath: the page scrolls in a container that starts below the
  header. On single-bar pages (home, search, lists, item page), that container
  now moves up under the header and its content keeps its place: when
  scrolling, posters pass behind the glass, which blurs them and takes their
  color. Libraries, whose bar changes height on mobile, keep the client's
  behavior.
- Item page on phone: the client does not load the fixed background image
  there, so the page had neither the colored background of desktop nor an
  image under the header. The banner now moves up under the header and
  continues under the content as a blurred ambiance, with a fade from the
  sharp image. Play goes full width, the round buttons below it: on a centered
  row, the last one wrapped alone below 412px. The poster's shadow is reduced,
  it used to fall on the Play button.
- Chevron of section titles ("Films, recently added ›"): it sat below the
  text line, especially on mobile (client margins in em of different font
  sizes, title padding in mobile layout). Aligned on the baseline and lowered
  by 0.14em: centered on cap height to within 0.5px, measured on ink on real
  pages. On hover it used to grow (its offset cancelled the Phosphor
  reduction) and a veiled pill appeared behind the whole title: it now only
  slides and brightens.
- Same transform conflict elsewhere: the arrow of expandable sections no
  longer flipped once open, and the icon of image-less cards was no longer
  centered.
- Scrollbar: on touch screens, styling `::-webkit-scrollbar` replaced the
  native thin, temporary bar with a thick, permanent one, even under every row
  of cards. It is hidden on touch, where you scroll with a finger. With a
  mouse, Chrome ignored the theme's bar (it neutralizes it as soon as
  `scrollbar-width` is set) and drew its own, arrows included:
  `scrollbar-width` is reserved for Firefox, Chrome gets the thin pill without
  arrows.

### Added

- `src/91-icones-mui.css`, generated by `tools/icones-mui.py` from an MUI icon
  -> Phosphor table. An icon that has an already-remapped Material equivalent
  gets the same glyph. Checkboxes, radio buttons and the dropdown arrow stay
  drawn by their own modules.

## [3.1.0] - 2026-09-30 - Jellyfin 12.x, Modern layout

The base stays neutral, but color now comes from posters and backgrounds: the
glass lets it through, the cards move.

### Added

- More present glass: 28px blur saturated at x1.8 and a highlight on the edge
  (`--glass-edge`), applied to the header, the drawer (permanent one included),
  menus, action sheets, dialogs, notifications and tooltips. The page behind an
  open dialog is slightly blurred.
- Cards: on hover the poster lifts with a slight bounce, its image zooms
  within the frame, and the white ring comes with a shadow. The bottom buttons
  become fixed-size glass chips.
- Item page: round glass buttons over the background image; white glow on
  hover of the Play button and of the main buttons.
- Login: glass panel under a white halo.
- Item page on desktop: the background image stays sharp at the top of the
  page (`--hero-height`), and the content blurs it as it passes over
  (`--hero-blur`, `--hero-veil`), with a fade under the title. The client only
  fills the `#itemBackdrop` banner in mobile layout: the fixed-background
  image serves as the hero. Soft shadow on the title and logo, which overflow
  onto the image.
- Buttons: slight compression on click.
- New tokens: `--glass-strong`, `--glass-edge`, `--backdrop-dim`,
  `--shadow-lift`, `--glow-primary`, `--ease-spring`, `--t-slow`,
  `--card-lift`, `--card-zoom`, `--press`. Motion is disabled under
  `prefers-reduced-motion`.

### Fixed

- Card ring, shadow and hover cut off sharply: the client sets
  `contain: layout style paint` on every card, and paint containment clips like
  an `overflow: hidden`. Brought back to `layout style`. Natively scrolling
  rows (`.scrollX`, touch) get a vertical margin for the same reason.
- Background image never visible: `.backgroundContainer` covered it with an
  opaque flat fill. Replaced by a gradient veil, and the image is more
  saturated.
- Play button icon on cards invisible (white on white): the generic hover of
  icon buttons won over it.
- Login page portraits shrunk to 24px: their percentage width was computed for
  a full-page grid.
- Item page in a narrow window (under ~1000px, desktop layout): the title
  collapsed to 0px wide, squeezed by the button row. The buttons now go under
  the title below 62.5em, and the title may wrap. Without a background image,
  the top area is no longer a 400px void.

## [3.0.0] - 2026-09-25 - Jellyfin 12.x, Modern layout

Complete rewrite. No third-party base anymore: Ultrachromic is removed, along
with all the rules that existed to fix it. The theme is now a token system and
one module per component family, applied to the whole app, dashboard included.

### Direction

- Neutral, untinted surfaces: the blue-violet accent of v2 is gone.
- White becomes the action color: Play button, main buttons, checked
  checkboxes, switches, progress bars, selected item.
- Depth through the brightness of surfaces and one-pixel rules, with no
  colored glows or drop shadows. The only saturated colors are semantic:
  error, success, warning.

### Added

- `src/01-tokens.css`: every value of the theme (backgrounds, veils, rules,
  text, semantic colors, glass, radii, focus ring, motion).
- `src/02-palette-jf.css`: the tokens wired to the `--jf-*` variables, read by
  both MUI and the client's base theme.
- One module per component family, each covering the client's legacy component
  and its MUI equivalent: buttons, fields and dropdowns, checkboxes and
  switches, floating surfaces (menus, dialogs, action sheets, tooltips,
  alerts), lists and tables, tabs and chips.
- `js/theme-dashboard.js`: in 12, branding CSS is not applied to the
  dashboard. This script, to install with JavaScript Injector, loads the
  stylesheet served at `/Branding/Css` there.
- `src/95-plugins.css`: Jellyfin Enhanced quality labels brought back to dark
  glass labels, Jellyseerr's season picker, bookmark tabs.
- Icons: `edit`, `image`, `refresh`, `video_library` and `tune` remapped to
  Phosphor, and the Collections icon of the top bar (`#/boxsets`).

### Removed

- Ultrachromic (`src/vendor/`, `vendor.list`, `vendor.exclude`,
  `update-vendor.sh`, the `veille-upstream` workflow).
- The Legacy layout: `.skinHeader` tabs and header, and the height
  compensations they required.
- Modules 02 to 25 of v2, replaced by the component modules.

### Changed

- `build.py` now only concatenates `src/` and checks the result.
- The built file goes from 123 KB to 83 KB.

## [2.0.0] - 2026-09-15 - Jellyfin 12.x

Port to Jellyfin 12, whose **Modern** layout is now the default. A major
version because the target changes, not because the theme was redone: most of
it did not move, and that is the striking fact of this port.

### Context

12 is not a new client. The item, login and list pages, the preferences and
the queue are still rendered by the earlier controllers, **Modern included**:
this is explicit in the client's source, `src/apps/modern/routes/legacyRoutes/`.
And the cards, although rewritten as React components, emit the same class
vocabulary as in 10.11 (`cardScalable`, `cardContent`, `cardText`,
`innerCardFooter`, `cardOverlayButton`, `cardIndicators`). Finally
`layout-desktop`, `layout-mobile` and `layout-tv` are still set on `<html>` by
`layoutManager`, even in Modern.

Consequence: modules 02 to 22 apply unchanged. What changes is the styling of
the header, the drawer and the toolbars, redone in MUI.

### Added

- `src/23-modern.css`. Styling of the four elements 12 renders in MUI: header,
  drawer, selected entries, library navigation. Two anchors, chosen for their
  lifespan:

  - the **MUI component classes** (`.MuiAppBar-root`, `.MuiDrawer-paper`,
    `.Mui-selected`, `.MuiButton-colorPrimary`), which are part of MUI's public
    API. They replace the `css-4yt2of`, `css-17c09up` and `css-fknfom` hashes
    that Ultrachromic still targets: Emotion recomputes them as soon as
    upstream styles move, and they already matched nothing in 12.1;
  - the base theme's **`--jf-*` variables**, which 12 introduced and which its
    source presents as exposed for custom themes. The preset's accent is wired
    into them, so MUI components stop falling back to the default Jellyfin
    blue.

  Library navigation reuses the pill of `05-onglets.css`, with the same
  values, so that both layouts look alike: light gray for the current view,
  accent reserved for remote-control focus.

- `src/25-icones-mui.css`. The icons of the Modern bar are MUI SVG components:
  the drawing is in the markup and not in a font, and the `data-testid` that
  named them is stripped from the production build — checked in the served
  bundle. The method of `07-icones.css`, which remaps `.material-icons.<name>`
  to Phosphor, therefore cannot apply to them. The chosen hook is the link's
  route, stable and language-independent: `appRouter` builds `#/movies?`,
  `#/tv?`, `#/music?` from the collection type. The SVG is hidden, the
  Phosphor glyph set in `::after`. Cast and SyncPlay being neither links nor
  carrying an identifier, they go through `aria-label`, hence through French;
  in another language these two icons stay SVG and nothing else moves.

- `src/24-champs.css`. See "Fixed".

- `--accent-canal` in `src/01-reglages.css`. Same color as `--accent`, as
  space-separated components: MUI expects this syntax for its `*Channel`
  variables, where comma notation is invalid.

### Changed

- Ultrachromic resynchronized on [`1398af2`](https://github.com/CTalvio/Ultrachromic/tree/1398af21b8fe120a972bd00942ad60a76a932647).
  Upstream fixed for 12: the item page poster is `position: relative` again
  and accepts transforms, the title logo is scoped to `.layout-desktop` and
  gets proper placement on TV, borderless fields get their padding back. The
  modules that 08, 10, 11, 12 and 13 depend on — `hoverglow`,
  `overlayprogress`, `cornerindicator` — are unchanged, checked before
  accepting the diff.

- `build.py` announces the 12.x target in the header of the built file.

### Fixed

- The gap at the top of list pages in Modern. Ultrachromic offsets
  `#indexPage` and the like by 68px, or 130px under 100em wide, to clear
  Jellyfin's fixed header; `05-onglets.css` added 100px of the same kind on
  phones. In Modern these values are empty space: the legacy header is no
  longer displayed, and the MUI bar is an `OffsetAppBar`, which sets its own
  footrest of the height it measures. Neutralized in `23-modern.css`, under
  `:root:has(.MuiAppBar-root)` — Legacy having no MUI AppBar in its tree, the
  condition serves as a layout test.

- The circle arcs floating to the right of the library bar's buttons. The bar
  assembles its buttons as a `MuiButtonGroup`, where MUI draws a one-piece
  group with only the ends rounded, and separates its members with a one-pixel
  right border. The pill of `23-modern.css` rounded each of them to 999px:
  that border followed the curve. Only the sides that touch are now
  straightened, through `MuiButtonGroup-firstButton`, `-lastButton` and
  `-middleButton` — going through the ends rather than flattening `-grouped`
  avoids flattening a group reduced to a single button.

- The bar's item counter, oval on a single digit. MUI gives the chip a fixed
  height and side padding; a `min-width` equal to the height makes it a circle
  as long as the text fits, and lets it stretch when pagination fills it with
  a range.

- The readability of the episode counter, which read dark gray although its
  computed color is indeed `rgb(255, 255, 255)`. The cause is an inherited
  property: Ultrachromic sets `text-shadow: 0 0 4px rgba(0,0,0,.6) !important`
  on `body`, and `text-shadow` flows down the whole document. In front of a
  poster, on a title, that is what makes it legible; on the digit of an
  11px-high chip, a black shadow blurred over 4px with no offset overflows the
  glyph and drowns its inside. Turned off on chips, which have a solid
  background and need none. The background goes to 95% opacity along the way,
  with a dark rendered hairline — `indicator_floating.css` removes the one
  Jellyfin sets.

- Squashed dropdowns. A regression from Ultrachromic, not from Jellyfin:
  `fields_noborder.css` recently overrides `.emby-select`'s padding with
  `0 1.9em 0 .35em !important`. No vertical padding anymore, hence a field as
  tall as its line of text, and a label running into the curve of the pill
  that `rounding.css` draws around it. `24-champs.css` restores Jellyfin's
  values, with 0.75em on the left to account for that rounding.

### Removed

- `js/onglets-dans-la-page.js` and the rules of `05-onglets.css` that
  depended on it. The script cloned the header's tab row into the scrolling
  area, on phones, because CSS cannot reparent an element and those tabs lived
  in a `position: fixed` header. In 12 that header is no longer displayed and
  navigation goes through the MUI bar: the script has no purpose left. Also
  removed from the JavaScript Injector plugin's configuration, where
  `apply-js.sh` had written it.

## [1.3.0] - 2026-08-23 - Jellyfin 10.11.x

### Added

- `src/19-rangees-degrade.css`. A row of cards carries the page gutter itself
  (`.padded-left` / `.padded-right`, `3.3%`), and padding is part of the
  clipping box: `overflow-x` cuts at the **outer** edge of the gutter. As long
  as the row has not scrolled the inset shows, and from the first scroll the
  cards cross it and touch the screen edge, while the section title stays
  aligned on the column. This is the left overflow visible on PC and on TV.

  Fixed with a gradient mask rather than margins: a margin would bring the
  clipping edge in to the cards' alignment and cut off the TV focus ring of
  the first card, which overflows its box. The mask is attached to the box and
  not to the content; the fade equals exactly the gutter, so the first card at
  rest is intact and only its halo fades as it overflows. Under `@supports`: a
  TV browser that ignores `mask-image` gets the previous behavior.

- `src/20-page-item-mobile.css`. The phone was the only layout left on the
  default rendering of an item page. `title_simple.css` makes `.detailRibbon`
  transparent, but under `.layout-desktop` only, and TV gets its
  `background: none` from `themes/dark`: the phone falls in neither case and
  kept `rgba(32, 32, 32, .8)`, a full-width gray slab under the background
  poster, where title, information and buttons piled up.

  Three fixes that go together: the slab disappears, the bottom of the
  background poster dissolves instead of being cut off, through a mask and not
  a color gradient, so nothing to match with the page background, and the
  image moves up under the header. That last one is not an addition but a
  removal: `#itemDetailPage` is a `.selfBackdropPage`, set to `padding-top: 0`
  precisely so its image starts at the top edge, and Jellyfin already gives it
  a `::before` veil that fades out over the height of a header. The `4rem`
  margin set by `fixes.css` made that veil useless and left a black strip that
  desktop never had.

- `src/21-info-media.css`. The rating and the subtitles marker are the only
  two `.mediaInfoText` of an item page; the rest of the row is bare text. They
  nevertheless received a 20% blue-gray flat fill, hence a color that depends
  on what is underneath: legible on the page background, washed out on a light
  poster. They take the theme's grammar again, an outline and not a fill, and
  the capsule of sections 2 and 18. In white and not in the accent: this chip
  signals neither a state nor an action, it files a piece of information among
  others.

- `src/22-liste-progression.css`. `overlayprogress.css` stretches the progress
  bar to `2000em` to make it a veil, and targets two pages by ID for that.
  Section 11 catches the case of cards; list rows, those of a season's episode
  list, which is precisely on `#itemDetailPage`, were caught by nothing. The
  same state, "started, not finished", therefore read as a floating bar on a
  thumbnail, as a half-tinted row just below, and as a `.28em` line on pages
  where the ID does not match: three renderings for one state. The list row
  now aligns on the card and reuses section 11's variables as they are.

## [1.2.0] - 2026-08-19 - Jellyfin 10.11.x

### Added

- `src/16-tv-focus.css`. On TV, the focused card was ringed by a `.5em` blue
  frame, with `#00a4dc` hard-coded in `themes/dark/theme.css` and unrelated to
  the theme's accent. The origin is not a Jellyfin choice but a detection:
  `cardBuilder` only sets `.show-animation` under
  `!browser.slow && !browser.edge`, and Tizen falls into "slow". The focus
  zoom planned by the client, `scale(1.07)`, therefore never reaches the TV,
  and only the fallback frame remains. The module restores both: a thin ring
  in the accent, and the enlargement the TV should have had.

  The zoom required removing `contain: paint` from the focused card alone,
  otherwise paint containment clipped it right at its edge. The vertical
  clearance already existed: Jellyfin carries `padded-top-focusscale`
  (`margin-top: -1.5em; padding-top: 1.5em`) on its rows, which bounds
  `--tv-card-zoom` to about 1.15 before the card gets cut off by `.scrollX`'s
  `overflow-y: hidden`.

  The module also takes over the movie page's buttons: no more flat fill on
  focus, the accent moves to the stroke, as Jellyfin does for the header icons
  on TV. And the Play button, already in the accent at rest, signals itself
  with a white ring: lightening it was not visible from an armchair, and
  inverting it to a white fill made a break where it is only about marking a
  state.

- `src/17-boutons-survol.css`. A single hover language for secondary buttons:
  header icons, the movie page's row, the selection banner. All received a flat
  fill in the accent, but through two distinct rules,
  `.paper-icon-button-light:hover` and `.button-flat:hover`, which explains why
  a fix on one did not carry over to the other.

  The flicker on the movie page came from `effects/glassy.css`: hover creates
  a compositing layer **and** requests a `backdrop-filter: blur(4px)` at the
  same moment. On an item page the header is `.semiTransparent`, set on the
  background poster: there is material to blur and the transition shows. On the
  home page it sits over a dark flat fill, and the same rule produces nothing
  visible.

- `src/18-selection.css`. The selection banner was `rgba(var(--accent), .8)`,
  so 20% of the page scrolled through it, and stuck edge to edge whereas
  everything else in the theme floats. It takes the surface of the other
  floating elements, a very dark background and backdrop blur like `.dialog`
  and `.toast`, and the accent is a hairline again there.

  The cards took a detour. `.itemSelectionPanel` is set on **all** cards as
  soon as selection mode starts, not only the checked ones: Ultrachromic's
  accent veil therefore tinted the whole grid, and the accent distinguished
  nothing. Worse, nothing in the DOM marks a checked card: the selection
  module only holds an array of IDs in JavaScript and toggles `input.checked`,
  never setting a class. Hence a two-stage split: a neutral veil and a clearly
  visible checkbox, which any engine can render; then the accent ring on the
  checked card, under `@supports selector(:has(*))`, since it has to climb
  from the field to its ancestor.

- `--btn-hover-bg` in `src/01-reglages.css`, `--tv-card-ring` and
  `--tv-card-zoom` in `src/16-tv-focus.css`.

### Removed

- `.mainDetailButtons .detailButton { align-self: center !important }` in
  `src/03-page-item.css`. Dead rule: Jellyfin already sets `align-items: center`
  on `.mainDetailButtons`, and nothing declares `align-self` on these buttons:
  it restated the computed value.
- Two of the three cancellation selectors of `src/12-carte-zone.css`.
  `.card-hoverable` is carried by `.card` itself and `.cardBox` is a child of
  it: the three weigh 0-3-0 and designate the same set of elements. The top
  one is enough, the other two only named the targeted rules, which the
  comment already does.

  Checked mechanically before cutting: every class targeted by `src/*.css`
  still exists in the served client, and the (selector, property) pairs
  declared several times are otherwise all legitimate overrides of
  Ultrachromic.

## [1.1.1] - 2026-08-12 - Jellyfin 10.11.x

### Fixed

- A horizontal scrollbar appeared at the bottom of the home page, although no
  content actually overflowed the page. `src/15-barre-defilement.css` closes
  the axis on `#indexPage` and its three sibling pages.

  The origin is indirect: `header_transparent-dashboard.css` sets
  `overflow-y: scroll` on these pages so they scroll under the transparent
  header, and the CSS spec then requires the horizontal axis, left at
  `visible`, to compute as `auto`. The page container became laterally
  scrollable for a one-pixel overflow. Jellyfin itself sets no `overflow` on
  its page containers. Card rows keep their own `.scrollX` scroller: you keep
  scrolling along the row.

## [1.1.0] - 2026-08-12 - Jellyfin 10.11.x

### Removed

- `smallercast.css` is no longer loaded: its 18 media queries shrank and
  squared the cast thumbnails. Jellyfin's portrait thumbnails are restored.

### Added

- `src/vendor.exclude`, the only way to remove a module from the preset
  without modifying upstream, which would make `update-vendor.sh` conflict on
  every resync. `build.py` refuses to build if an entry is never encountered,
  and the built file carries the list of what was actually omitted.
- `src/14-carte-fond.css`. `smallercast.css` also carried a global
  `.cardPadder` rule, unrelated to the cast: it neutralizes the placeholder
  background shown under each thumbnail before its image loads. It is taken
  over identically, otherwise that background reappeared on every grid.

### Fixed

- `build.py` reported characters under the "bytes" label. Em dashes weigh
  three each in UTF-8, hence a gap of 18 with what the CDN returned.
- The four scripts were recorded as `100644`. The repository lives on a
  Windows drive, hence under `core.filemode false`, where `chmod +x` no longer
  affects what git records: they arrived non-executable on a Linux clone and CI
  failed with exit code 126.

## [1.0.0] - 2026-08-12 - Jellyfin 10.11.x

First published version. Takes over the `ultrachromic.css` maintained by hand
until then, byte for byte, reorganized into modules.

### Added

- Build by `build.py`: Ultrachromic and the in-house modules merged into a
  single `dist/theme.css`, served by jsDelivr in one request.
- Ultrachromic vendored and pinned on `fa158a2`. The upstream repository has
  no tag or release, so an unversioned URL pointed at the HEAD of `main`: the
  theme was built on a moving target.
- `update-vendor.sh` to resynchronize that copy, without committing, so the
  diff can be read before accepting it.
- Blocking checks at build time: balanced braces, no `@import` after a rule,
  `display: !important` guarded by `:not(.hide)`.
- `apply-local.sh` and `apply-js.sh` configurable through `JELLYFIN_DIR`,
  `JELLYFIN_CONTAINER` and `JELLYFIN_URL`.

### Changed

- Remote `@import`s are hoisted to the top of the built file, wherever they
  sit in the sources.
- Ultrachromic's image URLs, which pointed at its `main` branch, are pinned
  to the vendored commit.
- `apply-local.sh` escapes XML instead of forbidding `<` and `&` in the CSS.
  That prohibition had become untenable: `jf_font.css` imports Google Fonts
  with an `&` in its URL. Unescaping is checked by reading it back.

### Fixed

- Three to four levels of cascading `@import` at runtime, the cause of the
  flash of unstyled UI on first load and of `--accent` arriving late.

[1.1.1]: https://github.com/matqueme/jellyfin-theme/releases/tag/v1.1.1
[1.1.0]: https://github.com/matqueme/jellyfin-theme/releases/tag/v1.1.0
[1.0.0]: https://github.com/matqueme/jellyfin-theme/releases/tag/v1.0.0
