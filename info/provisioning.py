# info/provisioning.py
"""Client de l'API de création de compte (POST /api/provision/) de fincompta
et de syscebnl.

Le site ne crée plus les comptes en écrivant dans les bases des applications :
l'application cible crée et initialise elle-même le client (fiche société,
plan comptable, journaux, paramètres de paie, administrateur et rôles) en une
seule transaction.

Chaque appel est signé : X-Provision-Signature = "sha256=" + HMAC-SHA256(secret,
"<timestamp>.<corps JSON>"), avec X-Provision-Timestamp = heure courante en
secondes ; le serveur refuse une signature de plus de 5 minutes.
"""
import hashlib
import hmac
import json
import logging
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 30  # secondes : la création copie tout un plan comptable

# Message affiché quand le problème vient de la configuration (URL, secret,
# horloge) : le détail part dans les journaux, pas à l'écran.
INDISPONIBLE = "La création de compte est momentanément indisponible. Réessayez plus tard."


@dataclass
class ProvisioningResult:
    ok: bool
    status: int = 0          # code HTTP, 0 si le service est injoignable
    data: dict = None        # réponse JSON de l'API
    error: str = ""          # message affichable
    field: str = None        # champ en cause ("identifiant", "email", ...)


def _signature(secret, timestamp, body):
    return "sha256=" + hmac.new(secret.encode(), timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()


def provision(product, payload):
    """Crée le compte dans ``product`` ("fincompta" ou "syscebnl")."""
    conf = settings.PROVISIONING.get(product) or {}
    url, secret = conf.get("url"), conf.get("secret")
    if not url or not secret:
        logger.error("Création de compte %s : URL ou secret non configuré", product)
        return ProvisioningResult(ok=False, error=INDISPONIBLE)

    body = json.dumps(payload).encode()
    timestamp = str(int(time.time()))
    request = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Provision-Timestamp": timestamp,
        "X-Provision-Signature": _signature(secret, timestamp, body),
    })
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            status, raw = response.status, response.read()
    except urllib.error.HTTPError as exc:
        status, raw = exc.code, exc.read()
    except (urllib.error.URLError, OSError) as exc:
        logger.error("Création de compte %s : service injoignable (%s)", product, exc)
        return ProvisioningResult(ok=False, error=INDISPONIBLE)

    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError
    except ValueError:
        logger.error("Création de compte %s : réponse inattendue (HTTP %s)", product, status)
        return ProvisioningResult(ok=False, status=status, error=INDISPONIBLE)

    if status == 201 and data.get("ok"):
        return ProvisioningResult(ok=True, status=status, data=data)
    if status in (400, 409):
        return ProvisioningResult(ok=False, status=status, data=data,
                                  error=data.get("error") or "Données invalides.", field=data.get("field"))
    logger.error("Création de compte %s refusée (HTTP %s) : %s", product, status, data.get("error"))
    return ProvisioningResult(ok=False, status=status, data=data, error=INDISPONIBLE)
