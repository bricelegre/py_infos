#presentation/views.py
from .modules import MODULES, module_list, plan_comparison
from .utils import send_demo_request, send_contact_request
from django.contrib import messages
from django.shortcuts import render, redirect

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
