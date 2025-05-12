from typing import Any
import uuid

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db import models


from profiles.models import ProfileModel


def upload_to_wishlist(instance: "WishItemModel", filename: str) -> str:
    ext = filename.split(".")[-1]
    return f"wishitems/picture/{uuid.uuid4()}.{ext}"


class WishItemModel(models.Model):
    PRICE_CURRENCY_CHOICES = [
        ("₽", "RUB"),
        ("$", "USD"),
        ("€", "EUR"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    picture = models.ImageField(upload_to=upload_to_wishlist, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True)
    price_currency = models.CharField(choices=PRICE_CURRENCY_CHOICES, blank=True)

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

    class Meta:
        ordering = ["title"]

    @property
    def get_price(self) -> str:
        return self.price + " " + self.price_currency

    def __str__(self) -> str:
        return f"<WishItemModel {self.title}>"


@receiver(pre_save, sender=WishItemModel)
def delete_old_picture_on_update(
    sender: WishItemModel, instance: WishItemModel, **kwargs: Any
) -> None:
    if not instance.pk:
        return

    try:
        old_file = sender.objects.get(pk=instance.pk).picture
    except sender.DoesNotExist:
        return

    new_file = instance.picture
    if old_file and old_file != new_file and old_file.storage.exists(old_file.name):
        old_file.delete(save=False)


@receiver(post_delete, sender=WishItemModel)
def delete_picture_on_delete(
    sender: WishItemModel, instance: WishItemModel, **kwargs: Any
) -> None:
    pic = instance.picture
    if pic and pic.storage.exists(pic.name):
        pic.delete(save=False)
