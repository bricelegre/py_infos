from django.contrib import admin

from . import telechargement
from .models import TelechargementFinCompta

admin.site.site_header = "Administration FinCompta"
admin.site.site_title = "Administration FinCompta"


@admin.register(TelechargementFinCompta)
class TelechargementFinComptaAdmin(admin.ModelAdmin):
    """Compteur des téléchargements de FinCompta, réservé aux superadministrateurs."""

    change_list_template = "admin/presentation/telechargementfincompta/change_list.html"
    list_display = ("date", "version", "fichier", "adresse_ip")
    list_filter = ("version",)
    date_hierarchy = "date"

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["stats_telechargements"] = telechargement.statistiques_telechargements(
            telechargement.derniere_version())
        return super().changelist_view(request, extra_context=extra_context)
