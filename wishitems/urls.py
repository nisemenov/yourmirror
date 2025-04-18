from django.urls import path
from .views import (
    WishItemListView,
    WishItemDetailView,
    WishItemCreateView,
    WishItemUpdateView,
    WishItemDeleteView,
)


urlpatterns = [
    path("wishlist/", WishItemListView.as_view(), name="wishlist"),
    path("wishlist/add/", WishItemCreateView.as_view(), name="wishitem_create"),
    path("wishlist/<slug:slug>/", WishItemDetailView.as_view(), name="wishitem_detail"),
    path(
        "wishlist/<slug:slug>/edit/",
        WishItemUpdateView.as_view(),
        name="wishitem_update",
    ),
    path(
        "wishlist/<slug:slug>/delete/",
        WishItemDeleteView.as_view(),
        name="wishitem_delete",
    ),
]
