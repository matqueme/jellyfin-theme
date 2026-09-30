# Thème Jellyfin

Thème sombre pour Jellyfin 12, layout **Modern**. Surfaces neutres, blanc
comme couleur d'action, icônes [Phosphor](https://phosphoricons.com), police
Plus Jakarta Sans. Il couvre toute l'application : navigation, page d'item,
connexion, préférences, dialogues et menus, lecteur, layout TV, et le
tableau de bord d'administration.

Écrit de zéro depuis la v3 : plus de base tierce ni de règles qui en
corrigent d'autres. Les valeurs sont des **tokens** définis à un seul
endroit, et chaque famille de composants (bouton, champ, liste déroulante,
case à cocher, liste, menu, dialogue…) est dessinée une seule fois, avec les
mêmes valeurs pour les anciens composants du client et pour ceux de MUI.

Livré en **un seul fichier** : `dist/theme.css`.

<img width="2549" height="1314" alt="image" src="https://github.com/user-attachments/assets/d4ca6f8c-034c-45df-bc63-41bbb013c3ff" />

## Installation

Tableau de bord → Général → **CSS personnalisé**, une seule ligne :

```css
@import url('https://cdn.jsdelivr.net/gh/matqueme/jellyfin-theme@v3.1.2/dist/theme.css');
```

Puis `Ctrl+F5` sur le client. L'`@import` doit rester la première chose du
champ : un `@import` placé après une règle est ignoré par le navigateur.

### Tableau de bord

En 12, le client n'applique le CSS de branding **qu'à l'application
utilisateur** : le composant qui pose la balise `<style>` n'est pas monté
dans le layout du tableau de bord. Pour que l'administration suive le thème,
installer [`js/theme-dashboard.js`](js/theme-dashboard.js) avec le plugin
JavaScript Injector :

```bash
./apply-js.sh js/theme-dashboard.js
```

Le script ne contient pas le thème : sur les pages `#/dashboard`, il charge
la feuille que le serveur sert déjà sur `/Branding/Css`, et la retire en
sortant. Mettre à jour le CSS de branding suffit donc à mettre à jour le
tableau de bord.

### Sans dépendance réseau

Si les clients doivent fonctionner sans accès à Internet, `apply-local.sh`
écrit le fichier directement dans le `branding.xml` du serveur. Voir
[Développement](#développement). Seules les polices (Plus Jakarta Sans,
Phosphor) et les SVG Phosphor des icônes MUI restent chargés depuis un CDN.

