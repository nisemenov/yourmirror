from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from profiles.models import FollowModel, ProfileModel
from yourmirror.settings import LOGIN_REMEMBER_ME

from .forms import EmailRegistrationForm, UserSettingsForm

if TYPE_CHECKING:
    from django.contrib.auth.forms import AuthenticationForm
    from django.db.models.query import QuerySet


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = "wishlist_me"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        email = self.request.session.pop("prefilled_email", None)
        if email:
            print(initial)
            initial["username"] = email
        return initial

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(LOGIN_REMEMBER_ME)
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
                    return redirect("wishlist_me")
            except User.DoesNotExist:
                user = form.save()
                login(request, user)
                return redirect("wishlist_me")
    else:
        form = EmailRegistrationForm(initial={"email": request.GET.get("email", "")})

    return render(request, "registration/register.html", {"form": form})


class FollowingView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    template_name = "following.html"
    context_object_name = "profiles"

    def get_queryset(self) -> QuerySet[ProfileModel]:
        user = cast(User, self.request.user)
        return user.profile.following


class FollowCreateView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    def post(self, request: HttpRequest, profile_id: int) -> HttpResponse:
        target_profile = get_object_or_404(ProfileModel, id=profile_id)
        user = cast(User, request.user)
        me = user.profile

        follow_obj, created = FollowModel.objects.get_or_create(  # pyright: ignore[reportAttributeAccessIssue]
            follower=me,
            following=target_profile,
        )
        if not created:
            follow_obj.delete()

        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def settings(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    if request.method == "POST":
        form = UserSettingsForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect("settings")
    else:
        form = UserSettingsForm(
            user=user,
            initial={
                "email": user.email,
                "first_name": user.first_name,
                "telegram_id": getattr(user.profile, "telegram_id", ""),
            },
        )
    return render(request, "settings/main.html", {"form": form})
