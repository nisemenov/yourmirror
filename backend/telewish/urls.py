from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.views.generic import TemplateView

from profiles.views import CustomLoginView, register


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path("auth/", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("contacts/", views.flatpage, {"url": "/contacts/"}, name="contacts"),
    path("about/", views.flatpage, {"url": "/about/"}, name="about"),
    path("", include("profiles.urls")),
    path("", include("wishitems.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("__reload__/", include("django_browser_reload.urls")),
]
