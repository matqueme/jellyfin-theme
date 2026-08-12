#!/usr/bin/env bash
#
# Resynchronise src/vendor/ultrachromic/ sur un commit d'Ultrachromic.
#
#   ./update-vendor.sh            dernier commit de main
#   ./update-vendor.sh <sha>      un commit precis
#
# Ne commite rien : le but est justement de LIRE le diff avant d'accepter.
# Ultrachromic n'a ni tag ni release, donc une URL sans @version pointe sur
# le HEAD de main. Vendoriser fige cette cible mouvante ; ce script est le
# seul endroit ou elle bouge, volontairement et avec un diff sous les yeux.

set -euo pipefail
cd "$(dirname "$0")"

REPO="CTalvio/Ultrachromic"
VENDOR="src/vendor/ultrachromic"

SHA="${1:-}"
if [ -z "$SHA" ]; then
  SHA=$(curl -sf "https://api.github.com/repos/$REPO/commits/main" \
        | python3 -c 'import json,sys; print(json.load(sys.stdin)["sha"])')
fi

OLD=$(cat "$VENDOR/VERSION" 2>/dev/null || echo "aucun")
echo "Ultrachromic : $OLD"
echo "          ->  $SHA"
[ "$OLD" = "$SHA" ] && { echo "Deja a jour."; exit 0; }

# On retelecharge exactement les modules deja presents : la liste vient de
# l'arborescence locale, pas d'une liste en dur qui se perimerait. Un module
# ajoute par le preset upstream sera signale par build.py, qui refuse de
# construire quand un @import ne se resout pas en local.
find "$VENDOR" -name '*.css' -print0 | while IFS= read -r -d '' f; do
  rel="${f#"$VENDOR"/}"; rel="${rel%.css}"
  curl -sf --max-time 20 -o "$f" \
    "https://cdn.jsdelivr.net/gh/$REPO@$SHA/$rel.css" \
    || { echo "ECHEC : $rel.css n'existe plus en amont"; exit 1; }
done

# Les modules amont referencent leurs images par une URL figee sur main.
# Meme raison qu'au-dessus : on l'epingle sur le commit vendorise.
grep -rl "$REPO/main/assets" "$VENDOR" --include='*.css' 2>/dev/null \
  | xargs -r sed -i "s|$REPO/main/assets|$REPO/$SHA/assets|g"

echo "$SHA" > "$VENDOR/VERSION"
./build.py

cat <<EOF

Recupere. Maintenant, et dans cet ordre :

  git diff -- $VENDOR     lire ce qui a change en amont
  ./apply-local.sh                     tester pour de vrai

Regarder en particulier effects/hoverglow.css, overlayprogress.css et
cornerindicator/ : les modules 08, 10, 11, 12 et 13 s'appuient sur leurs
valeurs exactes et sur leur specificite. Un changement y est silencieux.
EOF
