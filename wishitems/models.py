import uuid
from django.db import models

def get_picture_path(instance, filename):
    return 'app_data/profiles/user_{0}/{1}'


class WishItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True
    )

    link = models.URLField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=get_picture_path, blank=True)

    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
