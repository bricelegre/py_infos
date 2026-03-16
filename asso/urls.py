from django.urls import path
from . import views

app_name = "asso"

urlpatterns = [
    path('creer-votre-compte-association/', views.add_asso, name='ajouter_asso'),
]