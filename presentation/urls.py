from django.urls import path
from . import views

app_name = "presentation"
urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("details-comptabilite", views.detail_module, {"slug": "comptabilite"}, name="details-comptabilite"),
    path("details-tresorerie", views.detail_module, {"slug": "tresorerie"}, name="details_tresorerie"),
    path("details-facturation-crm", views.detail_module, {"slug": "facturation"}, name="detail_facturation_crm"),
    path("details-crm", views.detail_module, {"slug": "crm"}, name="detail_crm"),
    path("details-grh", views.detail_module, {"slug": "grh"}, name="details_grh"),
    path("details-paies", views.detail_module, {"slug": "paie"}, name="details_paies"),
    path("details-etats", views.detail_module, {"slug": "etats"}, name="details_etats_financiers"),
    path("details-budget", views.detail_module, {"slug": "budget"}, name="details_budget"),
    path("details-audit", views.detail_module, {"slug": "audit"}, name="details_audit"),
    path("details-prospection", views.detail_module, {"slug": "prospection"}, name="details_prospection"),
]
