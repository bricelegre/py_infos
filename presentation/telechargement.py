"""
presentation/telechargement.py

Installation de FinCompta (version Windows) depuis le site.

Les fichiers sont déposés à la main (FTP, gestionnaire de fichiers cPanel)
dans settings.FINCOMPTA_DOWNLOAD_DIR :
- FinCompta-Setup-<version>.exe : programme d'installation complet, produit
  par le workflow « Installateur Windows » du dépôt fincompta_pc ;
- FinCompta-Installateur.exe : ancien installateur en ligne, plus proposé sur
  la page mais toujours servi pour les liens existants.

La version la plus élevée est proposée au téléchargement et publiée dans le
manifeste lu par le script PowerShell (et l'ancien installateur en ligne).
Chaque téléchargement d'un FinCompta-Setup-<version>.exe est enregistré
(TelechargementFinCompta), hors robots, pour le compteur des superusers.
"""

import hashlib
import re
from datetime import timedelta
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.db.models import Count
from django.utils import timezone

from analytics.utils import detect_bot, get_client_ip

from .models import TelechargementFinCompta

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


def enregistrer_telechargement(request, fichier):
    """Compte le téléchargement d'un FinCompta-Setup-<version>.exe (robots exclus)."""
    correspondance = SETUP_RE.match(fichier.name)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if correspondance is None or request.method != "GET" or detect_bot(user_agent)[0]:
        return
    TelechargementFinCompta.objects.create(
        version=correspondance.group(1),
        fichier=fichier.name,
        adresse_ip=get_client_ip(request) or None,
        user_agent=user_agent,
    )


def statistiques_telechargements(version=None):
    """Compteurs affichés aux superusers sur la page « Télécharger FinCompta »."""
    telechargements = TelechargementFinCompta.objects.all()
    stats = {
        "total": telechargements.count(),
        "trente_jours": telechargements.filter(date__gte=timezone.now() - timedelta(days=30)).count(),
        "par_version": telechargements.values("version").annotate(nombre=Count("id")).order_by("-nombre")[:5],
    }
    if version is not None:
        stats["version_courante"] = telechargements.filter(version=version.numero).count()
    return stats
