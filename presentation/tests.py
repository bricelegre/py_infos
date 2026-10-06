import hashlib
import shutil
import tempfile
from datetime import date
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import TelechargementFinCompta


class InstallationFinComptaTests(TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dossier)
        reglages = override_settings(FINCOMPTA_DOWNLOAD_DIR=str(self.dossier), FINCOMPTA_SITE_URL="")
        reglages.enable()
        self.addCleanup(reglages.disable)

    def deposer(self, nom, contenu=b"MZ"):
        (self.dossier / nom).write_bytes(contenu)

    def test_page_sans_version_publiee(self):
        reponse = self.client.get(reverse("presentation:telecharger_fincompta"))
        self.assertContains(reponse, "disponible au téléchargement très prochainement")
        self.assertEqual(self.client.get(reverse("presentation:fincompta_manifeste")).status_code, 404)

    def test_manifeste_derniere_version(self):
        self.deposer("FinCompta-Setup-1.9.0.exe")
        self.deposer("FinCompta-Setup-1.10.0.exe", b"MZ derniere")
        self.deposer("autre.exe")
        reponse = self.client.get(reverse("presentation:fincompta_manifeste"))
        contenu = reponse.content.decode()
        self.assertIn("version=1.10.0\r\n", contenu)
        self.assertIn("url=http://testserver/telecharger/fincompta/FinCompta-Setup-1.10.0.exe\r\n", contenu)
        self.assertIn(f"sha256={hashlib.sha256(b'MZ derniere').hexdigest()}\r\n", contenu)

    @override_settings(FINCOMPTA_SITE_URL="https://infos.fincompta.net/")
    def test_liens_absolus_avec_adresse_publique(self):
        self.deposer("FinCompta-Setup-2.0.0.exe")
        manifeste = self.client.get(reverse("presentation:fincompta_manifeste")).content.decode()
        self.assertIn("url=https://infos.fincompta.net/telecharger/fincompta/FinCompta-Setup-2.0.0.exe", manifeste)
        script = self.client.get(reverse("presentation:fincompta_script")).content.decode()
        self.assertIn("'https://infos.fincompta.net/telecharger/fincompta/derniere-version.ini'", script)

    def test_page_sans_installateur_en_ligne(self):
        self.deposer("FinCompta-Setup-1.2.3.exe")
        self.deposer("FinCompta-Installateur.exe")
        reponse = self.client.get(reverse("presentation:telecharger_fincompta"))
        self.assertContains(reponse, "Télécharger FinCompta 1.2.3")
        self.assertContains(reponse, "/telecharger/fincompta/demo")
        self.assertContains(reponse, "irm http://testserver/telecharger/fincompta/installer.ps1 | iex")
        self.assertNotContains(reponse, "Installateur")
        self.assertNotContains(reponse, "installateur")
        self.assertNotContains(reponse, "disponible au téléchargement très prochainement")

    def test_lien_demo_derniere_version(self):
        self.assertEqual(self.client.get(reverse("presentation:fincompta_demo")).status_code, 404)
        self.deposer("FinCompta-Setup-1.1.0.exe", b"MZ ancienne")
        self.deposer("FinCompta-Setup-1.1.1.exe", b"MZ derniere")
        reponse = self.client.get("/telecharger/fincompta/demo")
        self.assertEqual(b"".join(reponse.streaming_content), b"MZ derniere")
        self.assertIn('filename="FinCompta-Setup-1.1.1.exe"', reponse["Content-Disposition"])

    def test_telechargement_fichiers(self):
        self.deposer("FinCompta-Installateur.exe", b"MZ installateur")
        reponse = self.client.get(reverse("presentation:fincompta_fichier", args=["FinCompta-Installateur.exe"]))
        self.assertEqual(b"".join(reponse.streaming_content), b"MZ installateur")
        self.assertIn("attachment", reponse["Content-Disposition"])
        self.deposer("secret.txt")
        for nom in ["secret.txt", "FinCompta-Setup-9.9.9.exe", "..%2Fsettings.py"]:
            reponse = self.client.get(f"/telecharger/fincompta/{nom}")
            self.assertEqual(reponse.status_code, 404, nom)

    def test_compteur_de_telechargements(self):
        self.deposer("FinCompta-Setup-1.0.0.exe")
        self.client.get(reverse("presentation:fincompta_fichier", args=["FinCompta-Setup-1.0.0.exe"]))
        self.deposer("FinCompta-Setup-1.1.0.exe")
        self.client.get(reverse("presentation:fincompta_demo"))
        self.client.get(reverse("presentation:fincompta_demo"))
        self.client.get(reverse("presentation:fincompta_demo"), HTTP_USER_AGENT="Googlebot/2.1")
        self.deposer("FinCompta-Installateur.exe")
        self.client.get(reverse("presentation:fincompta_fichier", args=["FinCompta-Installateur.exe"]))
        self.assertEqual(
            list(TelechargementFinCompta.objects.order_by("date").values_list("version", flat=True)),
            ["1.0.0", "1.1.0", "1.1.0"],
        )

    def test_compteur_visible_uniquement_par_les_superusers(self):
        self.deposer("FinCompta-Setup-1.1.0.exe")
        self.client.get(reverse("presentation:fincompta_demo"))
        url = reverse("presentation:telecharger_fincompta")
        self.assertNotContains(self.client.get(url), "compteur-telechargements")

        User = get_user_model()
        self.client.force_login(User.objects.create_user("employe", password="x", is_staff=True))
        self.assertNotContains(self.client.get(url), "compteur-telechargements")

        self.client.force_login(User.objects.create_superuser("chef", password="x"))
        reponse = self.client.get(url)
        self.assertContains(reponse, "compteur-telechargements")
        self.assertContains(reponse, "Total : <strong>1</strong>", html=False)
        self.assertContains(reponse, "Version 1.1.0 : <strong>1</strong>", html=False)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class LicenceFinComptaTests(TestCase):
    url = "/telecharger-fincompta"

    def test_promotion_jusqu_au_31_decembre(self):
        with mock.patch("presentation.views.timezone.localdate", return_value=date(2026, 12, 31)):
            reponse = self.client.get(self.url)
        self.assertContains(reponse, "100\u202f000 FCFA")
        self.assertContains(reponse, "150\u202f000 FCFA")
        self.assertContains(reponse, "31 décembre 2026")
        self.assertContains(reponse, "Application › Licence")

    def test_aide_blocage_windows(self):
        # Ancre citée par le message d'erreur de FinCompta-Installateur.exe (fincompta_pc)
        self.assertContains(self.client.get(self.url), 'id="blocage-windows"')

    def test_prix_normal_apres_la_promotion(self):
        with mock.patch("presentation.views.timezone.localdate", return_value=date(2027, 1, 1)):
            reponse = self.client.get(self.url)
        self.assertContains(reponse, "150\u202f000 FCFA")
        self.assertNotContains(reponse, "100\u202f000 FCFA")

    def test_demande_de_cle(self):
        reponse = self.client.post(self.url, {
            "titulaire": "SARL Exemple", "name": "Awa", "email": "awa@exemple.ci", "phone": "0102030405",
        }, follow=True)
        self.assertContains(reponse, "Votre demande de clé a été envoyée")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("SARL Exemple", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].reply_to, ["awa@exemple.ci"])

    def test_demande_de_cle_incomplete(self):
        reponse = self.client.post(self.url, {"titulaire": "", "email": "awa@exemple.ci"}, follow=True)
        self.assertContains(reponse, "Une erreur est survenue")
        self.assertEqual(len(mail.outbox), 0)
