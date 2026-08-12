(function () {
    'use strict';

    /* =========================================================================
       Onglets "Accueil / Favoris" dans la page, sur telephone.

       Jellyfin place ces onglets dans .skinHeader, qui est en position: fixed.
       Aucune regle CSS ne peut les rattacher a la zone qui defile : il faut
       agir sur le DOM.

       On CLONE la rangee au lieu de deplacer l'originale. Deplacer le noeud
       serait plus simple, mais Jellyfin detruit l'element de page a chaque
       navigation : les onglets partiraient avec, et l'en-tete les perdrait
       jusqu'au rechargement. Avec un clone, le pire qui puisse arriver est
       une rangee en trop, et l'originale reste intacte.

       Les clics sont renvoyes sur les vrais boutons, donc toute la logique de
       navigation de Jellyfin reste la sienne.

       Le CSS associe est dans ultrachromic.css, sous "Onglets deplaces dans
       la page". Il ne s'active que si ce script pose body.tabs-in-page.
       ========================================================================= */

    var MAX_WIDTH  = 800;               /* doit rester aligne sur la media query 50em */
    var HOST_CLASS = 'pageTabsHost';
    var BODY_CLASS = 'tabs-in-page';

    function surAccueil() {
        return location.hash.indexOf('/home') !== -1;
    }

    function ecranEtroit() {
        return window.innerWidth <= MAX_WIDTH;
    }

    function vraiesRangees() {
        return document.querySelector('.skinHeader .headerTabs.sectionTabs');
    }

    function page() {
        return document.querySelector('#indexPage');
    }

    /* Signature de l'etat voulu. On ne touche au DOM que si elle change :
       sans ce garde-fou, nos propres ecritures relanceraient l'observateur
       en boucle. */
    function signature(boutons, actif) {
        var noms = [];
        for (var i = 0; i < boutons.length; i++) {
            noms.push((boutons[i].textContent || '').trim());
        }
        return noms.join('|') + '#' + actif;
    }


    var ECART = 16;                     /* espace entre le titre et la premiere pilule */

    /* Largeur reellement PEINTE du logo de l'en-tete.
       Sur l'accueil, .pageTitle n'a pas de texte : c'est une boite de
       13.2em portant l'image en background-size: contain, calee a gauche.
       L'image n'en remplit donc pas toute la largeur, et le reste est du
       vide. Le cas est spectaculaire en affichage TV, ou Jellyfin remplace
       la banniere par la seule icone carree
       (.layout-tv .pageTitleWithDefaultLogo) : l'icone n'occupe plus qu'un
       cinquieme de la boite, et une rangee calee sur la boite laissait un
       grand trou apres le logo.
       Avec contain, l'image est mise a l'echelle jusqu'a toucher le premier
       bord : sa largeur peinte vaut donc la hauteur de la boite fois le
       rapport de l'image, plafonnee a la largeur de la boite. Le rapport
       demande de charger l'image, ce qui est asynchrone : on memorise le
       resultat par URL et on relance une mesure a l'arrivee. */
    var rapports = {};                  /* url -> rapport, ou null tant qu'on charge */

    function largeurLogo(el) {
        var fond = getComputedStyle(el).backgroundImage || '';
        var m = /url\(["']?(.*?)["']?\)/.exec(fond);
        if (!m) return null;

        var url = m[1];
        if (!(url in rapports)) {
            rapports[url] = null;       /* pose avant le chargement : une seule tentative */
            var img = new Image();
            img.onload = function () {
                if (img.naturalWidth && img.naturalHeight) {
                    rapports[url] = img.naturalWidth / img.naturalHeight;
                    planifier();
                }
            };
            img.src = url;
        }
        if (!rapports[url]) return null;

        var b = el.getBoundingClientRect();
        if (!b.width || !b.height) return null;
        return Math.min(b.width, b.height * rapports[url]);
    }

    /* Decalage horizontal de la rangee d'onglets dans l'en-tete.
       Une valeur fixe ne peut pas convenir : .headerLeft contient le logo
       sur l'accueil mais un titre de page sur une bibliotheque ("Films"
       s'affichait sous les onglets), et les boutons qui le precedent
       varient - Jellyfin masque le hamburger en affichage TV. On mesure
       donc le bord droit reel de ce contenu et on pose la rangee apres. */
    function calerOnglets() {
        var entete = document.querySelector('.skinHeader');
        if (!entete) return;
        var racine = document.documentElement;

        var titre = document.querySelector('.headerLeft .pageTitle');
        var droite = null;

        /* Titre textuel : on vise le texte et non la boite, qui deborde. */
        if (titre) {
            for (var i = 0; i < titre.childNodes.length; i++) {
                var n = titre.childNodes[i];
                if (n.nodeType === 3 && n.textContent.trim()) {
                    var rg = document.createRange();
                    rg.selectNodeContents(n);
                    var b = rg.getBoundingClientRect();
                    if (b.width) { droite = b.right; break; }
                }
            }
        }

        /* Sinon logo : bord gauche de la boite plus la largeur peinte. */
        if (droite === null && titre) {
            var l = largeurLogo(titre);
            if (l !== null) droite = titre.getBoundingClientRect().left + l;
        }

        /* Ni l'un ni l'autre - image pas encore chargee, en-tete pas encore
           rendu : on laisse le repli du CSS. */
        if (droite === null) {
            if (racine.style.getPropertyValue('--tabs-left')) {
                racine.style.removeProperty('--tabs-left');
            }
            return;
        }

        var v = Math.round(droite - entete.getBoundingClientRect().left + ECART) + 'px';
        if (racine.style.getPropertyValue('--tabs-left') !== v) {
            racine.style.setProperty('--tabs-left', v);
        }
    }

    /* Bord gauche du TEXTE d'un element, et non de sa boite. Un titre de
       section a son propre padding : viser la boite laissait la pilule 13px
       trop a gauche. On passe par un Range sur le premier noeud texte. */
    function bordTexte(el) {
        if (!el) return null;
        for (var i = 0; i < el.childNodes.length; i++) {
            var n = el.childNodes[i];
            if (n.nodeType === 3 && n.textContent.trim()) {
                var r = document.createRange();
                r.selectNodeContents(n);
                var b = r.getBoundingClientRect();
                if (b.width) return b.left;
            }
        }
        var r2 = document.createRange();
        r2.selectNodeContents(el);
        var b2 = r2.getBoundingClientRect();
        return b2.width ? b2.left : el.getBoundingClientRect().left;
    }

    /* Hauteur reelle de l'en-tete, et bord gauche des titres de section :
       l'hote doit s'aligner sur "Mes medias", pas sur le bord de l'ecran. */
    function mesurer(p, hote) {
        var racine = document.documentElement;

        var entete = document.querySelector('.skinHeader');
        if (entete) {
            racine.style.setProperty('--header-h',
                Math.round(entete.getBoundingClientRect().height) + 'px');
        }

        var titre = p.querySelector('.homeSectionsContainer .sectionTitle-cards')
                 || p.querySelector('.homeSectionsContainer .sectionTitle');
        if (!titre) return;

        /* On aligne le BORD GAUCHE de la pilule sur le texte du titre de
           section. Son propre padding decale donc son libelle vers la
           droite, ce qui est le rendu voulu : la pilule est un fond qui
           entoure le texte, comme sur la barre de Netflix.
           On vise le texte du titre et non sa boite : celle-ci commence une
           quinzaine de pixels plus a gauche a cause de son padding. */
        var xTitre = bordTexte(titre);
        if (xTitre === null) return;

        var dx = Math.round(xTitre - p.getBoundingClientRect().left);
        if (dx < 0) dx = 0;
        if (dx < 200) racine.style.setProperty('--tabs-host-left', dx + 'px');
    }

    var derniere = null;

    function appliquer() {
        /* Vaut pour toutes les pages, pas seulement l'accueil. */
        calerOnglets();

        var p = page();
        var src = vraiesRangees();
        var hote = p ? p.querySelector('.' + HOST_CLASS) : null;

        if (!surAccueil() || !ecranEtroit() || !p || !src) {
            if (hote && hote.parentNode) hote.parentNode.removeChild(hote);
            document.body.classList.remove(BODY_CLASS);
            derniere = null;
            return;
        }

        var boutons = src.querySelectorAll('.emby-tab-button');
        if (!boutons.length) return;

        var actif = -1;
        for (var i = 0; i < boutons.length; i++) {
            if (boutons[i].classList.contains('emby-tab-button-active')) actif = i;
        }

        if (!hote) {
            hote = document.createElement('div');
            hote.className = HOST_CLASS;
            p.insertBefore(hote, p.firstChild);
        }
        document.body.classList.add(BODY_CLASS);

        var sig = signature(boutons, actif);
        if (sig !== derniere) {
            derniere = sig;
            hote.innerHTML = '';
            for (var j = 0; j < boutons.length; j++) {
                (function (source, index) {
                    var b = document.createElement('button');
                    b.type = 'button';
                    b.className = 'pageTab' + (index === actif ? ' pageTab-active' : '');
                    b.textContent = (source.textContent || '').trim();
                    b.addEventListener('click', function () { source.click(); });
                    hote.appendChild(b);
                })(boutons[j], j);
            }
        }

        /* Toujours mesurer, meme quand les onglets n'ont pas change : la
           hauteur de l'en-tete et le bord des sections bougent au
           redimensionnement. Et apres construction, pour disposer de la
           pilule et lire son padding reel. */
        mesurer(p, hote);
    }

    /* Une seule execution par frame, quel que soit le nombre de mutations. */
    var enAttente = false;
    function planifier() {
        if (enAttente) return;
        enAttente = true;
        requestAnimationFrame(function () { enAttente = false; appliquer(); });
    }

    new MutationObserver(planifier).observe(document.body, {
        childList: true, subtree: true, attributes: true,
        attributeFilter: ['class']
    });
    window.addEventListener('hashchange', planifier);
    window.addEventListener('resize', planifier);
    planifier();
})();
