import uuid

from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models


def upload_to_wishlist(instance, filename):
    ext = filename.split(".")[-1]
    return f"wishitems/picture/{uuid.uuid4()}.{ext}"


class WishItemModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    picture = models.ImageField(upload_to=upload_to_wishlist, blank=True, null=True)

    slug = models.SlugField(blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishitems")

    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<WishItemModel {self.slug}>"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while WishItemModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("wish_detail", kwargs={"slug": self.slug})
