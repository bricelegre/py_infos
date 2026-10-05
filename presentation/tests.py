import hashlib
import shutil
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings
from django.urls import reverse


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
        self.assertContains(reponse, "disponible très prochainement")
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

    def test_page_avec_installateur(self):
        self.deposer("FinCompta-Setup-1.2.3.exe")
        self.deposer("FinCompta-Installateur.exe")
        reponse = self.client.get(reverse("presentation:telecharger_fincompta"))
        self.assertContains(reponse, "Installer FinCompta 1.2.3")
        self.assertContains(reponse, "/telecharger/fincompta/FinCompta-Installateur.exe")
        self.assertContains(reponse, "irm http://testserver/telecharger/fincompta/installer.ps1 | iex")

    def test_telechargement_fichiers(self):
        self.deposer("FinCompta-Installateur.exe", b"MZ installateur")
        reponse = self.client.get(reverse("presentation:fincompta_fichier", args=["FinCompta-Installateur.exe"]))
        self.assertEqual(b"".join(reponse.streaming_content), b"MZ installateur")
        self.assertIn("attachment", reponse["Content-Disposition"])
        self.deposer("secret.txt")
        for nom in ["secret.txt", "FinCompta-Setup-9.9.9.exe", "..%2Fsettings.py"]:
            reponse = self.client.get(f"/telecharger/fincompta/{nom}")
            self.assertEqual(reponse.status_code, 404, nom)
