from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    #path('creer-votre-compte-entreprise/', views.add_client, name='ajouter_client'),
    path('creer-votre-compte-entreprise/<str:cust_plan_text>/', views.add_client, name='ajouter_client'),
]
