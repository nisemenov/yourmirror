import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    telegram_id = models.CharField(verbose_name="telegram ID", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def followers(self):
        return ProfileModel.objects.filter(follower_profiles__following=self)  # pyright: ignore[reportAttributeAccessIssue]

    @property
    def following(self):
        return ProfileModel.objects.filter(following_profiles__follower=self).order_by(
            "user__first_name"
        )  # pyright: ignore[reportAttributeAccessIssue]

    def is_following(self, other_profile):
        return FollowModel.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
            follower=self, following=other_profile
        ).exists()

    @property
    def wishitems_public(self):
        return self.wishitems.filter(is_private=False)  # pyright: ignore[reportAttributeAccessIssue]

    def __str__(self):
        return f"<ProfileModel {self.user.username} / {self.user.first_name}>"


class FollowModel(models.Model):
    follower = models.ForeignKey(
        ProfileModel,
        on_delete=models.CASCADE,
        related_name="follower_profiles",
    )
    following = models.ForeignKey(
        ProfileModel,
        on_delete=models.CASCADE,
        related_name="following_profiles",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["follower", "following"]

    def save(self, *args, **kwargs):
        if self.follower == self.following:
            raise ValueError("User can't follow themselves")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"<FollowModel {self.follower.user.username} → {self.following.user.username}>"  # pyright: ignore[reportAttributeAccessIssue]


@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created: bool, **kwargs):
    if created:
        profile_kwargs = {}

        profile = ProfileModel(user=instance, **profile_kwargs)
        profile.save()
