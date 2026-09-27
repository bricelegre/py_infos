#clients/utils.py
from django.shortcuts import get_object_or_404, redirect
from functools import wraps
from asso.models import Customer
import secrets
import string


def get_customer_asso(cust_id):
    return get_object_or_404(Customer, cust_id=cust_id)

def generate_password(length: int=8) -> str:
    alphabet = string.ascii_letters + string.digits  # a-zA-Z0-9
    return "".join(secrets.choice(alphabet) for _ in range(length))

def login_required_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            return redirect('login_admin')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required_admin_principal(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_code' not in request.session:
            return redirect('login_admin')
        elif request.session['admin_code'] != '1':
            return redirect('login_admin')
        return view_func(request, *args, **kwargs)
    return wrapper

