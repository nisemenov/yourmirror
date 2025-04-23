import uuid

from django.urls import reverse
from django.db import models

from slugify import slugify

from profiles.models import ProfileModel


def upload_to_wishlist(instance, filename):
    ext = filename.split(".")[-1]
    return f"wishitems/picture/{uuid.uuid4()}.{ext}"


class WishItemModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    picture = models.ImageField(upload_to=upload_to_wishlist, blank=True, null=True)
    slug = models.SlugField(blank=True)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(str(self.title))
            slug = base_slug
            num = 1
            while WishItemModel.objects.filter(slug=slug).exists():  # pyright: ignore[reportAttributeAccessIssue]
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse("wishitem_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"<WishItemModel {self.slug}>"
