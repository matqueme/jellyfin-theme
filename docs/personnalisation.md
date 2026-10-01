# Personnalisation

Tout est dans [`../src/01-tokens.css`](../src/01-tokens.css). Les modules ne posent
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
l'`@import` de [`../src/00-imports.css`](../src/00-imports.css), et `Phosphor-Bold`
par `Phosphor` dans [`../src/90-icones.css`](../src/90-icones.css). Les points de
code sont identiques entre les deux graisses. Pour les icônes MUI, remplacer
`bold` par `regular` dans l'URL `CORE` de
[`../tools/icones-mui.py`](../tools/icones-mui.py) et le relancer.
