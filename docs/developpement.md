# Développement

[English](development.md) · **Français**

Guide pour contribuer ou modifier le thème. Pour l'utiliser seulement, le [README](../README.fr.md) suffit.

## Structure

```
src/
  00-imports.css        polices distantes, les seuls @import du fichier construit
  01-tokens.css         toutes les valeurs du thème
  02-palette-jf.css     tokens branchés sur les variables --jf-* du client et de MUI
  10-base.css           fond, police, texte, liens, défilement, focus
  20-boutons.css        principal, secondaire, discret, destructif, icônes, groupes
  21-champs.css         champs de saisie et listes déroulantes
  22-cases.css          cases à cocher, boutons radio, interrupteurs, curseurs
  23-surfaces.css       menus, dialogues, feuilles d'actions, infobulles, alertes
  24-listes.css         listes, tableaux, cartes MUI, pagination, chargement
  25-onglets-puces.css  onglets, puces, badges
  30-entete-tiroir.css  en-tête MUI, navigation des bibliothèques, tiroir
  40-cartes.css         affiches : survol, indicateurs, progression, sélection
  41-rangees.css        titres de section, rangées, sélecteur alphabétique
  50-page-item.css      page d'un film, d'une série, d'une saison
  51-connexion.css      page de connexion
  60-lecteur.css        OSD, barres de lecture, lecture en cours, « À suivre »
  80-tv.css             navigation à la télécommande
  90-icones.css         icônes Material (police) remappées sur Phosphor
  91-icones-mui.css     icônes SVG de MUI redessinées en Phosphor (généré)
  95-plugins.css        ce qu'ajoutent les plugins, mis au diapason
tools/icones-mui.py     génère 91-icones-mui.css à partir de sa table
js/                     comportements non réalisables en CSS
dist/theme.css          fichier construit et commité : c'est lui que sert le CDN
```

**L'ordre des modules est significatif.** Les préfixes numériques donnent
l'ordre de concaténation, donc la cascade : les tokens d'abord, les
composants génériques ensuite, puis les pages, qui peuvent les spécialiser.

### Deux familles de composants

La 12 mélange deux générations de composants, et le thème les aligne l'une
sur l'autre, module par module :

- les **anciens** (`.emby-button`, `.emby-input`, `.emby-select`,
  `.actionSheet`, `.listItem`…), sur les pages que la 12 rend encore avec ses
  contrôleurs d'avant, **y compris en Modern** : page d'item, connexion,
  listes, une partie des préférences ;
- les **MUI** : en-tête, tiroir, barres d'outils de bibliothèque, préférences
  d'affichage, tableau de bord.

Deux leviers, dans cet ordre :

1. les **variables `--jf-*`** (`02-palette-jf.css`). Le client construit son
   thème MUI en variables CSS, et son thème de base colore aussi les anciens
   composants à partir des mêmes variables. Les poser habille une bonne part
   de l'application d'un coup ;
2. les **classes de composant** : `.emby-*` d'un côté, `.MuiButton-root`,
   `.MuiFilledInput-root`, `.Mui-selected`… de l'autre. Elles font partie de
   l'API publique de MUI. Ne jamais viser les classes `css-xxxxxx`
   qu'Emotion génère à côté : ce sont des hachages recalculés à chaque
   version.

`dist/theme.css` est un fichier construit : ne jamais l'éditer, il est
réécrit à chaque build. jsDelivr sert depuis l'arbre git, d'où sa présence
dans les commits.

## Développement

```bash
./build.py
```

Concatène `src/` dans `dist/theme.css`, puis vérifie le résultat. Les
vérifications sont bloquantes : accolades équilibrées, aucun `@import` après
une règle, et tout `display` en `!important` gardé par `:not(.hide)`.

```bash
./apply-local.sh
```

Construit, écrit `dist/theme.css` dans le `branding.xml` du serveur, redémarre
le conteneur, puis vérifie que `/Branding/Css` renvoie **exactement** le
fichier attendu. Le chemin par défaut est `~/docker/jellyfin` ; sinon
`JELLYFIN_DIR=/srv/jellyfin ./apply-local.sh`.

```bash
./apply-js.sh js/*.js
```

Injecte les scripts dans la configuration du plugin JavaScript Injector :

