from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from profiles.models import FollowModel, ProfileModel

from .forms import UserSettingsForm

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class FollowingView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    template_name = "following.html"
    context_object_name = "profiles"

    def get_queryset(self) -> QuerySet[ProfileModel]:
        user = cast(User, self.request.user)
        profile = cast(ProfileModel, user.profile)  # type: ignore[attr-defined]
        return profile.following


class FollowCreateView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    def post(self, request: HttpRequest, profile_id: int) -> HttpResponse:
        target_profile = get_object_or_404(ProfileModel, id=profile_id)
        user = cast(User, request.user)
        me = user.profile  # type: ignore[attr-defined]

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
                "telegram_id": getattr(user.profile, "telegram_id", ""),  # type: ignore[attr-defined]
            },
        )
    return render(request, "settings/main.html", {"form": form})
