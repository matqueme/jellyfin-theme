(function () {
    'use strict';

    /* =============================== réglages =============================== */
    var MENU_ROUTE  = 'mypreferencesmenu';
    var ENTRY_CLASS = 'lnkSyncPlayCustom';
    var SHOW_STATUS = true;                       // sous-titre d'état sous "SyncPlay"
    var TXT = { fallback: 'SyncPlay', inGroup: 'Groupe actif', noGroup: 'Aucun groupe' };

    /* ==================== 1. bouton natif : invisible, pas absent ============ */
    /* La popup SyncPlay s'ancre sur le bouton : display:none => rect nul =>
       popup en 0,0. On le garde à 1px, et on le repositionne au clic.          */
    var css = document.createElement('style');
    css.textContent =
        '.headerSyncButton:not(.hide){' +
            'position:fixed !important;top:0 !important;left:0 !important;' +
            'width:1px !important;height:1px !important;' +
            'min-width:0 !important;min-height:0 !important;' +
            'padding:0 !important;margin:0 !important;border:0 !important;' +
            'opacity:0 !important;pointer-events:none !important;' +
            'overflow:hidden !important;z-index:-1 !important;}' +
        /* entrée de menu : aucune couleur en dur -> suit le thème actif */
        '.' + ENTRY_CLASS + '{display:block;margin:0;padding:0;' +
            'color:inherit !important;text-decoration:none !important;}' +
        '.' + ENTRY_CLASS + ' .listItemBodyText{color:inherit;}' +
        /* utilisé seulement si le clonage échoue */
        '.' + ENTRY_CLASS + '--fb .listItem{display:flex;align-items:center;padding:.65em 1em;}' +
        '.' + ENTRY_CLASS + '--fb .listItemIcon{margin-right:1em;}' +
        '.' + ENTRY_CLASS + '--fb:hover .listItem,' +
        '.' + ENTRY_CLASS + '--fb:focus .listItem{background:rgba(127,127,127,.18);}';
    document.head.appendChild(css);

    /* ============================ 2. helpers ================================ */
    function nativeBtn() {
        var b = document.querySelector('.headerSyncButton');
        return (b && !b.classList.contains('hide')) ? b : null;   // SyncPlayAccess = Aucun
    }

    // Ancre la popup sur l'entrée cliquée (inline !important > CSS !important)
    function anchorTo(btn, target) {
        var r = target.getBoundingClientRect(), s = btn.style;
        s.setProperty('top',    r.top + 'px', 'important');
        s.setProperty('left',   r.left + 'px', 'important');
        s.setProperty('width',  Math.max(r.width, 1) + 'px', 'important');
        s.setProperty('height', Math.max(r.height, 1) + 'px', 'important');
    }

    function buildEntry(model, btn) {
        var label = btn.getAttribute('title') || btn.getAttribute('aria-label') || TXT.fallback;
        var entry;

        if (model) {                       // clone d'une vraie entrée -> style identique
            entry = model.cloneNode(true);
            entry.removeAttribute('id');
            entry.className = entry.className
                .replace(/\blnk[A-Za-z0-9]*\b/g, ' ').replace(/\s+/g, ' ').trim();
        } else {                           // secours
            entry = document.createElement('a');
            entry.className = 'emby-button listItem-border ' + ENTRY_CLASS + '--fb';
            entry.innerHTML =
                '<div class="listItem">' +
                    '<span class="listItemIcon listItemIcon-transparent"></span>' +
                    '<div class="listItemBody"><div class="listItemBodyText"></div></div>' +
                '</div>';
        }

        entry.classList.add(ENTRY_CLASS);
        entry.setAttribute('href', '#');
        entry.setAttribute('role', 'button');
        entry.setAttribute('title', label);

        // Icône reprise du bouton natif : bonne glyphe quelle que soit la version
        var srcIcon = btn.querySelector('.material-icons') || btn.querySelector('span');
        var slot    = entry.querySelector('.listItemIcon');
        if (srcIcon && slot) {
            var icon = srcIcon.cloneNode(true);
            icon.removeAttribute('style');
            icon.classList.remove('syncPlayIconCircle');
            icon.classList.add('listItemIcon', 'listItemIcon-transparent');
            slot.parentNode.replaceChild(icon, slot);
        }

        // Libellé (+ nettoyage des lignes héritées du clone)
        var texts = entry.querySelectorAll('.listItemBodyText');
        if (texts[0]) texts[0].textContent = label;
        for (var i = texts.length - 1; i >= 1; i--) texts[i].parentNode.removeChild(texts[i]);

        if (SHOW_STATUS) {
            var body = entry.querySelector('.listItemBody');
            if (body) {
                var sub = document.createElement('div');
                sub.className = 'listItemBodyText secondary';
                sub.setAttribute('data-syncplay-status', '');
                body.appendChild(sub);
            }
        }

        entry.addEventListener('click', function (e) {
            e.preventDefault();
            var b = nativeBtn();
            if (!b) return;
            anchorTo(b, entry);
            b.click();
        });

        return entry;
    }

    function updateStatus() {
        if (!SHOW_STATUS) return;
        var slot = document.querySelector('.' + ENTRY_CLASS + ' [data-syncplay-status]');
        var b    = nativeBtn();
        if (!slot || !b) return;
        // Jellyfin ajoute syncPlayIconCircle quand on est dans un groupe
        var active = !!b.querySelector('.syncPlayIconCircle') ||
                     b.className.indexOf('syncPlayIconCircle') !== -1;
        slot.textContent = active ? TXT.inGroup : TXT.noGroup;
    }

    /* ============================= 3. injection ============================= */
    var watchingBtn = false;

    function inject() {
        var btn = nativeBtn();
        if (btn && !watchingBtn) {              // suivi de l'état du groupe
            watchingBtn = true;
            new MutationObserver(updateStatus)
                .observe(btn, { attributes: true, childList: true, subtree: true,
                                attributeFilter: ['class', 'title'] });
        }
        if (location.hash.indexOf(MENU_ROUTE) === -1) return;
        if (!btn) return;
        if (document.querySelector('.' + ENTRY_CLASS)) { updateStatus(); return; }

        var model = document.querySelector(
            '.lnkQuickConnectPreferences, .lnkDisplayPreferences, .lnkHomePreferences');
        if (!model) return;                     // page pas encore rendue

        model.parentNode.insertBefore(buildEntry(model, btn), model);
        updateStatus();
    }

    var queued = false;
    function schedule() {
        if (queued) return;
        queued = true;
        requestAnimationFrame(function () { queued = false; inject(); });
    }

    new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    window.addEventListener('hashchange', schedule);
    schedule();
})();
