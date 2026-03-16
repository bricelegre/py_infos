#presentation/views.py
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
    
    return render(request, "presentation/accueil.html")

def detail_comptabilite(request):

    if request.method == "POST" :

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")
        
        return redirect("presentation:details-comptabilite")

    return render(request, "presentation/details-comptabilite.html")

def detail_grh(request):

    if request.method == "POST" :

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")
        
        return redirect("presentation:details_grh")

    return render(request, "presentation/details-grh.html")

def detail_paies(request):

    if request.method == "POST":

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")

        return redirect("presentation:details_paies")

    return render(request, "presentation/details-paies.html")

def detail_etats_financiers(request):

    if request.method == "POST":

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")

        return redirect("presentation:details_etats_financiers")

    return render(request, "presentation/details-etats.html")

def detail_facturation_crm(request):

    if request.method == "POST":

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")

        return redirect("presentation:detail_facturation_crm")
    
    return render(request, "presentation/details-facturation-crm.html")

def detail_crm(request):

    if request.method == "POST":

        success, err = send_demo_request(request)

        if success:
            messages.success(request, "Votre demande de démo a été envoyée avec succès.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'envoi.")

        return redirect("presentation:detail_crm")

    return render(request, "presentation/details-crm.html")