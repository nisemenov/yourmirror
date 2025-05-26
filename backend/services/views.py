from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

import uuid

from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from services.models import RegistrationTokenModel
from tasks.email import send_confirmation_email, send_reservation_email

from .forms import EmailRegistrationForm

if TYPE_CHECKING:
    from django.contrib.auth.forms import AuthenticationForm


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = "wishlist_me"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        email = self.request.session.pop("prefilled_email", None)
        if email:
            initial["username"] = email
        return initial

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1)
        return super().form_valid(form)


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EmailRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                if user.has_usable_password():
                    form.add_error(
                        "email", "Пользователь с таким email уже зарегистрирован, "
                    )
                    request.session["prefilled_email"] = email
                    return render(request, "registration/register.html", {"form": form})
                else:
                    user.set_password(form.cleaned_data["password1"])
                    user.first_name = form.cleaned_data["first_name"]
                    user.save()
                    login(request, user)
                    # TODO Отправка письма
                    return redirect("wishlist_me")
            except User.DoesNotExist:
                registration_token, created = (
                    RegistrationTokenModel.objects.get_or_create(
                        email=email,
                        defaults={
                            "first_name": form.cleaned_data["first_name"],
                            "password_hash": make_password(
                                form.cleaned_data["password1"]
                            ),
                            "token": str(uuid.uuid4()),
                        },
                    )
                )
                if not created and registration_token.is_expired:
                    registration_token.first_name = form.cleaned_data["first_name"]
                    registration_token.password_hash = make_password(
                        form.cleaned_data["password1"]
                    )
                    registration_token.token = str(uuid.uuid4())
                    registration_token.expires_at = timezone.now() + timedelta(hours=24)
                    registration_token.save()

                # Отправка письма
                confirmation_url = request.build_absolute_uri(
                    f"/auth/confirm/{registration_token.token}/"
                )
                send_confirmation_email.delay(email, confirmation_url)
                return render(request, "registration/email_sent.html")
    else:
        form = EmailRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def confirm_email(request: HttpRequest, token: uuid.UUID) -> HttpResponse:
    try:
        registration_token = RegistrationTokenModel.objects.get(token=token)
        if registration_token.is_expired:
            return render(
                request,
                "registration/confirmation_failed.html",
                {"error": "Ссылка истекла."},
            )

        user, created = User.objects.get_or_create(
            email=registration_token.email,
            defaults={
                "username": registration_token.email,
                "first_name": registration_token.first_name,
            },
        )
        if created:
            user.password = registration_token.password_hash
            user.save()
            registration_token.delete()

        login(request, user)
        return redirect("home")
    except RegistrationTokenModel.DoesNotExist:
        return render(
            request,
            "registration/confirmation_failed.html",
            {"error": "Недействительная ссылка."},
        )


def confirm_first_reservation_email(request: HttpRequest, token: str) -> HttpResponse:
    try:
        registration_token = RegistrationTokenModel.objects.get(token=token)
        if registration_token.is_expired:
            return render(
                request,
                "registration/confirmation_failed.html",
                {"error": "Ссылка истекла."},
            )

        # for mypy [union-attr], если wishitem нет, то инстанс удалится из-за каскада
        wishitem = registration_token.wishitem
        if wishitem.reserved:  # type: ignore[union-attr]
            return render(
                request,
                "registration/confirmation_failed.html",
                {"error": "кто-то уже зарезервировал это желание"},
            )
        else:
            user, created = User.objects.get_or_create(
                email=registration_token.email,
                defaults={
                    "username": registration_token.email,
                },
            )

            wishitem.reserved = user.profile  # type: ignore[union-attr]
            wishitem.save()  # type: ignore[union-attr]

            # Отправка письма
            send_reservation_email.delay(
                registration_token.email,
                registration_token.wishitem.id,  # type: ignore[union-attr]
            )

            if created:
                user.set_unusable_password()
                user.save()
                registration_token.delete()

            return redirect(
                "wishitem_detail",
                wishitem_id=registration_token.wishitem.id,  # type: ignore[union-attr]
            )
    except RegistrationTokenModel.DoesNotExist:
        return render(
            request,
            "registration/confirmation_failed.html",
            {"error": "Недействительная ссылка."},
        )
