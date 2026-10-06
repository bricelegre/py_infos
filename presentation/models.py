from django.db import models


class TelechargementFinCompta(models.Model):
    """Un téléchargement du programme d'installation de FinCompta (version Windows)."""

    version = models.CharField(max_length=30, db_index=True)
    fichier = models.CharField(max_length=120)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "téléchargement de FinCompta"
        verbose_name_plural = "téléchargements de FinCompta"

    def __str__(self):
        return f"{self.fichier} - {self.date:%d/%m/%Y %H:%M}"
