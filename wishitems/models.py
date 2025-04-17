import uuid
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def upload_to_wishlist(instance, filename):
    ext = filename.split(".")[-1]
    return f"wishitems/picture/{uuid.uuid4()}.{ext}"


class WishItemModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    picture = models.ImageField(upload_to=upload_to_wishlist, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishitems")

    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<WishItemModel {self.pk} / {self.title}>"
