from django.urls import path

from .views import (
    CustomLoginView,
    confirm_email,
    confirm_first_reservation_email,
    register,
)

urlpatterns = [
    path("auth/confirm/<str:token>/", confirm_email, name="confirm_email"),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path(
        "confirm_email/<str:token>/",
        confirm_first_reservation_email,
        name="confirm_first_reservation_email",
    ),
    path("register/", register, name="register"),
]
