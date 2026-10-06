#!/usr/bin/env python3
"""Genere src/91-icones-mui.css : les icones SVG de MUI redessinees en Phosphor.

MUI rend ses icones en <svg class="MuiSvgIcon-root" data-testid="CastIcon">.
Le data-testid est conserve en production : c'est une accroche stable,
independante de la langue et de l'etat du composant, contrairement a
l'aria-label ou a l'URL d'un lien.

Le dessin d'un SVG ne se remplace pas en CSS. On masque donc ses traces et
on peint l'element lui-meme : fond en currentColor, decoupe par un masque
qui est le SVG Phosphor. L'icone garde exactement la taille et la couleur
que MUI lui donne, ou qu'elle soit (en-tete, cartes, menus, dashboard).

Les masques pointent vers les SVG Phosphor sur jsDelivr, la ou le theme
charge deja la police Phosphor : aucune dependance de plus, et seuls les
glyphes affiches sont telecharges (CORS ouvert, cache immuable d'un an).
Les embarquer en data: doublait le poids du theme. Ce script n'est a
relancer que pour modifier la table ci-dessous ; build.py n'en depend pas,
il verifie seulement que chaque SVG existe.

    ./tools/icones-mui.py
"""

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "91-icones-mui.css"

# Meme version que la police de src/00-imports.css (@phosphor-icons/web
# 2.1.2, construite sur core 2.1.1) : les glyphes doivent etre identiques.
CORE = "https://cdn.jsdelivr.net/npm/@phosphor-icons/core@2.1.1/assets/bold/{}-bold.svg"

# Icone MUI (data-testid sans le suffixe Icon) -> icone Phosphor.
# Quand l'icone a un equivalent Material deja remappe dans 90-icones.css,
# c'est le meme glyphe : une action a la meme icone dans les deux familles
# de composants.
#
# Laissees de cote : les cases a cocher, les boutons radio et la fleche des
# listes deroulantes (CheckBox*, IndeterminateCheckBox, RadioButton*,
# ArrowDropDown). Ce sont des controles, dessines par 21-champs.css et
# 22-cases.css.
MAPPING = {
    # --- equivalents de 90-icones.css
    "Add": "plus",
    "Album": "vinyl-record",
    "ArrowBack": "arrow-left",
    "ArrowUpward": "arrow-up",
    "Book": "book",
    "Cast": "monitor-arrow-up",
    "Check": "check",
    "ChevronLeft": "caret-left",
    "ChevronRight": "caret-right",
    "Close": "x",
    "ClosedCaption": "closed-captioning",
    "ContentCopy": "copy",
    "Dashboard": "squares-four",
    "Delete": "trash",
    "Download": "download-simple",
    "DragHandle": "dots-six",
    "Dvr": "monitor-play",
    "Edit": "pencil-simple",
    "ExpandMore": "caret-down",
    "Favorite": "heart",
    "FileDownload": "download-simple",
    "FilterAlt": "funnel",
    "Folder": "folder",
    "Fullscreen": "corners-out",
    "Groups": "users-three",
    "Home": "house",
    "Image": "image",
    "Info": "info",
    "KeyboardArrowLeft": "caret-left",
    "KeyboardArrowRight": "caret-right",
    "LiveTv": "television",
    "Menu": "list",
    "MoreVert": "dots-three-vertical",
    "Movie": "film-slate",
    "MusicNote": "music-note",
    "OndemandVideo": "monitor-play",  # bibliotheque mixte (12.2), comme Dvr
    "NavigateBefore": "caret-left",
    "NavigateNext": "caret-right",
    "Pause": "pause",
    "Person": "user",
    "PhonelinkLock": "lock-key",
    "Photo": "image",
    "PlayArrow": "play",
    "PlaylistAdd": "playlist",
    "Refresh": "arrow-clockwise",
    "RemoveCircle": "minus-circle",
    "Save": "floppy-disk",
    "Search": "magnifying-glass",
    "Settings": "gear",
    "Shuffle": "shuffle",
    "SortByAlpha": "sort-ascending",
    "Star": "star",
    "Stop": "stop",
    "Storage": "hard-drives",
    "Theaters": "film-reel",
    "Tune": "sliders-horizontal",
    "Tv": "television-simple",
    "VideoLibrary": "film-strip",
    # --- propres a MUI
    "AccountCircle": "user-circle",
    "Analytics": "chart-bar",
    "AppSettingsAlt": "gear-six",
    "ArrowDownward": "arrow-down",
    "ArrowForwardIosSharp": "caret-right",
    "ArrowLeft": "caret-left",
    "ArrowRight": "caret-right",
    "Article": "article",
    "Backup": "cloud-arrow-up",
    "Calendar": "calendar-blank",
    "Cancel": "x-circle",
    "CastConnected": "monitor-arrow-up",  # le libelle a cote dit que la diffusion est active
    "Clear": "x",
    "ClearAll": "broom",
    "Comment": "chat-text",
    "Computer": "desktop",
    "DateRange": "calendar",
    "DensityLarge": "rows",
    "DensityMedium": "list",
    "DensitySmall": "list-dashes",
    "Devices": "devices",
    "DownloadDone": "check-circle",
    "ErrorOutline": "warning-circle",
    "ExpandLess": "caret-up",
    "Extension": "puzzle-piece",
    "FilterAltOff": "funnel-x",  # Reinitialiser les filtres (12.2)
    "FilterList": "funnel-simple",
    "FilterListOff": "funnel-simple-x",
    "FirstPage": "caret-line-left",
    "FullscreenExit": "corners-in",
    "GroupAdd": "users-three",  # SyncPlay hors groupe : meme glyphe que Groups
    "HelpOutline": "question",
    "ImageNotSupported": "image-broken",
    "InfoOutlined": "info",
    "Lan": "network",
    "LastPage": "caret-line-right",
    "LibraryAdd": "folder-plus",
    "LocationSearching": "crosshair",
    "Logout": "sign-out",
    "Memory": "cpu",
    "MoreHoriz": "dots-three",
    "MusicVideo": "music-notes",
    "Notifications": "bell",
    "OpenInNew": "arrow-square-out",
    "Palette": "palette",
    "People": "users",
    "PermMedia": "images",
    "PersonAdd": "user-plus",
    "PersonOff": "user-minus",
    "PersonRemove": "user-minus",
    "PhotoAlbum": "images-square",
    "PlayCircle": "play-circle",
    "PowerSettingsNew": "power",
    "Queue": "queue",
    "ReportProblemOutlined": "warning",
    "RestartAlt": "arrow-counter-clockwise",
    "Restore": "clock-counter-clockwise",
    "SettingsRemote": "game-controller",  # Phosphor n'a pas de telecommande
    "Smartphone": "device-mobile",
    "Sort": "arrows-down-up",
    "StopCircle": "stop-circle",
    "SuccessOutlined": "check-circle",
    "SyncAlt": "arrows-left-right",
    "Tablet": "device-tablet",
    "Upload": "upload-simple",
    "Usb": "usb",
    "Videocam": "video-camera",
    "ViewColumn": "columns",
    "ViewList": "list-bullets",
    "ViewModule": "grid-four",
    "Visibility": "eye",
    "VisibilityOff": "eye-slash",
    "VpnKey": "key",
    "Warning": "warning",
}

