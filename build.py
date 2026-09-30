#!/usr/bin/env python3
"""Construit dist/theme.css a partir de src/.

Concatene les modules de src/ dans l'ordre de leur prefixe numerique, en un
seul fichier, puis verifie le resultat. Les verifications sont bloquantes :
mieux vaut refuser de construire que produire une feuille qui casse
Jellyfin en silence.

    ./build.py            construit
    ./build.py --check    verifie seulement que dist/ est a jour (CI)

Un seul fichier plutot qu'une chaine d'@import : une feuille servie par
@import n'est decouverte qu'une fois la precedente recue et analysee, d'ou
un flash d'interface non stylee au premier chargement, tres visible sur la
TV. Seules les polices restent importees (voir src/00-imports.css).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist" / "theme.css"

# N\'importe quel @import distant, reconnu sur le texte et non sur les lignes.
ANY_IMPORT = re.compile(r"@import\s+url\(\s*['\"]?(?P<url>[^'\")]+)['\"]?\s*\)\s*;", re.I)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


class Assembler:
    """Concatene les modules en collectant les @import distants au passage."""

    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.remote: list[str] = []  # @import distants, ordre de decouverte

    def emit(self, title: str, body: str) -> None:
        """Ajoute un module, ses @import distants mis de cote."""
        for m in ANY_IMPORT.finditer(body):
            if m.group("url") not in self.remote:
                self.remote.append(m.group("url"))
        body = ANY_IMPORT.sub("", body).strip()
        if body:
            self.chunks.append(f"/* ===== {title} ===== */\n{body}\n")


def build() -> str:
    theme_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    asm = Assembler()

    # Les modules, dans l'ordre de leur prefixe numerique. Cet ordre est
    # celui de la cascade : le modifier change le rendu.
    own = sorted(SRC.glob("*.css"))
    if not own:
        sys.exit("aucun module dans src/")
    for path in own:
        asm.emit(path.name, path.read_text(encoding="utf-8"))

    header = f"""/* =====================================================================
   Theme Jellyfin, par matqueme
   Version {theme_version}, pour Jellyfin 12.x, layout Modern

   FICHIER CONSTRUIT : NE PAS EDITER.
   Genere par build.py depuis src/. Toute modification faite ici sera
   perdue au prochain build. Editer src/, puis relancer ./build.py.

   Police : Plus Jakarta Sans (OFL). Icones : Phosphor Bold 2.1.2 (MIT).
   ===================================================================== */
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