- `theme-dashboard.js` : applique le thème au tableau de bord (voir
  [Installation](../README.fr.md#tableau-de-bord)) ;
- `replace-sync-button.js` : remplace le bouton SyncPlay de l'en-tête par une
  entrée dans le menu des préférences.

> Le plugin patche l'`index.html` servi par le serveur. L'app Tizen embarque
> sa propre copie du client web et ne le reçoit jamais : seul `/Branding/Css`
> l'atteint. Tout ce qui concerne la TV est donc fait en CSS.

### Sur un lecteur Windows monté dans WSL

Le dépôt réclame `core.filemode false` : `drvfs` remonte tous les fichiers en
777, et sans ce réglage git verrait des changements de permissions partout.
Corollaire : `chmod +x` n'a plus aucun effet sur ce que git enregistre. Pour
tout nouveau script :

```bash
git update-index --chmod=+x mon-script.sh
```

## Publier une version

Le tag et la release sont créés par GitHub Actions à partir du fichier
`VERSION`. Il n'y a rien à taguer à la main :

1. Éditer `VERSION` et ajouter la section correspondante dans `CHANGELOG.md`.
2. `./build.py` : l'en-tête de `dist/theme.css` porte le nouveau numéro.
3. Commiter, pousser sur `main`.

Le workflow `publier` vérifie le build, refuse une version sans notes dans le
`CHANGELOG`, crée le tag `vX.Y.Z` puis la release dont les notes sont cette
section. Il ne fait rien si le tag existe déjà.

Les URL jsDelivr taguées sont **immuables et mises en cache définitivement** :
pas de purge à faire, et un retour arrière consiste à remettre l'ancien tag.
Pour suivre `main` malgré tout, purger après chaque push :

```bash
curl -s https://purge.jsdelivr.net/gh/matqueme/jellyfin-theme@main/dist/theme.css
```

## Pièges

Écrits après les avoir rencontrés. Chacun se manifeste en silence, sans erreur
console.

**Le tableau de bord ne reçoit pas le CSS de branding.** Voir
[Installation](../README.fr.md#tableau-de-bord). Sans `theme-dashboard.js`, l'administration
reste sur le thème par défaut, bleu Jellyfin compris.

**Les variables `--jf-*` se posent sur `:root[data-theme]`, pas sur `:root`.**
MUI les déclare sur `:root, [data-theme="dark"]` et insère sa feuille à
l'exécution, après la nôtre : à spécificité égale, les siennes gagnent.
`:root[data-theme]` pèse 0-2-0 et passe devant, quel que soit le thème choisi
dans les préférences.

**MUI compile sa police en dur.** Les variables `--jf-font-*` existent mais
les composants ne les lisent pas : la police est reposée composant par
composant dans `10-base.css`.

**Tout `display` en `!important` doit être gardé par `:not(.hide)`.** Jellyfin
masque ses pages avec `.hide { display: none !important }`. Un sélecteur d'ID
l'emporte sur une classe à `!important` égal : sans ce garde-fou, la page de
connexion restait affichée par-dessus l'accueil. `build.py` refuse de
construire sans lui.

**Les liens de la fiche sont des boutons.** Étiquettes, liens externes,
réalisateur : ce sont des `a.button-link.emby-button`. Toute règle posée sur
`.emby-button` les atteint ; `50-page-item.css` les remet à plat.

**Les icônes MUI se reconnaissent à leur `data-testid`.** MUI rend ses
icônes en SVG, avec `data-testid="CastIcon"`, conservé en production. C'est
la seule accroche qui ne dépende ni de la langue (`aria-label`) ni de l'état
du composant : le bouton Diffusion devient un bouton à libellé quand une
diffusion est en cours. `91-icones-mui.css` masque les tracés du SVG et le
peint en `currentColor` à travers un masque Phosphor : taille et couleur
restent celles de MUI. Une icône absente de la table de
`tools/icones-mui.py` garde son dessin Material.

**Une icône en ligature ne se remappe pas.** `90-icones.css` agit sur la
classe (`.material-icons.play_arrow`). Une icône écrite en ligature, dont le
nom est le texte de la balise (`<span class="material-icons">key</span>`,
courant dans les plugins), reste en Material : aucun sélecteur ne porte sur
le texte d'un élément.

**Le layout se choisit sur le user-agent.** En « Mode d'affichage : Auto »,
un navigateur de bureau réduit à 390 px reste en `layout-desktop`. Pour
tester le rendu téléphone, il faut un user-agent mobile, pas seulement une
fenêtre étroite.

**La forme courte `background` remet `background-image` à `none`.** Le bouton
de profil de l'en-tête, dont l'avatar est un `background-image` posé en
ligne, perdait son image au survol. Écrire `background-color` dès qu'on ne
veut que la couleur.

**La TV n'est pas un layout, c'est aussi une détection de lenteur.**
`cardBuilder` distingue `.show-focus` de `.show-animation` par
`!browser.slow && !browser.edge`, et Tizen est classé « slow ». Vérifier
laquelle des deux classes est posée avant de surcharger un état de focus.

**Rien ne marque une carte sélectionnée dans le DOM.** Le seul signal est
`input.chkItemSelect:checked`, plus bas dans l'arbre que ce qu'on veut
peindre : donc `:has()`, sous `@supports selector(:has(*))` pour les
navigateurs de TV antérieurs à Chromium 105.

**Les `<` et `&` sont permis.** Le CSS est stocké comme texte dans
`branding.xml` ; `apply-local.sh` échappe et vérifie le déséchappement par
relecture.
