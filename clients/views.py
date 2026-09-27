from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from info.provisioning import provision
from .utils import generate_password

def add_client(request, cust_plan_text):
    plan_map = {
        "free": 1,
        "starter": 2,
        "premium": 3,
    }

    plan_key = (cust_plan_text or "").strip().lower()
    cust_plan = plan_map.get(plan_key)

    if cust_plan is None:
        messages.warning(request, "Plan défini non reconnu.")
        return redirect("presentation:accueil")

    context = {
        "cust_plan_text": plan_key,
        "cust_plan": cust_plan,
    }

    if request.method != "POST":
        return render(request, "clients/add_clients.html", context)

    # Récupération des données AVANT validation
    user_pseudo = (request.POST.get("user_pseudo") or "").strip()
    cust_identifiant = (request.POST.get("cust_identifiant") or "").strip()
    cust_company_name = (request.POST.get("cust_company_name") or "").strip()
    cust_email = (request.POST.get("cust_email") or "").strip().lower()
    cust_fone = (request.POST.get("cust_fone") or "").strip()

    # Conserver les valeurs pour réaffichage si erreur
    context.update({
        "user_pseudo": user_pseudo,
        "cust_identifiant": cust_identifiant,
        "cust_company_name": cust_company_name,
        "cust_email": cust_email,
        "cust_fone": cust_fone,
    })

    # Validation minimale
    if not all([user_pseudo, cust_identifiant, cust_company_name, cust_email]):
        messages.error(request, "Veuillez renseigner tous les champs obligatoires.")
        return render(request, "clients/add_clients.html", context)

    # Validation email
    try:
        validate_email(cust_email)
    except ValidationError:
        messages.error(request, "Adresse email invalide.")
        return render(request, "clients/add_clients.html", context)

    user_password = generate_password(8)
    cust_end_subscription = timezone.localdate() + relativedelta(months=1)

    # Le compte est créé par fincompta (API POST /api/provision/) : client,
    # référentiel SYSCOHADA, paramètres de paie, administrateur et rôles, en
    # une transaction. L'unicité de l'identifiant et de l'email y est vérifiée.
    result = provision("fincompta", {
        "identifiant": cust_identifiant,
        "nom": cust_company_name,
        "pseudo": user_pseudo,
        "password": user_password,
        "email": cust_email,
        "telephone": cust_fone,
        "plan": cust_plan,  # on garde le plan validé depuis l'URL
        "fin_abonnement": cust_end_subscription.isoformat(),
    })
    if not result.ok:
        messages.error(request, result.error)
        return render(request, "clients/add_clients.html", context)

    # Envoi d'email APRÈS création du compte
    email_sent = False
    email_err = None

    if cust_email:
        subject = "Votre compte Fincompta a été créé"
        email_context = {
            "cust_identifiant": cust_identifiant,
            "company_name": cust_company_name,
            "user_pseudo": user_pseudo,
            "email": cust_email,
            "password": user_password,
            "cust_plan_text": plan_key,
            "login_url": settings.FINCOMPTA_LOGIN_URL,
        }

        text_body = render_to_string("clients/emails/account_created.txt", email_context)
        html_body = render_to_string("clients/emails/account_created.html", email_context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cust_email],
        )
        email.attach_alternative(html_body, "text/html")

        try:
            email.send(fail_silently=False)
            email_sent = True
        except Exception as e:
            email_err = str(e)
    else:
        email_err = "Aucun email fourni"

    if email_sent:
        messages.success(
            request,
            "Compte client créé avec succès. Vérifiez votre email pour les identifiants de connexion."
        )
    else:
        messages.warning(
            request,
            f"Compte créé, mais email non envoyé : {email_err}"
        )

    return redirect("clients:ajouter_client", cust_plan_text=plan_key)
