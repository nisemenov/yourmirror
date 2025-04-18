from django.contrib import admin

from wishitems.models import WishItemModel


@admin.register(WishItemModel)
class WishItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
