"""
presentation/telechargement.py

Installation de FinCompta (version Windows) depuis le site.

Les fichiers sont déposés à la main (FTP, gestionnaire de fichiers cPanel)
dans settings.FINCOMPTA_DOWNLOAD_DIR :
- FinCompta-Setup-<version>.exe : installateur complet, produit par le
  workflow « Installateur Windows » du dépôt fincompta_pc ;
- FinCompta-Installateur.exe : installateur en ligne (desktop/web-installer.iss),
  à déposer une seule fois : il télécharge toujours la dernière version.

La version la plus élevée est publiée automatiquement dans le manifeste lu
par l'installateur en ligne et par le script PowerShell.
"""

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings

INSTALLATEUR_EN_LIGNE = "FinCompta-Installateur.exe"
SETUP_RE = re.compile(r"^FinCompta-Setup-(\d+(?:\.\d+){0,3})\.exe$")

# Empreintes déjà calculées : {chemin: (taille, mtime, sha256)}
_sha256_cache = {}


@dataclass(frozen=True)
class Version:
    numero: str
    fichier: Path
    taille: int
    sha256: str


def dossier():
    return Path(settings.FINCOMPTA_DOWNLOAD_DIR)


def _cle_version(numero):
    return tuple(int(n) for n in numero.split("."))


def _sha256(chemin):
    stat = chemin.stat()
    cache = _sha256_cache.get(chemin)
    if cache and cache[:2] == (stat.st_size, stat.st_mtime):
        return cache[2]
    h = hashlib.sha256()
    with chemin.open("rb") as f:
        for bloc in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloc)
    _sha256_cache[chemin] = (stat.st_size, stat.st_mtime, h.hexdigest())
    return h.hexdigest()


def derniere_version():
    """Dernière FinCompta-Setup-<version>.exe déposée, ou None."""
    try:
        candidats = [
            (SETUP_RE.match(f.name).group(1), f)
            for f in dossier().iterdir()
            if f.is_file() and SETUP_RE.match(f.name)
        ]
    except OSError:
        return None
    if not candidats:
        return None
    numero, fichier = max(candidats, key=lambda c: _cle_version(c[0]))
    return Version(numero, fichier, fichier.stat().st_size, _sha256(fichier))


def fichier_telechargeable(nom):
    """Chemin d'un fichier publié (installateur en ligne ou Setup), ou None."""
    if nom != INSTALLATEUR_EN_LIGNE and not SETUP_RE.match(nom):
        return None
    chemin = dossier() / nom
    return chemin if chemin.is_file() else None


def installateur_en_ligne_disponible():
    return fichier_telechargeable(INSTALLATEUR_EN_LIGNE) is not None
