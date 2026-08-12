# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Versionnage sémantique, indépendant de celui de Jellyfin — la compatibilité
est indiquée par le titre de chaque version.

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
