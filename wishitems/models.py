import uuid

from django.urls import reverse
from django.db import models


from profiles.models import ProfileModel


def upload_to_wishlist(instance, filename):
    ext = filename.split(".")[-1]
    return f"wishitems/picture/{uuid.uuid4()}.{ext}"


class WishItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    picture = models.ImageField(upload_to=upload_to_wishlist, blank=True, null=True)

    profile = models.ForeignKey(
        ProfileModel,
        on_delete=models.CASCADE,
        related_name="wishitems",
    )

    reserved = models.ForeignKey(
        ProfileModel, on_delete=models.SET_NULL, blank=True, null=True
    )
    reserved_at = models.DateTimeField(auto_now=True)

    is_private = models.BooleanField(default=False)  # pyright: ignore[reportArgumentType]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_absolute_url(self):
        return reverse("wishitem_detail", kwargs={"wishitem_id": self.id})

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"<WishItemModel {self.title}>"
