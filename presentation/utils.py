import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def send_demo_request(request):

    name = (request.POST.get("name") or "").strip()
    subject = (request.POST.get("subject") or "").strip()
    message = (request.POST.get("message") or "").strip()
    email = (request.POST.get("email") or "").strip().lower()
    phone = (request.POST.get("phone") or "").strip()

    # anti spam honeypot
    honeypot = request.POST.get("website")
    if honeypot:
        return False, "spam"

    if not email or not message:
        return False, "missing_fields"

    context = {
        "name": name,
        "subject": subject,
        "message": message,
        "phone": phone,
        "email": email,
    }

    try:

        text_body = render_to_string("emails/demo_demand.txt", context)

        email_to_send = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["infos@erpmfr.net"],
            reply_to=[email],
        )

        email_to_send.send()

        return True, None

    except Exception as e:

        logger.error(f"Erreur envoi email démo : {str(e)}")

        return False, str(e)


def send_contact_request(request):
    
    name = (request.POST.get("name") or "").strip()
    subject = (request.POST.get("subject") or "").strip()
    phone = (request.POST.get("phone") or "").strip()
    message = (request.POST.get("message") or "").strip()
    email = (request.POST.get("email") or "").strip().lower()
    plan = (request.POST.get("plan") or "").strip()
    org_type = (request.POST.get("org_type") or "").strip()
    
    # anti spam honeypot
    honeypot = request.POST.get("website")
    if honeypot:
        return False, "spam"

    if not email or not message:
        return False, "missing_fields"

    context = {
        "name": name,
        "subject": subject,
        "message": message,
        "phone": phone,
        "email": email,
        "plan" : plan,
        "org_type" : org_type,
    }

    try:

        text_body = render_to_string("emails/form_contact.txt", context)

        email_to_send = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["infos@erpmfr.net"],
            reply_to=[email],
        )

        email_to_send.send()

        return True, None

    except Exception as e:

        logger.error(f"Erreur envoi email fiche contact : {str(e)}")

        return False, str(e)