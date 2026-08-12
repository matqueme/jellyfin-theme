#!/usr/bin/env bash
#
# Injecte dist/theme.css directement dans branding.xml, sans passer par le
# CDN. C'est la voie de secours du mode CDN documente dans le README :
# aucune dependance reseau cote client, mais il faut acces au serveur et
# relancer ce script a chaque modification.
#
#   ./apply-local.sh
#   JELLYFIN_DIR=/srv/jellyfin ./apply-local.sh
#
# Toutes les verifications sont bloquantes : mieux vaut refuser d'appliquer
# qu'ecrire un branding.xml casse, qui ferait silencieusement retomber
# Jellyfin sur le theme par defaut.

set -euo pipefail
cd "$(dirname "$0")"

JELLYFIN_DIR="${JELLYFIN_DIR:-$HOME/docker/jellyfin}"
JELLYFIN_CONTAINER="${JELLYFIN_CONTAINER:-jellyfin}"
JELLYFIN_URL="${JELLYFIN_URL:-http://localhost:8096}"

./build.py

JELLYFIN_DIR="$JELLYFIN_DIR" \
JELLYFIN_CONTAINER="$JELLYFIN_CONTAINER" \
JELLYFIN_URL="$JELLYFIN_URL" \
python3 - <<'PY'
import os, re, subprocess, sys, time, urllib.request
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

XML = os.path.join(os.environ["JELLYFIN_DIR"], "config", "branding.xml")
CONTAINER = os.environ["JELLYFIN_CONTAINER"]
URL = os.environ["JELLYFIN_URL"]

css = open("dist/theme.css", encoding="utf-8").read()

if not os.path.exists(XML):
    sys.exit(f"introuvable : {XML}\n  definir JELLYFIN_DIR")

# Le CSS est stocke comme texte dans branding.xml. L'ancienne version de ce
# script INTERDISAIT < et & dans la feuille pour ne pas casser le XML ; c'est
# devenu intenable des lors qu'Ultrachromic est vendorise, jf_font.css
# important Google Fonts avec un & dans son URL. On echappe donc, au lieu
# d'interdire. Corollaire : src/ peut desormais contenir < et &, donc aussi
# les media queries de la forme @media (width < 50em).
payload = escape(css)

xml = open(XML, encoding="utf-8").read()
open(XML + ".bak", "w", encoding="utf-8").write(xml)

new, n = re.subn(r"<CustomCss>.*?</CustomCss>|<CustomCss\s*/>",
                 lambda m: "<CustomCss>" + payload + "</CustomCss>",
                 xml, count=1, flags=re.S)
if n != 1:
    sys.exit("balise CustomCss introuvable dans branding.xml")
open(XML, "w", encoding="utf-8").write(new)

# Relecture par un vrai parseur : valide le XML ET verifie que le texte se
# desechappe exactement en ce qu'on voulait ecrire.
node = ET.parse(XML).getroot().find("CustomCss")
if node is None or (node.text or "") != css:
    sys.exit("contenu altere a l'ecriture — branding.xml.bak conserve")

subprocess.run(["docker", "restart", CONTAINER], check=True, capture_output=True)

# Verification de bout en bout : Jellyfin sert-il exactement ce fichier ?
for _ in range(30):
    try:
        served = urllib.request.urlopen(f"{URL}/Branding/Css", timeout=8).read().decode()
        if served == css:
            print(f"OK - {len(css)} octets servis et conformes")
            sys.exit(0)
    except Exception:
        pass
    time.sleep(5)
sys.exit(f"ECHEC : {URL}/Branding/Css ne renvoie pas le CSS attendu")
PY
