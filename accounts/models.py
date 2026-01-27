from django.conf import settings
from django.db import models

class DealerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dealer_profile")
    display_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.display_name or self.user.username
