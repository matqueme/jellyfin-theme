# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Versionnage sémantique, indépendant de celui de Jellyfin — la compatibilité
est indiquée par le titre de chaque version.

## [1.2.0] — 2026-08-19 — Jellyfin 10.11.x

### Ajouté

- `src/16-tv-focus.css`. Sur TV, la carte visée était cernée d'un cadre bleu
  de `.5em`, au `#00a4dc` codé en dur dans `themes/dark/theme.css` et sans
  rapport avec l'accent du thème. L'origine n'est pas un choix de Jellyfin
  mais une détection : `cardBuilder` ne pose `.show-animation` que sous
  `!browser.slow && !browser.edge`, et Tizen tombe dans « slow ». Le zoom de
  focus prévu par le client, `scale(1.07)`, n'atteint donc jamais la TV, et
  il ne reste que le cadre de repli. Le module rend les deux : anneau fin à
  l'accent, et l'agrandissement que la TV aurait dû avoir.

  Le zoom demandait de retirer `contain: paint` de la seule carte visée —
  le confinement de peinture le rognait pile à son bord. Le dégagement
  vertical, lui, existait déjà : Jellyfin porte `padded-top-focusscale`
  (`margin-top: -1.5em; padding-top: 1.5em`) sur ses rangées, ce qui borne
  `--tv-card-zoom` à 1.15 environ avant que la carte se fasse couper par
  l'`overflow-y: hidden` de `.scrollX`.

  Le module reprend aussi les boutons de la page d'un film : plus d'aplat au
  focus, l'accent passe sur le trait, comme le fait Jellyfin pour les icônes
  de l'en-tête en TV. Et le bouton Lecture, déjà à l'accent au repos, se
  signale par un anneau blanc : l'éclaircir ne se voyait pas d'un fauteuil,
  et l'inverser en fond blanc faisait une rupture là où il ne s'agit que de
  marquer un état.

- `src/17-boutons-survol.css`. Un seul langage de survol pour les boutons
  secondaires : icônes de l'en-tête, rangée de la page d'un film, bandeau de
  sélection. Tous recevaient un aplat à l'accent, mais par deux règles
  distinctes — `.paper-icon-button-light:hover` et `.button-flat:hover` —
  ce qui explique qu'une correction sur l'une ne se répercutait pas sur
  l'autre.

  Le scintillement sur la page d'un film venait de `effects/glassy.css` :
  le survol crée une couche de composition **et** demande un
  `backdrop-filter: blur(4px)` au même instant. Sur une page d'item
  l'en-tête est `.semiTransparent`, posé sur l'affiche de fond : il y a de
  la matière à flouter et le passage se voit. Sur l'accueil il surplombe un
  aplat sombre, et la même règle ne produit rien de visible.

- `src/18-selection.css`. Le bandeau de sélection était à
  `rgba(var(--accent), .8)`, donc 20 % de la page défilait au travers, et
  collé bord à bord alors que tout le reste du thème flotte. Il reprend la
  surface des autres éléments flottants — fond très sombre et flou
  d'arrière-plan, comme `.dialog` et `.toast` — et l'accent y redevient un
  liseré.

  Les cartes ont demandé un détour. `.itemSelectionPanel` est posé sur
  **toutes** les cartes dès l'entrée en mode sélection, pas seulement sur
  les cochées : le voile à l'accent d'Ultrachromic teintait donc la grille
  entière, et l'accent ne distinguait rien. Pire, rien dans le DOM ne marque
  une carte cochée — le module de sélection ne tient qu'un tableau d'ID en
  JavaScript et bascule `input.checked`, sans jamais poser de classe. D'où
  un découpage en deux étages : un voile neutre et une case bien visible,
  que tout moteur sait rendre ; puis l'anneau d'accent sur la carte cochée,
  sous `@supports selector(:has(*))`, puisqu'il faut remonter du champ à son
  ancêtre.

- `--btn-hover-bg` dans `src/01-reglages.css`, `--tv-card-ring` et
  `--tv-card-zoom` dans `src/16-tv-focus.css`.

### Supprimé

- `.mainDetailButtons .detailButton { align-self: center !important }` dans
  `src/03-page-item.css`. Règle morte : Jellyfin pose déjà
  `align-items: center` sur `.mainDetailButtons`, et rien ne déclare
  `align-self` sur ces boutons — elle réaffirmait la valeur calculée.
- Deux des trois sélecteurs d'annulation de `src/12-carte-zone.css`.
  `.card-hoverable` est porté par `.card` lui-même et `.cardBox` en est un
  enfant : les trois pèsent 0-3-0 et désignent le même jeu d'éléments. Celui
  du dessus suffit, les deux autres ne faisaient que nommer les règles
  visées — ce que le commentaire fait déjà.

  Vérifié mécaniquement avant de couper : toutes les classes visées par
  `src/*.css` existent encore dans le client servi, et les paires
  (sélecteur, propriété) déclarées plusieurs fois sont par ailleurs toutes
  des surcharges légitimes d'Ultrachromic.

