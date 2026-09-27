from datetime import date
from unittest import mock

from dateutil.relativedelta import relativedelta
from django.core import mail
from django.test import TestCase, override_settings


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AddAssoTests(TestCase):
    URL = "/creer-votre-compte-association/"
    DONNEES = {"user_pseudo": "admin", "cust_identifiant": "ASSO1", "cust_company_name": "",
               "cust_email": "bureau@asso1.org", "cust_fone": "0102030405"}

    @mock.patch("asso.views.provision")
    def test_creation_par_l_api_syscebnl_puis_email(self, provision_mock):
        provision_mock.return_value = mock.Mock(ok=True)
        r = self.client.post(self.URL, self.DONNEES)
        self.assertRedirects(r, self.URL, fetch_redirect_response=False)
        product, payload = provision_mock.call_args.args
        self.assertEqual(product, "syscebnl")
        self.assertEqual(payload["plan"], 3)
        self.assertEqual(payload["nom"], "ASSO1")  # nom facultatif : identifiant par défaut
        self.assertEqual(payload["fin_abonnement"], (date.today() + relativedelta(months=1)).isoformat())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(payload["password"], mail.outbox[0].body)

    @mock.patch("asso.views.provision")
    def test_erreur_api_sans_email(self, provision_mock):
        provision_mock.return_value = mock.Mock(ok=False, error="L'identifiant « ASSO1 » est déjà utilisé.")
        r = self.client.post(self.URL, self.DONNEES, follow=True)
        self.assertContains(r, "déjà utilisé")
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch("asso.views.provision")
    def test_pseudo_et_identifiant_obligatoires(self, provision_mock):
        self.client.post(self.URL, dict(self.DONNEES, user_pseudo=""))
        provision_mock.assert_not_called()
