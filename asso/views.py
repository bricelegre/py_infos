from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from info.provisioning import provision
from .utils import generate_password


def add_asso(request):

    if request.method != "POST":
        return render(request, "asso/add_asso.html", {})

    user_pseudo = (request.POST.get("user_pseudo") or "").strip()
    cust_identifiant = (request.POST.get("cust_identifiant") or "").strip()
    cust_company_name = (request.POST.get("cust_company_name") or "").strip()
    cust_email = (request.POST.get("cust_email") or "").strip().lower()
    cust_fone = (request.POST.get("cust_fone") or "").strip()

    if not user_pseudo or not cust_identifiant:
        messages.error(request, "Pseudo et identifiant sont obligatoires.")
        return redirect("asso:ajouter_asso")

    cust_plan = 3
    user_password = generate_password(8)
    cust_end_subscription = timezone.now().date() + relativedelta(months=1)
    email_sent = False
    email_err = None

    # --- 1) Création par syscebnl (API POST /api/provision/) : entité, plan
    # SYCEBNL, journaux, tiers Divers, paie, administrateur et rôles, en une
    # transaction. L'unicité de l'identifiant et de l'email y est vérifiée.
    result = provision("syscebnl", {
        "identifiant": cust_identifiant,
        "nom": cust_company_name or cust_identifiant,
        "pseudo": user_pseudo,
        "password": user_password,
        "email": cust_email,
        "telephone": cust_fone,
        "plan": cust_plan,
        "fin_abonnement": cust_end_subscription.isoformat(),
    })
    if not result.ok:
        messages.error(request, result.error)
        return redirect("asso:ajouter_asso")

    # --- 2) Email AFTER creation ---
    if cust_email:
        subject = "Votre compte Fincompta a été créé"

        context = {
            "cust_identifiant": cust_identifiant,
            "company_name": cust_company_name,
            "user_pseudo": user_pseudo,
            "email": cust_email,
            "password": user_password,
            "login_url": settings.ASSO_LOGIN_URL,
        }

        text_body = render_to_string("asso/emails/account_created.txt", context)
        html_body = render_to_string("asso/emails/account_created.html", context)

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
        messages.success(request, "Compte association créé avec succès. Vérifiez votre email pour les identifiants de connexion.")
    else:
        messages.warning(request, f"Compte créé, mais email non envoyé : {email_err}")

    return redirect("asso:ajouter_asso")
