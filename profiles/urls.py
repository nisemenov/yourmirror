from django.urls import path
from .views import FollowingView, FollowItemCreateView, settings

urlpatterns = [
    path("following/", FollowingView.as_view(), name="following"),
    path(
        "follow/<uuid:profile_id>/",
        FollowItemCreateView.as_view(),
        name="follow_create",
    ),
    path("settings/", settings, name="settings"),
]
