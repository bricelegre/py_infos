#erpadmin/utils.py

from django.shortcuts import get_object_or_404, redirect
from functools import wraps
from django.db.models import OuterRef, Subquery
from clients.models import *
import secrets
import string

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