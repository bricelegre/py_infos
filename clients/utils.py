#info/utils.py
from django.shortcuts import get_object_or_404, redirect
from functools import wraps
from django.db.models import OuterRef, Subquery
import secrets
import string
from django.db import transaction
from .models import (
    Customer,
    Users,
    UserRole,
    UserPermission,
    UserAnnouncement,
    UserConnect,
    CustomerConnect,
    CompanyData,
    ExpendType,
    ListJrx,
    ThirdAccount,
    AccountChart,
    PayParameters,
    Roles,
    ExpendTypeTemplate,
    ListJrxTemplate,
    ThirdAccountTemplate,
    AccountChartTemplate,
    AccountsChartAssoTemplate,
    ExpendTypeAssoTemplate,
)

def generate_password(length: int=8) -> str:
    alphabet = string.ascii_letters + string.digits  # a-zA-Z0-9
    return "".join(secrets.choice(alphabet) for _ in range(length))

# --- Fonction utilitaire ---
def get_role_id_by_name(role_name):
    try:
        role = Roles.objects.get(roles_name=role_name)
        return role.roles_id
    except Roles.DoesNotExist:
        print(f"Rôle non trouvé : {role_name}")
        return None

def get_module_id_by_key(module_key):
    module_ids = {
        'accounting': 1,
        'employees': 2,
        'pay': 3,
        'sales': 4,
        'taxation': 5,
        'users': 6
    }
    return module_ids.get(module_key)

def assign_role_to_user(user_id, module_key, role_name):
    module_ids = {
        'accounting': 1,
        'employees': 2,
        'pay': 3,
        'sales': 4,
        'taxation': 5,
        'users': 6
    }

    module_id = module_ids.get(module_key)
    role_id = get_role_id_by_name(role_name)

    if role_id and module_id:
        UserRole.objects.create(
            user_id=user_id,
            roles_id=role_id,
            module_id=module_id
        )
    else:
        print(f"Échec assignation : rôle {role_name} ou module {module_key} invalide.")
        
def copy_expend_types(cust_id):
    templates = ExpendTypeTemplate.objects.all()
    expend_types = [
        ExpendType(
            cust_id=cust_id,
            et_account_nb=t.et_account_nb,
            et_account_name=t.et_account_name
        ) for t in templates
    ]
    ExpendType.objects.bulk_create(expend_types)
    return True

def copy_list_jrx(cust_id):
    templates = ListJrxTemplate.objects.all()
    journals = [
        ListJrx(
            cust_id=cust_id,
            journal_code=t.journal_code,
            journal_name=t.journal_name
        ) for t in templates
    ]
    ListJrx.objects.bulk_create(journals)
    return True

def copy_third_account(cust_id):
    templates = ThirdAccountTemplate.objects.all()
    third_accounts = [
        ThirdAccount(
            cust_id=cust_id,
            third_type=t.third_type,
            third_name=t.third_name
        ) for t in templates
    ]
    ThirdAccount.objects.bulk_create(third_accounts)
    return True

def copy_account_chart(cust_id):
    templates = AccountChartTemplate.objects.all()
    charts = [
        AccountChart(
            cust_id=cust_id,
            acc_account_number=t.acc_account_number,
            acc_account_name=t.acc_account_name,
            acc_class_level_2=t.acc_class_level_2,
            acc_class_level_3=t.acc_class_level_3
        ) for t in templates
    ]
    AccountChart.objects.bulk_create(charts)
    return True

def pay_parameters_init(cust_id):
    PayParameters.objects.get_or_create(
        cust_id=cust_id,
        defaults={
            "pp_cmu": "NON",
            "pp_anciennete": "NON",
            "pp_cnps_tx": 3,
            "pp_pay_rounded": "NON",
        }
    )
    return True

def initialize_customer_data(cust_id):
    
    """
    Initialise les données de base pour un nouveau client :
    - types de dépenses
    - plan comptable
    - tiers
    - journaux
    """
    copy_expend_types(cust_id)
    copy_account_chart(cust_id)
    copy_third_account(cust_id)
    copy_list_jrx(cust_id)
    pay_parameters_init(cust_id)

def copy_account_chart_asso(cust_id):
    templates = AccountsChartAssoTemplate.objects.all()
    charts = [
        AccountChart(
            cust_id=cust_id,
            acc_account_number=t.number,
            acc_account_name=t.name
        ) for t in templates
    ]
    AccountChart.objects.bulk_create(charts)
    return True


def copy_expend_types_asso(cust_id):
    templates = ExpendTypeAssoTemplate.objects.all()
    expend_types = [
        ExpendType(
            cust_id=cust_id,
            et_account_nb=t.et_account_nb,
            et_account_name=t.et_account_name
        ) for t in templates
    ]
    ExpendType.objects.bulk_create(expend_types)
    return True

def initialize_customer_data_asso(cust_id):
    """
    Initialise les données de base pour un nouveau client :
    - types de dépenses
    - plan comptable
    - tiers
    - journaux
    """
    
    copy_expend_types_asso(cust_id)
    copy_account_chart_asso(cust_id)
    copy_third_account(cust_id)
    copy_list_jrx(cust_id)
    pay_parameters_init(cust_id)

def get_customer(cust_id):
    return get_object_or_404(Customer, cust_id=cust_id)

def delete_customer_data(cust_id):
    """
    Supprime un client et les données liées connues dans cette app.
    Retourne un dictionnaire avec le nombre d'éléments supprimés.
    """

    customer = Customer.objects.filter(cust_id=cust_id).first()
    if not customer:
        raise ValueError("Client introuvable.")

    user_ids = list(
        Users.objects.filter(cust_id=cust_id).values_list("user_id", flat=True)
    )

    deleted = {}

    with transaction.atomic():
        # Données liées aux utilisateurs du client
        if user_ids:
            deleted["user_roles"] = UserRole.objects.filter(user_id__in=user_ids).delete()[0]
            deleted["user_permissions"] = UserPermission.objects.filter(user_id__in=user_ids).delete()[0]
            deleted["user_announcements"] = UserAnnouncement.objects.filter(user_id__in=user_ids).delete()[0]
            deleted["user_connects"] = UserConnect.objects.filter(user_id__in=user_ids).delete()[0]
        else:
            deleted["user_roles"] = 0
            deleted["user_permissions"] = 0
            deleted["user_announcements"] = 0
            deleted["user_connects"] = 0

        # Table de connexion client
        deleted["customer_connect"] = CustomerConnect.objects.filter(cust_id=cust_id).delete()[0]

        # Données métier initialisées à la création du client
        deleted["company_data"] = CompanyData.objects.filter(cust_id=cust_id).delete()[0]
        deleted["expend_types"] = ExpendType.objects.filter(cust_id=cust_id).delete()[0]
        deleted["list_jrx"] = ListJrx.objects.filter(cust_id=cust_id).delete()[0]
        deleted["third_accounts"] = ThirdAccount.objects.filter(cust_id=cust_id).delete()[0]
        deleted["account_chart"] = AccountChart.objects.filter(cust_id=cust_id).delete()[0]
        deleted["pay_parameters"] = PayParameters.objects.filter(cust_id=cust_id).delete()[0]

        # Utilisateurs du client
        deleted["users"] = Users.objects.filter(cust_id=cust_id).delete()[0]

        # Client
        deleted["customer"] = Customer.objects.filter(cust_id=cust_id).delete()[0]

    return deleted