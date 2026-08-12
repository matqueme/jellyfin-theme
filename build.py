#!/usr/bin/env python3
"""Construit dist/theme.css a partir de src/.

Fusionne Ultrachromic (vendorise) et les modules maison en UN fichier, puis
verifie le resultat. Les verifications sont bloquantes : mieux vaut refuser
de construire que produire une feuille qui casse Jellyfin en silence.

    ./build.py            construit
    ./build.py --check    verifie seulement que dist/ est a jour (CI)

Pourquoi fusionner plutot que chainer des @import : le preset kaleidochromic
importe 16 modules, qui en importent d'autres. Servi par @import, cet arbre
se parcourt en serie — chaque feuille doit etre recue et analysee avant que
la suivante soit decouverte. D'ou trois consequences, toutes vecues :

  - un flash d'interface non stylee au premier chargement, tres visible sur
    la TV ;
  - --accent, definie par type/colorful.css, arrive plusieurs allers-retours
    apres les regles qui l'utilisent, d'ou les valeurs de repli
    var(--accent, 98, 121, 205) semees dans src/ ;
  - une dependance a un depot tiers qui bouge : sans version epinglee,
    jsDelivr sert le HEAD de main.

Fusionne, tout arrive en une requete, dans un ordre fige et reproductible.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
VENDOR = SRC / "vendor" / "ultrachromic"
DIST = ROOT / "dist" / "theme.css"

# Reconnait un @import vers un module Ultrachromic vendorise, avec ou sans
# @version dans l'URL, et en capture le chemin pour le resoudre en local.
UC_IMPORT = re.compile(
    r"@import\s+url\(\s*['\"]?"
    r"https://cdn\.jsdelivr\.net/gh/CTalvio/Ultrachromic(?:@[^/]+)?/"
    r"(?P<path>[^'\")]+?)\.css"
    r"['\"]?\s*\)\s*;",
    re.I,
)

# N'importe quel @import distant. jf_font.css porte le sien sur la meme
# ligne qu'une regle, d'ou une expression sur le texte et non sur les lignes.
ANY_IMPORT = re.compile(r"@import\s+url\(\s*['\"]?(?P<url>[^'\")]+)['\"]?\s*\)\s*;", re.I)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


class Assembler:
    """Concatene les modules en collectant les @import distants au passage."""

    def __init__(self, excluded: set[str] | None = None) -> None:
        self.chunks: list[str] = []
        self.remote: list[str] = []       # @import distants, ordre de decouverte
        self.seen: set[Path] = set()      # anti-boucle sur les imports croises
        self.excluded = excluded or set()  # modules du preset volontairement omis
        self.skipped: set[str] = set()     # ceux effectivement rencontres et omis

    def add_remote(self, url: str) -> None:
        if url not in self.remote:
            self.remote.append(url)

    def emit(self, title: str, body: str) -> None:
        """Ajoute un module, ses @import distants mis de cote."""
        for m in ANY_IMPORT.finditer(body):
            self.add_remote(m.group("url"))
        body = ANY_IMPORT.sub("", body).strip()
        if body:
            self.chunks.append(f"/* ===== {title} ===== */\n{body}\n")

    def add_vendor(self, rel: str) -> None:
        """Ajoute un module vendorise, ses dependances Ultrachromic d'abord.

        Les @import vers Ultrachromic sont resolus en local et remplaces par
        le contenu du fichier ; ils ne comptent donc pas comme distants.
        """
        if rel in self.excluded:
            self.skipped.add(rel)
            return
        path = (VENDOR / f"{rel}.css").resolve()
        if path in self.seen:
            return
        self.seen.add(path)
        if not path.exists():
            sys.exit(f"module vendorise absent : {path.relative_to(ROOT)}\n"
                     f"  lancer ./update-vendor.sh")

        raw = path.read_text(encoding="utf-8")

        # Dependances d'abord, dans l'ordre du fichier.
        for m in UC_IMPORT.finditer(raw):
            self.add_vendor(m.group("path"))

        # Puis le corps propre du module, ses imports Ultrachromic retires.
        self.emit(f"ultrachromic/{rel}.css", UC_IMPORT.sub("", raw))


def lire_liste(nom: str) -> list[str]:
    """Lit un fichier de src/ : une entree par ligne, # pour commenter."""
    fichier = SRC / nom
    if not fichier.exists():
        return []
    return [l.split("#", 1)[0].strip()
            for l in fichier.read_text(encoding="utf-8").splitlines()
            if l.split("#", 1)[0].strip()]


