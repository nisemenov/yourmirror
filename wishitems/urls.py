from django.urls import path
from .views import (
    WishItemDetailView,
    WishItemCreateView,
    WishItemUpdateView,
    WishItemDeleteView,
    WishlistView,
)


urlpatterns = [
    path("wishlist/me/", WishlistView.as_view(), name="wishlist"),
    path(
        "wishlist/<uuid:profile_id>/",
        WishlistView.as_view(),
        name="wishlist",
    ),
    path("wishitem/add/", WishItemCreateView.as_view(), name="wishitem_create"),
    path("wishitem/<slug:slug>/", WishItemDetailView.as_view(), name="wishitem_detail"),
    path(
        "wishitem/<slug:slug>/edit/",
        WishItemUpdateView.as_view(),
        name="wishitem_update",
    ),
    path(
        "wishitem/<slug:slug>/delete/",
        WishItemDeleteView.as_view(),
        name="wishitem_delete",
    ),
]
