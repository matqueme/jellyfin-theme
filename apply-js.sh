#!/usr/bin/env bash
#
# Injecte les scripts de js/ dans la configuration du plugin
# JavaScript Injector, puis redémarre Jellyfin.
#
# Chaque fichier js/<nom>.js devient une entrée nommée <nom>. Une entrée
# du même nom est remplacée ; les autres (écrites depuis le tableau de
# bord) sont laissées intactes.
#
#   ./apply-js.sh js/onglets-dans-la-page.js
#   JELLYFIN_DIR=/srv/jellyfin ./apply-js.sh js/*.js

set -euo pipefail
cd "$(dirname "$0")"

[ $# -ge 1 ] || { echo "usage: ./apply-js.sh js/<fichier>.js"; exit 1; }

JELLYFIN_DIR="${JELLYFIN_DIR:-$HOME/docker/jellyfin}" \
JELLYFIN_CONTAINER="${JELLYFIN_CONTAINER:-jellyfin}" \
JELLYFIN_URL="${JELLYFIN_URL:-http://localhost:8096}" \
python3 - "$@" <<'PY'
import os, subprocess, sys, time, urllib.request
import xml.etree.ElementTree as ET

XML = os.path.join(os.environ["JELLYFIN_DIR"], "config", "data", "plugins",
                   "configurations",
                   "Jellyfin.Plugin.JavaScriptInjector.xml")

tree = ET.parse(XML)
root = tree.getroot()
liste = root.find("CustomJavaScripts")

for chemin in sys.argv[1:]:
    nom = chemin.split("/")[-1].rsplit(".", 1)[0]
    code = open(chemin, encoding="utf-8").read()

    # Remplacer l'entrée existante du même nom, sinon en créer une.
    cible = None
    for e in liste.findall("CustomJavaScriptEntry"):
        if (e.findtext("Name") or "") == nom:
            cible = e
            break
    if cible is None:
        cible = ET.SubElement(liste, "CustomJavaScriptEntry")
        for balise, valeur in (("Name", nom), ("Script", ""),
                               ("Enabled", "true"), ("RequiresAuthentication", "false")):
            ET.SubElement(cible, balise).text = valeur
        print(f"nouvelle entree : {nom}")
    else:
        print(f"entree remplacee : {nom}")

    cible.find("Name").text = nom
    cible.find("Script").text = code          # ElementTree échappe le XML lui-même
    cible.find("Enabled").text = "true"

open(XML + ".bak", "w", encoding="utf-8").write(open(XML, encoding="utf-8").read())
tree.write(XML, encoding="utf-8", xml_declaration=True)
ET.parse(XML)                                  # doit rester lisible

subprocess.run(["docker", "restart", os.environ["JELLYFIN_CONTAINER"]], check=True, capture_output=True)

# Vérification de bout en bout : le code est-il réellement servi ?
attendu = open(sys.argv[1], encoding="utf-8").read().strip().splitlines()[0]
for _ in range(30):
    try:
        servi = urllib.request.urlopen(
            os.environ["JELLYFIN_URL"] + "/JavaScriptInjector/public.js", timeout=8).read().decode()
        if attendu in servi:
            print(f"OK - script servi ({len(servi)} octets au total)")
            sys.exit(0)
    except Exception:
        pass
    time.sleep(5)
sys.exit("ECHEC : le script n'apparait pas dans public.js")
PY