## [1.1.1] — 2026-08-12 — Jellyfin 10.11.x

### Corrigé

- Une barre de défilement horizontale apparaissait en bas de l'accueil, alors
  qu'aucun contenu ne débordait réellement de la page. `src/15-barre-defilement.css`
  referme l'axe sur `#indexPage` et ses trois pages sœurs.

  L'origine est indirecte : `header_transparent-dashboard.css` pose
  `overflow-y: scroll` sur ces pages pour qu'elles défilent sous l'en-tête
  transparent, et la spec CSS impose alors que l'axe horizontal, resté à
  `visible`, se calcule en `auto`. Le conteneur de page devenait défilable
  latéralement pour un dépassement d'un pixel. Jellyfin, lui, ne pose aucun
  `overflow` sur ses conteneurs de page. Les rangées de cartes gardent leur
  propre défileur `.scrollX` : on continue de défiler sur la ligne.

## [1.1.0] — 2026-08-12 — Jellyfin 10.11.x

### Supprimé

- `smallercast.css` n'est plus chargé : ses 18 media queries rapetissaient et
  carraient les vignettes du casting. Les vignettes portrait de Jellyfin sont
  rétablies.

### Ajouté

- `src/vendor.exclude`, seul moyen de retirer un module du preset sans
  modifier l'amont — ce qui rendrait `update-vendor.sh` conflictuel à chaque
  resynchronisation. `build.py` refuse de construire si une entrée n'est
  jamais rencontrée, et le fichier construit porte la liste de ce qui a
  réellement été omis.
- `src/14-carte-fond.css`. `smallercast.css` portait aussi une règle
  `.cardPadder` globale, sans rapport avec le casting : elle neutralise le
  fond d'attente affiché sous chaque vignette avant chargement de l'image.
  Elle est reprise à l'identique, sinon ce fond réapparaissait sur toutes les
  grilles.

### Corrigé

- `build.py` annonçait des caractères sous le libellé « octets ». Les tirets
  cadratins en pèsent trois chacun en UTF-8, d'où un écart de 18 avec ce que
  renvoyait le CDN.
- Les quatre scripts étaient enregistrés en `100644`. Le dépôt vit sur un
  lecteur Windows, donc sous `core.filemode false`, où `chmod +x` n'influence
  plus ce que git enregistre : ils arrivaient non exécutables sur un clone
  Linux et la CI échouait en code 126.

## [1.0.0] — 2026-08-12 — Jellyfin 10.11.x

Première version publiée. Reprend le `ultrachromic.css` maintenu jusqu'ici
à la main, à l'octet près, réorganisé en modules.

### Ajouté

- Construction par `build.py` : Ultrachromic et les modules maison fusionnés
  en un seul `dist/theme.css`, servi par jsDelivr en une requête.
- Ultrachromic vendorisé et figé sur `fa158a2`. Le dépôt amont n'a ni tag ni
  release, et une URL sans version pointait donc sur le HEAD de `main` : le
  thème était bâti sur une cible mouvante.
- `update-vendor.sh` pour resynchroniser cette copie, sans commit, de façon
  à lire le diff avant de l'accepter.
- Vérifications bloquantes à la construction : accolades équilibrées, aucun
  `@import` après une règle, `display: !important` gardé par `:not(.hide)`.
- `apply-local.sh` et `apply-js.sh` paramétrables par `JELLYFIN_DIR`,
  `JELLYFIN_CONTAINER` et `JELLYFIN_URL`.

### Modifié

- Les `@import` distants sont remontés en tête du fichier construit, quelle
  que soit leur place dans les sources.
- Les URL d'images d'Ultrachromic, qui pointaient sur sa branche `main`,
  sont épinglées sur le commit vendorisé.
- `apply-local.sh` échappe le XML au lieu d'interdire `<` et `&` dans le CSS.
  Cette interdiction était devenue intenable : `jf_font.css` importe Google
  Fonts avec un `&` dans son URL. Le déséchappement est vérifié par relecture.

### Corrigé

- Trois à quatre niveaux d'`@import` en cascade à l'exécution, cause du flash
  d'interface non stylée au premier chargement et de l'arrivée tardive de
  `--accent`.

[1.1.1]: https://github.com/matqueme/jellyfin-theme/releases/tag/v1.1.1
[1.1.0]: https://github.com/matqueme/jellyfin-theme/releases/tag/v1.1.0
[1.0.0]: https://github.com/matqueme/jellyfin-theme/releases/tag/v1.0.0
