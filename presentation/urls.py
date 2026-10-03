from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "presentation"
urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("details-comptabilite", views.detail_module, {"slug": "comptabilite"}, name="details-comptabilite"),
    path("details-tresorerie", views.detail_module, {"slug": "tresorerie"}, name="details_tresorerie"),
    path("details-facturation-crm", views.detail_module, {"slug": "facturation_crm"},
         name="detail_facturation_crm"),
    # Ancienne page CRM, réunie avec la facturation
    path("details-crm", RedirectView.as_view(pattern_name="presentation:detail_facturation_crm", permanent=True),
         name="detail_crm"),
    path("details-grh", views.detail_module, {"slug": "grh"}, name="details_grh"),
    path("details-paies", views.detail_module, {"slug": "paie"}, name="details_paies"),
    path("details-etats", views.detail_module, {"slug": "etats"}, name="details_etats_financiers"),
    path("details-controle-gestion", views.detail_module, {"slug": "cdg"}, name="details_cdg"),
    # Ancienne page du module Budget, remplacé par le Contrôle de gestion
    path("details-budget", RedirectView.as_view(pattern_name="presentation:details_cdg", permanent=True),
         name="details_budget"),
    path("details-audit", views.detail_module, {"slug": "audit"}, name="details_audit"),
    path("details-prospection", views.detail_module, {"slug": "prospection"}, name="details_prospection"),
    path("details-association", views.detail_module, {"slug": "association"}, name="details_association"),
]
