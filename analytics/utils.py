# analytics/utils.py

import re
import ipaddress
import requests
from .models import Visitor


BOT_PATTERNS = [
    r"bot",
    r"crawl",
    r"crawler",
    r"spider",
    r"slurp",
    r"search",
    r"archiver",
    r"transcoder",
    r"preview",
    r"scanner",
    r"python-requests",
    r"curl",
    r"wget",
    r"httpclient",
    r"facebookexternalhit",
    r"linkedinbot",
    r"whatsapp",
    r"telegrambot",
    r"discordbot",
    r"googlebot",
    r"bingbot",
    r"yandex",
    r"duckduckbot",
    r"baiduspider",
    r"oai-searchbot",
    r"chatgpt-user",
    r"facebookbot",
]

EXCLUDED_PATH_PREFIXES = [
    "/static/",
    "/media/",
    "/admin/",
]

EXCLUDED_EXACT_PATHS = [
    "/robots.txt",
    "/favicon.ico",
]


def get_client_ip(request):
    """
    Récupère l'IP réelle du client en tenant compte d'un proxy éventuel.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    x_real_ip = request.META.get("HTTP_X_REAL_IP")

    if x_forwarded_for:
        # Premier IP = client réel
        return x_forwarded_for.split(",")[0].strip()

    if x_real_ip:
        return x_real_ip.strip()

    return request.META.get("REMOTE_ADDR", "")


def is_excluded_path(path):
    """
    Ignore les URLs techniques ou non pertinentes pour les stats.
    """
    if not path:
        return True

    if path in EXCLUDED_EXACT_PATHS:
        return True

    for prefix in EXCLUDED_PATH_PREFIXES:
        if path.startswith(prefix):
            return True

    return False


def detect_bot(user_agent):
    """
    Détecte si le user-agent ressemble à un bot/crawler.
    Retourne (is_bot, bot_name).
    """
    if not user_agent:
        return False, None

    ua = user_agent.lower()

    for pattern in BOT_PATTERNS:
        if re.search(pattern, ua):
            return True, pattern

    return False, None


def get_device_type_from_user_agent_string(user_agent):
    """
    Détection simple du type d'appareil à partir de la chaîne user-agent.
    """
    ua = (user_agent or "").lower()

    if "ipad" in ua or "tablet" in ua:
        return "tablette"

    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return "mobile"

    return "pc"


def get_device_infos(request):
    """
    Utilise request.user_agent si disponible, sinon fallback manuel.
    Retourne: device_type, browser, os
    """
    user_agent_string = request.META.get("HTTP_USER_AGENT", "")

    ua = getattr(request, "user_agent", None)

    if ua:
        device_type = (
            "mobile" if ua.is_mobile else
            "tablette" if ua.is_tablet else
            "pc"
        )
        browser = getattr(ua.browser, "family", "") or ""
        os_name = getattr(ua.os, "family", "") or ""
        return device_type, browser, os_name

    # fallback sans django-user-agents
    return (
        get_device_type_from_user_agent_string(user_agent_string),
        "",
        "",
    )


def is_local_or_private_ip(ip_address):
    """
    Vérifie si l'IP est locale, privée, loopback, réservée, etc.
    """
    if not ip_address:
        return True

    try:
        ip_obj = ipaddress.ip_address(ip_address)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_reserved
            or ip_obj.is_link_local
        )
    except ValueError:
        return True


def get_country_from_ip(ip_address):
    """
    Récupère le pays à partir de l'IP.
    Retourne 'Local' pour les IP privées/locales.
    """
    if not ip_address:
        return ""

    if is_local_or_private_ip(ip_address):
        return "Local"

    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=status,country"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            return data.get("country", "")
    except Exception:
        pass

    return ""


def track_visitor(request):
    """
    Enregistre une visite utile pour le site.
    Ignore:
    - requêtes non GET
    - paths techniques
    """
    if request.method != "GET":
        return None

    path = request.path or "/"

    if is_excluded_path(path):
        return None

    ip = get_client_ip(request)
    user_agent_string = request.META.get("HTTP_USER_AGENT", "")
    is_bot, bot_name = detect_bot(user_agent_string)
    device_type, browser, os_name = get_device_infos(request)

    # Option 1 : on enregistre aussi les bots
    visitor = Visitor.objects.create(
        ip_address=ip,
        path=path,
        country=get_country_from_ip(ip) if ip else "",
        device_type=device_type,
        browser=browser,
        os=os_name,
        user_agent=user_agent_string,
        is_bot=is_bot,
        bot_name=bot_name,
    )

    return visitor