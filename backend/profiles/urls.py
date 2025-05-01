from django.urls import path

from .views import FollowingView, FollowCreateView, settings


urlpatterns = [
    path("following/", FollowingView.as_view(), name="following"),
    path(
        "follow/<uuid:profile_id>/",
        FollowCreateView.as_view(),
        name="follow_create",
    ),
    path("settings/", settings, name="settings"),
]
