#info/utils.py
from django.shortcuts import get_object_or_404
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
)

def generate_password(length: int=8) -> str:
    alphabet = string.ascii_letters + string.digits  # a-zA-Z0-9
    return "".join(secrets.choice(alphabet) for _ in range(length))

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