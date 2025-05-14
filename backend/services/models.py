from typing import Any
from django.db import models
from django.utils import timezone
from datetime import timedelta


class RegistrationTokenModel(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    password_hash = models.CharField(max_length=128)
    token = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Registration Token"
        verbose_name_plural = "Registration Tokens"
