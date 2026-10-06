from django.contrib import admin

from .models import TelechargementFinCompta


@admin.register(TelechargementFinCompta)
class TelechargementFinComptaAdmin(admin.ModelAdmin):
    list_display = ("date", "version", "fichier", "adresse_ip")
    list_filter = ("version",)
    date_hierarchy = "date"
