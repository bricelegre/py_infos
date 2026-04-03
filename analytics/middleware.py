# analytics/middleware.py
from user_agents import parse

from .models import Visitor
from .utils import get_client_ip, is_excluded_path, detect_bot


class VisitorTrackingMiddleware:
    """
    Middleware orienté 'site public':
    - ignore robots.txt, favicon, static, media, admin
    - détecte les bots
    - enregistre seulement les requêtes GET
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            if request.method != "GET":
                return response

            path = request.path or "/"

            if is_excluded_path(path):
                return response

            user_agent = request.META.get("HTTP_USER_AGENT", "")
            is_bot, bot_name = detect_bot(user_agent)

            ua = parse(user_agent)

            if not request.session.session_key:
                request.session.save()

            Visitor.objects.create(
                ip_address=get_client_ip(request),
                path=path,
                method=request.method,
                user_agent=user_agent,
                referer=request.META.get("HTTP_REFERER"),
                device_type=(
                    "mobile" if ua.is_mobile else
                    "tablet" if ua.is_tablet else
                    "pc"
                ),
                browser=f"{ua.browser.family} {ua.browser.version_string}".strip(),
                os=f"{ua.os.family} {ua.os.version_string}".strip(),
                is_bot=is_bot,
                bot_name=bot_name,
                session_key=request.session.session_key,
            )

        except Exception:
            # on ne bloque jamais l'application à cause du tracking
            pass

        return response