import hashlib
import hmac
import io
import json
import time
import urllib.error
from datetime import date
from unittest import mock

from dateutil.relativedelta import relativedelta
from django.core import mail
from django.test import TestCase, override_settings

from info.provisioning import INDISPONIBLE, provision

PROVISIONING = {
    "fincompta": {"url": "https://fincompta.test/api/provision/", "secret": "secret-fin"},
    "syscebnl": {"url": "https://asso.test/api/provision/", "secret": "secret-asso"},
}


class FakeResponse(io.BytesIO):
    def __init__(self, status, data):
        super().__init__(json.dumps(data).encode())
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(status, data):
    return urllib.error.HTTPError("https://fincompta.test/api/provision/", status, "", {},
                                  io.BytesIO(json.dumps(data).encode()))


CREE = FakeResponse(201, {"ok": True, "cust_id": 7, "identifiant": "ACME", "pseudo": "admin"})


@override_settings(PROVISIONING=PROVISIONING)
class ProvisioningClientTests(TestCase):

    @mock.patch("info.provisioning.urllib.request.urlopen", return_value=CREE)
    def test_appel_signe_comme_l_attend_le_serveur(self, urlopen):
        result = provision("fincompta", {"identifiant": "ACME"})
        self.assertTrue(result.ok)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, PROVISIONING["fincompta"]["url"])
        ts = request.get_header("X-provision-timestamp")
        self.assertLess(abs(time.time() - int(ts)), 5)
        attendu = "sha256=" + hmac.new(b"secret-fin", ts.encode() + b"." + request.data, hashlib.sha256).hexdigest()
        self.assertEqual(request.get_header("X-provision-signature"), attendu)
        self.assertEqual(json.loads(request.data), {"identifiant": "ACME"})

    @mock.patch("info.provisioning.urllib.request.urlopen")
    def test_erreur_metier_affichee(self, urlopen):
        urlopen.side_effect = http_error(409, {"ok": False, "error": "L'identifiant « ACME » est déjà utilisé.",
                                               "field": "identifiant"})
        result = provision("fincompta", {})
        self.assertFalse(result.ok)
        self.assertEqual((result.status, result.field), (409, "identifiant"))
        self.assertIn("déjà utilisé", result.error)

    @mock.patch("info.provisioning.urllib.request.urlopen")
    def test_erreur_de_configuration_masquee(self, urlopen):
        urlopen.side_effect = http_error(401, {"ok": False, "error": "Signature invalide ou expirée."})
        with self.assertLogs("info.provisioning", "ERROR"):
            result = provision("fincompta", {})
        self.assertEqual((result.ok, result.error), (False, INDISPONIBLE))

    @mock.patch("info.provisioning.urllib.request.urlopen", side_effect=urllib.error.URLError("refused"))
    def test_service_injoignable(self, urlopen):
        with self.assertLogs("info.provisioning", "ERROR"):
            result = provision("fincompta", {})
        self.assertEqual((result.ok, result.status, result.error), (False, 0, INDISPONIBLE))

    @mock.patch("info.provisioning.urllib.request.urlopen")
    def test_secret_absent_aucun_appel(self, urlopen):
        with self.settings(PROVISIONING={"fincompta": {"url": "https://x/", "secret": ""}}):
            with self.assertLogs("info.provisioning", "ERROR"):
                result = provision("fincompta", {})
        self.assertFalse(result.ok)
        urlopen.assert_not_called()


@override_settings(PROVISIONING=PROVISIONING, EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AddClientTests(TestCase):
    URL = "/creer-votre-compte-entreprise/premium/"
    DONNEES = {"user_pseudo": "admin", "cust_identifiant": "ACME", "cust_company_name": "Acme SARL",
               "cust_email": "Contact@Acme.ci", "cust_fone": "0102030405"}

    @mock.patch("clients.views.provision")
    def test_creation_par_l_api_puis_email(self, provision_mock):
        provision_mock.return_value = mock.Mock(ok=True)
        r = self.client.post(self.URL, self.DONNEES)
        self.assertRedirects(r, self.URL, fetch_redirect_response=False)
        product, payload = provision_mock.call_args.args
        self.assertEqual(product, "fincompta")
        self.assertEqual(payload["plan"], 3)
        self.assertEqual(payload["email"], "contact@acme.ci")
        self.assertEqual(payload["fin_abonnement"], (date.today() + relativedelta(months=1)).isoformat())
        self.assertEqual(len(payload["password"]), 8)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(payload["password"], mail.outbox[0].body)

    @mock.patch("clients.views.provision")
    def test_erreur_api_sans_email(self, provision_mock):
        provision_mock.return_value = mock.Mock(ok=False, error="L'adresse « contact@acme.ci » est déjà utilisée.")
        r = self.client.post(self.URL, self.DONNEES)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "déjà utilisée")
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch("clients.views.provision")
    def test_champs_obligatoires_sans_appel(self, provision_mock):
        r = self.client.post(self.URL, dict(self.DONNEES, cust_email=""))
        self.assertContains(r, "Veuillez renseigner tous les champs obligatoires.")
        provision_mock.assert_not_called()

    def test_plan_inconnu(self):
        r = self.client.get("/creer-votre-compte-entreprise/gold/")
        self.assertEqual(r.status_code, 302)
