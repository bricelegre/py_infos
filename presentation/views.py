#presentation/views.py
from .modules import MODULES, module_list, plan_comparison
from .utils import send_demo_request, send_contact_request, send_licence_request
from . import telechargement
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

def accueil(request):

    if request.method == "POST" :

        success, err = send_contact_request(request)

        if success:
            messages.success(request, "Votre demande a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")
        
        return redirect("presentation:accueil")
    
    return render(request, "presentation/accueil.html", {
        "modules": module_list(),
        "plan_comparison": plan_comparison(),
        "offre": offre_licence(),
    })

def detail_module(request, slug):

    module = MODULES[slug]

    if request.method == "POST":

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")

        return redirect(module["url_name"])

    return render(request, "presentation/details-module.html", {
        "module": module,
        "modules": module_list(),
    })


def _url_absolue(request, chemin):
    base = settings.FINCOMPTA_SITE_URL.rstrip("/")
    return base + chemin if base else request.build_absolute_uri(chemin)


# Prix de la clé de licence (version complète), en FCFA, et promotion en cours
PRIX_LICENCE = 150_000
PRIX_LICENCE_PROMO = 100_000
FIN_PROMO_LICENCE = date(2026, 12, 31)


def offre_licence():
    """Prix de la version complète ; la promotion s'arrête d'elle-même après FIN_PROMO_LICENCE."""
    promo = timezone.localdate() <= FIN_PROMO_LICENCE
    fcfa = lambda montant: f"{montant:,}".replace(",", "\u202f") + " FCFA"
    return {
        "prix": fcfa(PRIX_LICENCE_PROMO if promo else PRIX_LICENCE),
        "prix_normal": fcfa(PRIX_LICENCE),
        "promo": promo,
        "fin_promo": FIN_PROMO_LICENCE,
    }


def telecharger_fincompta(request):
    """Page « Installer FinCompta » (version Windows) et demande de clé de licence."""
    if request.method == "POST":
        success, err = send_licence_request(request)
        if success:
            messages.success(request, "Votre demande de clé a été envoyée. Nous vous recontactons rapidement "
                                      "pour le règlement ; la clé vous est ensuite envoyée par email.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi. Vérifiez les champs "
                                    "ou contactez-nous au 0708218574.")
        return redirect(reverse("presentation:telecharger_fincompta") + "#licence")

    return render(request, "presentation/telecharger-fincompta.html", {
        "offre": offre_licence(),
        "version": telechargement.derniere_version(),
        "script_url": _url_absolue(request, reverse("presentation:fincompta_script")),
    })


def fincompta_manifeste(request):
    """Manifeste lu par le script PowerShell (et l'ancien installateur en ligne)."""
    version = telechargement.derniere_version()
    if version is None:
        raise Http404("Aucune version publiée")
    url = _url_absolue(request, reverse("presentation:fincompta_fichier", args=[version.fichier.name]))
    contenu = (
        "[FinCompta]\r\n"
        f"version={version.numero}\r\n"
        f"url={url}\r\n"
        f"sha256={version.sha256}\r\n"
        f"taille={version.taille}\r\n"
    )
    reponse = HttpResponse(contenu, content_type="text/plain; charset=utf-8")
    reponse["Cache-Control"] = "no-cache"
    return reponse


def fincompta_script(request):
    """Installation par PowerShell : irm <url> | iex"""
    reponse = render(request, "presentation/installer-fincompta.ps1", {
        "manifeste_url": _url_absolue(request, reverse("presentation:fincompta_manifeste")),
        "script_url": _url_absolue(request, request.path),
    }, content_type="text/plain; charset=utf-8")
    reponse["Cache-Control"] = "no-cache"
    return reponse


def fincompta_demo(request):
    """Programme d'installation de la dernière version (démarre en démonstration sans clé)."""
    version = telechargement.derniere_version()
    if version is None:
        raise Http404("Aucune version publiée")
    telechargement.enregistrer_telechargement(request, version.fichier)
    return FileResponse(version.fichier.open("rb"), as_attachment=True, filename=version.fichier.name,
                        content_type="application/vnd.microsoft.portable-executable")


def fincompta_fichier(request, nom):
    chemin = telechargement.fichier_telechargeable(nom)
    if chemin is None:
        raise Http404("Fichier introuvable")
    telechargement.enregistrer_telechargement(request, chemin)
    return FileResponse(chemin.open("rb"), as_attachment=True, filename=nom,
                        content_type="application/vnd.microsoft.portable-executable")