HEADER = """/* --- 91. Icones MUI : SVG Material redessines en Phosphor Bold -------
   FICHIER GENERE par tools/icones-mui.py : modifier la table du script et
   le relancer, pas ce fichier.

   Chaque icone MUI porte data-testid="<Nom>Icon", conserve en production.
   Ses traces sont masquees et l'element est peint en currentColor, decoupe
   par le SVG Phosphor : taille et couleur restent celles que MUI donne.
   --icon-scale reduit le glyphe comme pour les icones de police. Une icone
   absente de la table garde son dessin Material. */
"""


def check(name: str) -> str:
    """URL du SVG Phosphor, apres verification qu'il existe."""
    url = CORE.format(name)
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            ok = r.status == 200 and "svg" in r.headers.get("content-type", "")
    except Exception as e:  # 404 compris : nom Phosphor faux
        sys.exit(f"{name} : {e}")
    if not ok:
        sys.exit(f"{name} : reponse inattendue")
    return url


def main() -> None:
    cache: dict[str, str] = {}
    for ph in sorted(set(MAPPING.values())):
        cache[ph] = check(ph)

    sel = lambda n: f'.MuiSvgIcon-root[data-testid="{n}Icon"]'
    names = sorted(MAPPING)
    out = [HEADER]
    out.append(",\n".join(sel(n) for n in names) + " {")
    out.append("  background-color: currentColor;")
    out.append("  -webkit-mask: var(--ph) center / calc(100% * var(--icon-scale)) no-repeat;")
    out.append("  mask: var(--ph) center / calc(100% * var(--icon-scale)) no-repeat;")
    out.append("}\n")
    out.append(",\n".join(sel(n) + " > *" for n in names) + " {")
    out.append("  visibility: hidden;")
    out.append("}\n")
    for n in names:
        out.append(f'{sel(n)} {{ --ph: url("{cache[MAPPING[n]]}"); }} /* {MAPPING[n]} */')
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} : {len(names)} icones MUI, {len(cache)} glyphes verifies, "
          f"{OUT.stat().st_size} octets")


if __name__ == "__main__":
    main()
