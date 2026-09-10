"""
info/sitemaps.py

Sitemap XML du site infos.fincompta.net.
Basé sur le framework django.contrib.sitemaps.

Documentation : https://docs.djangoproject.com/en/5.2/ref/contrib/sitemaps/
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Sitemap pour les pages "vitrine" statiques de l'app `presentation`.
    Ce sont des pages publiques, sans paramètre, destinées à être indexées.
    """
    priority = 0.8
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        # Noms des URL définis dans presentation/urls.py
        return [
            "presentation:accueil",
            "presentation:details-comptabilite",
            "presentation:details_grh",
            "presentation:details_etats_financiers",
            "presentation:details_paies",
            "presentation:detail_facturation_crm",
            "presentation:detail_crm",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # La page d'accueil a une priorité plus forte
        return 1.0 if item == "presentation:accueil" else 0.8


# Dictionnaire des sitemaps à enregistrer dans urls.py
sitemaps = {
    "static": StaticViewSitemap,
}

# NOTE :
# Les pages "asso:ajouter_asso" et "clients:ajouter_client" sont des
# formulaires d'inscription (POST) et/ou nécessitent un paramètre
# dynamique (cust_plan_text). Elles ne sont volontairement PAS incluses
# dans le sitemap : elles n'ont pas vocation à être indexées telles quelles.
# Si vous souhaitez indexer une page de vente par plan (ex: /creer-votre-compte-entreprise/pro/),
# vous pouvez ajouter un second Sitemap listant les slugs de plans connus.