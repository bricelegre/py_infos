#presentation/views.py
from .modules import MODULES, module_list, plan_comparison
from .utils import send_demo_request, send_contact_request
from . import telechargement
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

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


def telecharger_fincompta(request):
    """Page « Installer FinCompta » (version Windows)."""
    return render(request, "presentation/telecharger-fincompta.html", {
        "version": telechargement.derniere_version(),
        "installateur_disponible": telechargement.installateur_en_ligne_disponible(),
        "script_url": _url_absolue(request, reverse("presentation:fincompta_script")),
    })


def fincompta_manifeste(request):
    """Manifeste lu par l'installateur en ligne et le script PowerShell."""
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


def fincompta_fichier(request, nom):
    chemin = telechargement.fichier_telechargeable(nom)
    if chemin is None:
        raise Http404("Fichier introuvable")
    return FileResponse(chemin.open("rb"), as_attachment=True, filename=nom,
                        content_type="application/vnd.microsoft.portable-executable")
