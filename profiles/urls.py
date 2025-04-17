from django.urls import path
from . import views

urlpatterns = [
    path("following/", views.following, name="following"),
    path("settings/", views.settings, name="settings"),
]