> Le CSS de branding s'applique au client web et aux clients qui l'embarquent
> (navigateur, application de bureau, Android TV en mode web). Les clients
> natifs, comme Roku ou l'app Android native, ne le lisent pas.
>
> L'app Samsung (Tizen) lit bien le CSS de branding, mais elle embarque son
> propre client web, figé à sa compilation (10.11 pour l'app 1.1.0), en
> layout TV : ce n'est pas le client 12 du serveur. `src/80-tv.css` couvre
> ce cas : pas de verre flouté (trop lourd pour une TV), hero net sur la page
> d'item, en-tête et focus adaptés.

## Compatibilité

| Thème | Jellyfin | Base |
|---|---|---|
| `v3.1.2` | 12.x, layout Modern (+ app Samsung, client 10.11) | aucune |
| `v3.1.1` | 12.x, layout Modern | aucune |
| `v3.1.0` | 12.x, layout Modern | aucune |
| `v3.0.0` | 12.x, layout Modern | aucune |
| `v2.0.0` | 12.x | [Ultrachromic `1398af2`](https://github.com/CTalvio/Ultrachromic/tree/1398af21b8fe120a972bd00942ad60a76a932647) |
| `v1.3.0` | 10.11.x | [Ultrachromic `fa158a2`](https://github.com/CTalvio/Ultrachromic/tree/fa158a241cb24298c9996af3cf6460ae2f9d522f) |

Le thème suit son propre semver ; la version de Jellyfin visée est une donnée
de compatibilité, portée par ce tableau et par le titre de chaque release.
Chaque version reste disponible par son tag : pour Jellyfin 10.11, importer
`@v1.3.0` à la place de la version courante dans l'URL d'installation.

Le layout Legacy n'est plus visé depuis la v3. Il reste utilisable, mais son
en-tête et son tiroir ne sont pas habillés.

## Réglages

Tout est dans [`src/01-tokens.css`](src/01-tokens.css). Les modules ne posent
jamais une couleur, un rayon ou une durée en dur : retoucher le thème, c'est
retoucher ce fichier.

| Token | Rôle |
|---|---|
| `--bg`, `--bg-raised`, `--bg-overlay` | Fonds : page, panneaux posés sur la page, ce qui flotte (menus, dialogues) |
| `--veil-1` à `--veil-3` | Voiles blancs : champs, boutons secondaires, survols. Justes sur n'importe quel fond |
| `--line`, `--line-strong` | Filets d'un pixel |
| `--text`, `--text-2`, `--text-3` | Texte principal, secondaire, discret |
| `--primary`, `--on-primary` | Action principale : blanc, texte noir |
| `--danger`, `--success`, `--warning`, `--info` | Les seules couleurs franches, sémantiques |
| `--glass`, `--glass-strong`, `--glass-blur`, `--glass-edge` | Verre : en-tête, tiroir, barre de lecture (`--glass`) ; menus, dialogues (`--glass-strong`). Le flou sature ce qui passe dessous, l'arête porte un reflet |
| `--backdrop-dim` | Flou de la page derrière un dialogue ouvert |
| `--shadow-float`, `--shadow-lift`, `--glow-primary` | Ombres de ce qui flotte et d'une carte soulevée ; lueur du bouton principal au survol |
| `--hero-height`, `--hero-blur`, `--hero-veil` | Page d'item sur ordinateur : hauteur de l'image nette en haut, flou et voile du contenu qui passe dessus |
| `--card-lift`, `--card-zoom`, `--press` | Survol des cartes (montée, zoom de l'image) et bouton enfoncé. Neutralisés sous `prefers-reduced-motion` |
| `--r-xs` à `--r-lg`, `--r-pill` | Rayons : pastilles, champs, cartes, dialogues, boutons |
| `--ring` | Anneau de focus et de survol des cartes |
| `--icon-scale` | Taille des icônes Phosphor, qui remplissent plus leur cadre que Material |
| `--play-label` | Libellé du bouton Lecture. Garder les guillemets : c'est une valeur de `content` |

Les couleurs utilisées en transparence existent aussi en canaux
(`--primary-canal: 244 244 245`), la syntaxe qu'attend MUI pour ses
variables `*Channel`. Les deux doivent rester d'accord.

Pour repasser les icônes en trait fin : remplacer `bold` par `regular` dans
l'`@import` de [`src/00-imports.css`](src/00-imports.css), et `Phosphor-Bold`
par `Phosphor` dans [`src/90-icones.css`](src/90-icones.css). Les points de
code sont identiques entre les deux graisses. Pour les icônes MUI, remplacer
`bold` par `regular` dans l'URL `CORE` de
[`tools/icones-mui.py`](tools/icones-mui.py) et le relancer.

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
  [Installation](#tableau-de-bord)) ;
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
[Installation](#tableau-de-bord). Sans `theme-dashboard.js`, l'administration
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

## Crédits

- [Phosphor Icons](https://phosphoricons.com) : licence MIT.
- Police [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) : SIL OFL 1.1.
- Les versions 1.x et 2.x reposaient sur [Ultrachromic](https://github.com/CTalvio/Ultrachromic),
  de CTalvio (MIT). La v3 n'en contient plus rien.

Code de ce dépôt sous licence [MIT](LICENSE).
