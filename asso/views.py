from django.shortcuts import render, redirect
from asso.models import Customer as AssoCustomer, Users as AssoUsers, UserRole as AssoUserRole, CompanyData as AssoCompanyData
from django.utils import timezone
from .utils import *
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from slugify import slugify
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
    cust_slug = slugify(cust_identifiant)

    user_password = None
    email_sent = False
    email_err = None

    try:
        # --- 1) DB transaction ---
        with transaction.atomic():
            q = Q(cust_identifiant=cust_identifiant)
            if cust_email:
                q |= Q(cust_email__iexact=cust_email)

            if AssoCustomer.objects.filter(q).exists():
                messages.error(request, "Identifiant ou email déjà utilisé.")
                return redirect("asso:ajouter_asso")

            cust_end_subscription = timezone.now().date() + relativedelta(months=1)

            customer = AssoCustomer.objects.create(
                cust_identifiant=cust_identifiant,
                cust_company_name=cust_company_name,
                cust_email=cust_email,
                cust_fone=cust_fone,
                cust_plan=cust_plan,
                cust_end_subscription=cust_end_subscription,
                cust_slug=cust_slug,
                cust_status=1,
            )
            cust_id = customer.cust_id
            initialize_customer_data_asso(cust_id)

            user_password = generate_password(8)
            user_password_hashed = make_password(user_password)

            user_created = AssoUsers.objects.create(
                user_pseudo=user_pseudo,
                user_password=user_password_hashed,
                cust_id=cust_id,
                user_email=cust_email
            )
            user_id = user_created.user_id

            roles = {
                'accounting': 'manager_comptable',
                'employees': 'rh_manager',
                'pay': 'paie_manager',
                'sales': 'manager_ventes',
                'taxation': 'utilisateur_impots',
                'users': 'manager_utilisateur',
                'administration': 'app_admin',
            }

            user_roles = []
            for module_key, role_name in roles.items():
                role_id = get_role_id_by_name(role_name)
                module_id = get_module_id_by_key(module_key)
                if role_id and module_id:
                    user_roles.append(
                        AssoUserRole(user_id=user_id, roles_id=role_id, module_id=module_id)
                    )

            if user_roles:
                AssoUserRole.objects.bulk_create(user_roles)

            AssoCompanyData.objects.create(
                cust_id=cust_id,
                company_name=cust_company_name,
                company_fone=cust_fone,
                company_adress="Adresse",
                
                company_email=cust_email,
            )

        # --- 2) Email AFTER commit ---
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

    except Exception as e:
        messages.error(request, f"Erreur lors de la création : {e}")
        return redirect("asso:ajouter_asso")
