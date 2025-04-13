from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.views.generic import TemplateView

from users.views import CustomLoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path("auth/", include("django.contrib.auth.urls")),
    path("contacts/", views.flatpage, {"url": "/contacts/"}, name="contacts"),
    path("about/", views.flatpage, {"url": "/about/"}, name="about"),
    path("users/", include("users.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("__reload__/", include("django_browser_reload.urls")),
]