def build() -> str:
    theme_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    uc_sha = (VENDOR / "VERSION").read_text(encoding="utf-8").strip()

    asm = Assembler(excluded=set(lire_liste("vendor.exclude")))

    # 1. Ultrachromic. Le preset porte l'ordre de chargement : on le suit
    #    plutot que de recopier sa liste, pour ne pas avoir a la maintenir.
    asm.add_vendor("presets/kaleidochromic_preset")

    # 2. Les variantes ajoutees par-dessus le preset.
    for rel in lire_liste("vendor.list"):
        asm.add_vendor(rel)

    # Un module liste en exclusion mais jamais rencontre est le signe d'une
    # faute de frappe, ou d'un module que le preset amont ne charge plus :
    # dans les deux cas l'exclusion ne fait rien et le croire serait pire
    # que l'erreur.
    inutiles = asm.excluded - asm.skipped
    if inutiles:
        sys.exit(f"vendor.exclude : jamais rencontre(s) -> {sorted(inutiles)}\n"
                 f"  chemin errone, ou module que le preset ne charge plus")

    # 3. Les modules maison, dans l'ordre de leur prefixe numerique.
    #    Cet ordre reproduit celui du fichier d'origine : le modifier
    #    change la cascade, donc le rendu.
    own = sorted(p for p in SRC.glob("*.css"))
    if not own:
        sys.exit("aucun module dans src/")
    for path in own:
        asm.emit(path.name, path.read_text(encoding="utf-8"))

    # Une exclusion doit se voir dans le fichier servi : sans cette mention,
    # un module absent du resultat est indiscernable d'un module oublie.
    exclusions = ""
    if asm.skipped:
        exclusions = ("\n   Modules du preset volontairement exclus :\n"
                      + "".join(f"          {m}.css\n" for m in sorted(asm.skipped)))

    header = f"""/* =====================================================================
   Theme Jellyfin — matqueme
   Version {theme_version} — Jellyfin 10.11.x

   FICHIER CONSTRUIT — NE PAS EDITER.
   Genere par build.py depuis src/. Toute modification faite ici sera
   perdue au prochain build. Editer src/, puis relancer ./build.py.

   Base : Ultrachromic de CTalvio (MIT), vendorise et fusionne.
          commit {uc_sha}
   Icones : Phosphor Bold 2.1.2 (MIT).
{exclusions}   ===================================================================== */
"""

    # Les @import remontent en tete : un @import place apres une regle est
    # ignore par le navigateur. C'est la raison d'etre de la collecte.
    imports = "".join(f"@import url('{u}');\n" for u in asm.remote)

    return header + "\n" + imports + "\n" + "\n".join(asm.chunks)


def check(css: str) -> None:
    """Verifications bloquantes sur le fichier construit."""
    nc = strip_comments(css)

    # 1. Accolades equilibrees : un decoupage rate se voit ici.
    if nc.count("{") != nc.count("}"):
        sys.exit(f"accolades desequilibrees : {nc.count('{')} ouvrantes, "
                 f"{nc.count('}')} fermantes")

    # 2. Aucun @import apres une regle, sinon il est ignore silencieusement.
    #    Verifie que la remontee en tete a bien fonctionne.
    lines = css.splitlines()
    imports = [i for i, l in enumerate(lines, 1) if l.strip().startswith("@import")]
    first_rule = next((i for i, l in enumerate(lines, 1)
                       if re.match(r"^[.#:\[a-zA-Z]", l) and not l.strip().startswith("@")),
                      len(lines) + 1)
    if imports and max(imports) > first_rule:
        sys.exit(f"@import ligne {max(imports)}, apres une regle ligne {first_rule}")

    # 3. Tout display en !important doit etre garde par :not(.hide).
    #    Jellyfin masque ses pages avec .hide { display: none !important } ;
    #    un selecteur d'ID l'emporte sur cette classe a !important egal, et
    #    la page de connexion restait affichee par-dessus l'accueil.
    #    Ne s'applique qu'aux modules maison : le code vendorise est connu
    #    pour fonctionner, et le reecrire n'est pas le role du build.
    own = "\n".join(p.read_text(encoding="utf-8") for p in sorted(SRC.glob("*.css")))
    bad = [m.group(1).strip()
           for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", strip_comments(own))
           if re.search(r"\bdisplay\s*:[^;]*!important", m.group(2))
           and "display: none" not in m.group(2)
           and ":not(.hide)" not in m.group(1)]
    if bad:
        sys.exit(f"display sans garde :not(.hide) -> {bad}")


def main() -> None:
    css = build()
    check(css)

    if "--check" in sys.argv:
        current = DIST.read_text(encoding="utf-8") if DIST.exists() else None
        if current != css:
            sys.exit("dist/theme.css n'est pas a jour : lancer ./build.py et commiter")
        print(f"OK - dist/theme.css a jour ({len(css.encode())} octets)")
        return

    DIST.parent.mkdir(parents=True, exist_ok=True)
    DIST.write_text(css, encoding="utf-8")
    rules = len(re.findall(r"\{", strip_comments(css)))
    print(f"OK - dist/theme.css : {len(css.splitlines())} lignes, "
          f"{len(css.encode())} octets, {rules} regles")


if __name__ == "__main__":
    main()
