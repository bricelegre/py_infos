from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from clients.utils import *
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.db.models import Q, F
from slugify import slugify
from .utils import *
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db import transaction, IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def add_client(request, cust_plan_text):
    plan_map = {
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

    # Unicité côté applicatif
    if Customer.objects.filter(
        Q(cust_identifiant__iexact=cust_identifiant) |
        Q(cust_email__iexact=cust_email)
    ).exists():
        messages.error(request, "Identifiant ou email déjà utilisé.")
        return render(request, "clients/add_clients.html", context)

    if Users.objects.filter(
        Q(user_email__iexact=cust_email) |
        Q(user_pseudo__iexact=user_pseudo)
    ).exists():
        messages.error(request, "Pseudo ou email utilisateur déjà utilisé.")
        return render(request, "clients/add_clients.html", context)

    user_password = generate_password(8)
    user_password_hashed = make_password(user_password)
    cust_slug = slugify(cust_identifiant)
    cust_end_subscription = timezone.localdate() + relativedelta(months=1)

    try:
        with transaction.atomic():
            customer = Customer.objects.create(
                cust_identifiant=cust_identifiant,
                cust_company_name=cust_company_name,
                cust_email=cust_email,
                cust_fone=cust_fone,
                cust_plan=cust_plan,  # on garde le plan validé depuis l'URL
                cust_end_subscription=cust_end_subscription,
                cust_slug=cust_slug,
                cust_status=1,
            )

            cust_id = customer.cust_id

            # Initialisation des données client
            initialize_customer_data(cust_id)

            user_created = Users.objects.create(
                user_pseudo=user_pseudo,
                user_password=user_password_hashed,
                cust_id=cust_id,
                user_email=cust_email,
            )

            user_id = user_created.user_id

            roles = {
                "accounting": "manager_comptable",
                "employees": "rh_manager",
                "pay": "paie_manager",
                "sales": "manager_ventes",
                "taxation": "utilisateur_impots",
                "users": "manager_utilisateur",
            }

            user_roles = []
            for module_key, role_name in roles.items():
                role_id = get_role_id_by_name(role_name)
                module_id = get_module_id_by_key(module_key)
                if role_id and module_id:
                    user_roles.append(
                        UserRole(user_id=user_id, roles_id=role_id, module_id=module_id)
                    )

            if user_roles:
                UserRole.objects.bulk_create(user_roles)

            CompanyData.objects.create(
                cust_id=cust_id,
                company_name=cust_company_name,
                company_fone=cust_fone,
                company_adress="Adresse",
                company_email=cust_email,
            )

        # Envoi d'email APRÈS validation de la transaction
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
            }

            text_body = render_to_string("emails/account_created.txt", email_context)

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[cust_email],
            )

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

    except IntegrityError:
        messages.error(request, "Impossible de créer le compte : doublon détecté.")
        return render(request, "clients/add_clients.html", context)

    except Exception as e:
        messages.error(request, f"Erreur lors de la création : {e}")
        return render(request, "clients/add_clients.html", context)       