from django.db import models

class Visitor(models.Model):

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=500, db_index=True)
    method = models.CharField(max_length=10, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    referer = models.TextField(blank=True, null=True)

    country = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)

    device_type = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=120, blank=True, null=True)
    os = models.CharField(max_length=120, blank=True, null=True)

    is_bot = models.BooleanField(default=False, db_index=True)
    bot_name = models.CharField(max_length=120, blank=True, null=True)

    session_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.created_at:%d/%m/%Y %H:%M}"