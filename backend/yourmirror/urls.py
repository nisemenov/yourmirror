from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("profiles.urls")),
    path("", include("services.urls")),
    path("", include("wishitems.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", views.flatpage, {"url": "/about/"}, name="about"),
    path("auth/", include("django.contrib.auth.urls")),
    path("contacts/", views.flatpage, {"url": "/contacts/"}, name="contacts"),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
