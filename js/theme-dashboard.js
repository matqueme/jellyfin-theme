/* theme-dashboard : applique le theme aux pages d'administration.
 *
 * En 12, le client n'injecte le CSS de branding (Tableau de bord ->
 * General -> CSS personnalise) que dans l'application utilisateur : le
 * composant qui pose la balise <style> n'est pas monte dans le layout du
 * dashboard. Ce script comble ce trou en chargeant la meme feuille, servie
 * par le serveur sur /Branding/Css, tant qu'une page #/dashboard est
 * affichee, et la retire en sortant.
 *
 * Aucune copie du theme ici : le script ne fait que pointer vers ce que le
 * serveur sert deja, donc une mise a jour du CSS de branding suffit.
 *
 * A installer par JavaScript Injector :  ./apply-js.sh js/theme-dashboard.js
 */
(function () {
    'use strict';

    var ID = 'theme-dashboard-css';

    function urlFeuille() {
        // ApiClient connait l'adresse du serveur, y compris derriere un
        // reverse proxy avec un chemin de base. A defaut, on remonte de
        // /web/ vers la racine du serveur.
        if (window.ApiClient && typeof window.ApiClient.getUrl === 'function') {
            return window.ApiClient.getUrl('Branding/Css');
        }
        return location.pathname.replace(/\/web\/.*$/, '/') + 'Branding/Css';
    }

    function surDashboard() {
        return /^#\/dashboard/.test(location.hash);
    }

    function appliquer() {
        var lien = document.getElementById(ID);
        if (surDashboard()) {
            if (!lien) {
                lien = document.createElement('link');
                lien.id = ID;
                lien.rel = 'stylesheet';
                lien.href = urlFeuille();
                // En dernier dans <body> : apres les feuilles du client et
                // apres celle de MUI, inseree dans <head> a l'execution.
                document.body.appendChild(lien);
            }
        } else if (lien) {
            lien.remove();
        }
    }

    window.addEventListener('hashchange', appliquer);
    window.addEventListener('popstate', appliquer);
    if (document.body) {
        appliquer();
    } else {
        document.addEventListener('DOMContentLoaded', appliquer);
    }
})();
