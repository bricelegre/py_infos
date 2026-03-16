from django.urls import path
from . import views

app_name = "presentation"
urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("details-comptabilite", views.detail_comptabilite, name="details-comptabilite"),
    path("details-grh", views.detail_grh, name="details_grh"),
    path("details-etats", views.detail_etats_financiers, name="details_etats_financiers"),
    path("details-paies", views.detail_paies, name="details_paies"),
    path("details-facturation-crm", views.detail_facturation_crm, name="detail_facturation_crm"),
    path("details-crm", views.detail_crm, name="detail_crm")
]