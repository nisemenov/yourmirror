from django.contrib import admin

from wishitems.models import WishItemModel


@admin.register(WishItemModel)
class WishItemAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass
