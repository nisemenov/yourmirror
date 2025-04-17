import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import post_save
from django.dispatch import receiver


class ProfileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    telegram_id = models.CharField(verbose_name="telegram ID", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<ProfileModel {self.user}>"


class FollowModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "following"]

    def __str__(self):
        return f"<FollowModel {self.pk}>"


@staticmethod
@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created: bool, **kwargs):
    if created:
        profile_kwargs = {}

        profile = ProfileModel(user=instance, **profile_kwargs)
        profile.save()
