# Thème Jellyfin

Thème sombre pour Jellyfin 10.11, construit sur
[Ultrachromic](https://github.com/CTalvio/Ultrachromic) (preset `kaleidochromic`)
avec les icônes [Phosphor](https://phosphoricons.com), et une soixantaine de
surcharges maison : page d'item, page de connexion, onglets d'en-tête,
barres de progression des cartes, corrections TV et téléphone.

Livré comme **un seul fichier** : `dist/theme.css`. Ultrachromic est vendorisé
et fusionné à la construction, il n'y a donc aucune cascade d'`@import` à
l'exécution ni aucune dépendance à un dépôt tiers qui bouge.

<img width="2549" height="1314" alt="image" src="https://github.com/user-attachments/assets/d4ca6f8c-034c-45df-bc63-41bbb013c3ff" />

## Installation

Tableau de bord → Général → **CSS personnalisé**, une seule ligne :

```css
@import url('https://cdn.jsdelivr.net/gh/matqueme/jellyfin-theme@v1.1.0/dist/theme.css');
```

Puis `Ctrl+F5` sur le client.

L'`@import` doit rester la première chose du champ : un `@import` placé après
une règle est ignoré par le navigateur.

> Le CSS de branding s'applique au client web et aux clients qui l'embarquent
> (navigateur, application de bureau, Android TV en mode web). Les clients
> natifs — Roku, l'app Android native — ne le lisent pas.

### Sans dépendance réseau

Si les clients doivent fonctionner sans accès à Internet, ou si le CDN est
indésirable, `apply-local.sh` écrit le fichier directement dans le
`branding.xml` du serveur. Voir [Développement](#développement).

## Compatibilité

| Thème | Jellyfin | Ultrachromic |
|---|---|---|
| `v1.1.0` | 10.11.x | [`fa158a2`](https://github.com/CTalvio/Ultrachromic/tree/fa158a241cb24298c9996af3cf6460ae2f9d522f) |
| `v1.0.0` | 10.11.x | [`fa158a2`](https://github.com/CTalvio/Ultrachromic/tree/fa158a241cb24298c9996af3cf6460ae2f9d522f) |

Le thème suit son propre semver ; la version de Jellyfin visée est une donnée
de compatibilité, pas un numéro de version. Elle est portée par ce tableau et
par le titre de chaque release.

Le thème s'accroche aux classes internes du client web, que Jellyfin peut
renommer d'une version mineure à l'autre. Une montée de Jellyfin en version
mineure appelle donc une relecture — et, si le rendu casse, une branche
`jellyfin-10.11` pour figer l'existant pendant que `main` part sur la suite.

## Réglages

Les valeurs prévues pour être retouchées, avec leur emplacement :

| Variable | Fichier | Effet |
|---|---|---|
| `--icon-scale` | [`src/01-reglages.css`](src/01-reglages.css) | Taille des icônes Phosphor, qui remplissent plus leur cadre que Material |
| `--play-label` | [`src/01-reglages.css`](src/01-reglages.css) | Libellé du bouton Lecture. Garder les guillemets : c'est une valeur de `content` |
| `--play-label-size` | [`src/01-reglages.css`](src/01-reglages.css) | Taille de ce libellé |
| `--tabs-left` | [`src/05-onglets.css`](src/05-onglets.css) | Décalage des onglets d'en-tête. Repli seulement : le script les mesure et pose sa propre valeur |
| `--card-bar-height` | [`src/10-carte-barre.css`](src/10-carte-barre.css) | Épaisseur de la barre de progression des cartes |
| `--card-bar-gap` | [`src/10-carte-barre.css`](src/10-carte-barre.css) | Détachement du bord bas — c'est ce qui fait l'effet flottant |
| `--card-bar-inset` | [`src/10-carte-barre.css`](src/10-carte-barre.css) | Retrait latéral de cette barre |

Pour repasser les icônes en trait fin : remplacer `bold` par `regular` dans
l'`@import` de [`src/00-imports.css`](src/00-imports.css), et `Phosphor-Bold`
par `Phosphor` dans [`src/07-icones.css`](src/07-icones.css). Les points de
code sont identiques entre les deux graisses.

## Structure

```
src/
  00-imports.css        polices distantes — les seuls @import qui survivent au build
  01-reglages.css       variables de réglage
  02-cartes-survol.css  bouton play des cartes
  03-page-item.css      page d'un film : bouton Lecture en pilule
  04-connexion.css      page de connexion
  05-onglets.css        onglets Accueil / Favoris, en-tête téléphone
  06-tv.css             corrections propres au layout TV
  07-icones.css         100 icônes Material remappées sur Phosphor
  08-indicateurs.css    indicateur « vu » détaché du coin
  09-lecteur.css        marqueurs de chapitres, barres arrondies
  10-carte-barre.css    barre de progression des cartes
  11-carte-boutons.css  boutons d'overlay
  12-carte-zone.css     zone de survol calée sur l'affiche
  13-carte-curseur.css  curseur main calé sur la carte visible
  14-carte-fond.css     fond d'attente des affiches
  vendor/ultrachromic/  Ultrachromic figé sur un commit (32 Ko)
  vendor.list           modules Ultrachromic chargés après le preset
  vendor.exclude        modules du preset volontairement écartés
js/                     comportements non réalisables en CSS
dist/theme.css          fichier construit — commité, c'est lui que sert le CDN
```

**L'ordre des modules est significatif.** Les préfixes numériques donnent
l'ordre de concaténation, et donc la cascade. Plusieurs modules s'appuient
sur le fait qu'ils passent après tel autre — renuméroter change le rendu.

### Écarter un module d'Ultrachromic

Le preset importe sa propre liste de modules, que `build.py` suit telle
quelle. Pour en retirer un, l'inscrire dans
[`src/vendor.exclude`](src/vendor.exclude) plutôt que de toucher à
`src/vendor/` — une modification là-bas rendrait `update-vendor.sh`
conflictuel à chaque resynchronisation.

`build.py` refuse de construire si une entrée n'est jamais rencontrée : une
exclusion qui ne s'applique à rien serait indiscernable d'une exclusion qui
marche. Le fichier construit porte en en-tête la liste de ce qui a réellement
été omis.

Vérifier ce que le module faisait **d'autre** avant de l'écarter : plusieurs
modules d'Ultrachromic mêlent des règles sans rapport avec leur nom.
`smallercast.css` portait ainsi une règle `.cardPadder` globale, qu'il a fallu
reprendre dans `14-carte-fond.css`.

`dist/theme.css` est un fichier construit : ne jamais l'éditer, il est
réécrit à chaque build. jsDelivr sert depuis l'arbre git, d'où sa présence
dans les commits.

## Développement

```bash
./build.py
```

Fusionne tout dans `dist/theme.css`, puis vérifie le résultat. Les
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

Injecte les scripts dans la configuration du plugin JavaScript Injector.
Deux comportements ne sont pas réalisables en CSS :

- `onglets-dans-la-page.js` — sur téléphone, déplace les onglets dans la page
  pour qu'ils défilent avec le contenu. Le CSS ne peut pas reparenter un
  élément, et les onglets sont dans un en-tête `position: fixed`. Il mesure
  aussi `--header-h` et `--tabs-host-left`, que `05-onglets.css` consomme.
- `replace-sync-button.js` — remplace le bouton SyncPlay de l'en-tête par une
  entrée dans le menu des préférences.

Le CSS fonctionne sans eux : les règles concernées sont gardées par
`body.tabs-in-page`, que seul le script pose.

> Le plugin patche l'`index.html` servi par le serveur. L'app Tizen embarque
> sa propre copie du client web et ne le reçoit jamais — seul `/Branding/Css`
> l'atteint. D'où le calage des onglets en TV fait entièrement en CSS, dans
> `06-tv.css`.

### Sur un lecteur Windows monté dans WSL

Le dépôt réclame `core.filemode false` : `drvfs` remonte tous les fichiers en
777, et sans ce réglage git verrait des changements de permissions partout.
Corollaire : `chmod +x` n'a plus aucun effet sur ce que git enregistre, et un
script ajouté ici arrive en `100644` — donc non exécutable une fois cloné
sous Linux, ou sur un runner GitHub Actions. Pour tout nouveau script :

```bash
git update-index --chmod=+x mon-script.sh
```

`--chmod` écrit le mode directement dans l'index, sans consulter le système
de fichiers. C'est le seul moyen quand `core.filemode` vaut `false`.

```bash
./update-vendor.sh [sha]
```

Resynchronise `src/vendor/ultrachromic/`. Ne commite rien : le but est de
lire le diff avant d'accepter. Ultrachromic n'a **ni tag ni release**, donc
une URL sans version pointe sur le HEAD de `main` — vendoriser fige cette
cible mouvante, et ce script est le seul endroit où elle bouge.

## Publier une version

Le tag et la release sont créés par GitHub Actions à partir du fichier
`VERSION`. Il n'y a rien à taguer à la main :

1. Éditer `VERSION` (ex. `1.2.0`) et ajouter la section correspondante dans
   `CHANGELOG.md`.
2. `./build.py` — l'en-tête de `dist/theme.css` porte le nouveau numéro.
3. Commiter, pousser sur `main`.

Le workflow `publier` vérifie le build, refuse une version sans notes dans le
`CHANGELOG`, crée le tag `vX.Y.Z` puis la release dont les notes sont cette
section. Il ne fait rien si le tag existe déjà : pousser plusieurs fois est
sans effet.

`VERSION` était déjà la source de vérité — `build.py` l'estampille dans le CSS
servi. Taguer à la main revenait à recopier ce numéro, donc à pouvoir
l'oublier, ou à publier une feuille qui s'annonce en `1.1.0` sous un tag
`v1.0.0`.

Le résumé d'exécution du workflow affiche la ligne d'`@import` à coller dans
le branding : c'est la seule étape qui reste manuelle, côté Jellyfin.

Les URL jsDelivr taguées sont **immuables et mises en cache définitivement** :
pas de purge à faire, et un retour arrière consiste à remettre l'ancien tag.
C'est la raison de préférer les tags à `@main`, dont le cache CDN tient de
12 heures à 7 jours — un push suivi de « rien ne change » est le symptôme
classique. Pour suivre `main` malgré tout, purger après chaque push :

```bash
curl -s https://purge.jsdelivr.net/gh/matqueme/jellyfin-theme@main/dist/theme.css
```

Le workflow GitHub Actions le fait automatiquement, et vérifie à chaque push
que `dist/` correspond bien à `src/`.

## Pièges

Écrits après les avoir rencontrés. Chacun se manifeste en silence, sans erreur
console.

**Tout `display` en `!important` doit être gardé par `:not(.hide)`.** Jellyfin
masque ses pages avec `.hide { display: none !important }`. Un sélecteur d'ID
l'emporte sur une classe à `!important` égal : sans ce garde-fou, la page de
connexion restait affichée par-dessus l'accueil. `build.py` refuse de
construire sans lui.

**Toujours écrire `var(--accent, 98, 121, 205)`.** `--accent` vient de
`type/colorful.css`. Sans repli, `rgba(var(--accent), .95)` est une valeur
invalide tant que la variable n'est pas définie, et la déclaration est
purement ignorée — bouton transparent au lieu de coloré. La fusion réduit
beaucoup ce risque, mais les replis restent la bonne pratique.

**Les variantes d'Ultrachromic ne s'empilent pas.** `indicator_corner` et
`indicator_floating`, `title_simple` et `title_banner-logo` sont des
alternatives. Le preset en charge déjà une ; ajouter l'autre par-dessus ne la
remplace pas, car la première pose des `!important` que la seconde ne reprend
pas. C'est tout l'objet de `08-indicateurs.css`.

**Les `<` et `&` ne sont plus interdits.** Le CSS est stocké comme texte dans
`branding.xml`, et une version antérieure de l'outillage les proscrivait pour
ne pas casser le XML. `apply-local.sh` échappe désormais correctement, et
vérifie le déséchappement par relecture. Les media queries de la forme
`@media (width < 50em)` sont donc utilisables.

## Crédits

- [Ultrachromic](https://github.com/CTalvio/Ultrachromic) — CTalvio, licence MIT.
  Vendorisé dans `src/vendor/`, voir [NOTICE](NOTICE).
- [Phosphor Icons](https://phosphoricons.com) — licence MIT.
- Police [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) — SIL OFL 1.1.

Code de ce dépôt sous licence [MIT](LICENSE).
