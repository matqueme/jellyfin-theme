# Thème Jellyfin

[English](README.md) · **Français**

Thème sombre pour Jellyfin 12, layout **Modern**. Surfaces neutres, blanc
comme couleur d'action, verre flouté, icônes [Phosphor](https://phosphoricons.com),
police Plus Jakarta Sans. Il couvre toute l'application : navigation, page
d'item, connexion, préférences, dialogues et menus, lecteur, layout TV, et le
tableau de bord d'administration.

Un seul fichier CSS, une seule ligne à coller : `dist/theme.css`.

## Aperçu

### Accueil

Les rangées, l'en-tête en verre, des cartes qui se soulèvent au survol.

![Accueil](docs/images/accueil.webp)

### Page d'un film

Hero net, boutons ronds, fiche lisible.

![Page d'un film](docs/images/page-item.webp)

### Bibliothèque

Cartes, pastilles « vu », barre de progression, index alphabétique.

![Bibliothèque](docs/images/bibliotheque.webp)

### Menus, filtres, connexion et préférences

Un seul dessin pour les anciens composants du client et pour ceux de MUI.

![Menu, filtres, connexion et préférences](docs/images/composants.webp)

### Mobile et TV

![Page d'un film sur mobile, accueil en layout TV](docs/images/mobile-tv.webp)

<sub>Captures prises sur un serveur Jellyfin 12.1 de test. Affiches et visuels : © leurs ayants droit, via TMDb.</sub>

## Installation

Tableau de bord → Général → **CSS personnalisé**, une seule ligne :

```css
@import url('https://cdn.jsdelivr.net/gh/matqueme/jellyfin-theme@v3.1.2/dist/theme.css');
```

Puis `Ctrl+F5` sur le client. L'`@import` doit rester la première chose du
champ : un `@import` placé après une règle est ignoré par le navigateur.

Pour le fond d'affiche flouté derrière les pages (comme sur les captures),
activer **Fonds d'écran** dans les préférences d'affichage de chaque utilisateur.

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
[Développement](docs/developpement.md). Seules les polices (Plus Jakarta Sans,
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
| `v3.0.0` à `v3.1.1` | 12.x, layout Modern | aucune |
| `v2.0.0` | 12.x | [Ultrachromic `1398af2`](https://github.com/CTalvio/Ultrachromic/tree/1398af21b8fe120a972bd00942ad60a76a932647) |
| `v1.3.0` | 10.11.x | [Ultrachromic `fa158a2`](https://github.com/CTalvio/Ultrachromic/tree/fa158a241cb24298c9996af3cf6460ae2f9d522f) |

Le thème suit son propre semver ; la version de Jellyfin visée est une donnée
de compatibilité, portée par ce tableau et par le titre de chaque release.
Chaque version reste disponible par son tag : pour Jellyfin 10.11, importer
`@v1.3.0` à la place de la version courante dans l'URL d'installation.

Le layout Legacy n'est plus visé depuis la v3. Il reste utilisable, mais son
en-tête et son tiroir ne sont pas habillés.

## Personnaliser

Toutes les valeurs (fonds, texte, rayons, verre, survol des cartes, taille des
icônes, libellé du bouton Lecture…) sont des tokens, définis à un seul endroit :
[`src/01-tokens.css`](src/01-tokens.css). Voir
[docs/personnalisation.md](docs/personnalisation.md) pour la liste.

## Contribuer

Structure des modules, build, publication d'une version et pièges rencontrés :
[docs/developpement.md](docs/developpement.md).

## Crédits

- [Phosphor Icons](https://phosphoricons.com) : licence MIT.
- Police [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) : SIL OFL 1.1.
- Les versions 1.x et 2.x reposaient sur [Ultrachromic](https://github.com/CTalvio/Ultrachromic),
  de CTalvio (MIT). La v3 n'en contient plus rien.

Code de ce dépôt sous licence [MIT](LICENSE).
