from django.urls import path
from .views import (
    WishItemDetailView,
    WishItemCreateView,
    WishItemUpdateView,
    WishItemDeleteView,
    WishlistMyView,
    WishlistProfileView,
)


urlpatterns = [
    path("wishlist/me/", WishlistMyView.as_view(), name="wishlist_me"),
    path(
        "wishlist/<uuid:profile_id>/",
        WishlistProfileView.as_view(),
        name="wishlist_profile",
    ),
    path("wishitem/add/", WishItemCreateView.as_view(), name="wishitem_create"),
    path(
        "wishitem/<uuid:wishitem_id>/",
        WishItemDetailView.as_view(),
        name="wishitem_detail",
    ),
    path(
        "wishitem/<uuid:wishitem_id>/edit/",
        WishItemUpdateView.as_view(),
        name="wishitem_update",
    ),
    path(
        "wishitem/<uuid:wishitem_id>/delete/",
        WishItemDeleteView.as_view(),
        name="wishitem_delete",
    ),
]
