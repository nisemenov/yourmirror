from datetime import timedelta
from typing import Any, cast

import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from profiles.models import ProfileModel
from services.models import RegistrationTokenModel
from tasks.email import send_first_reservation_email, send_reservation_email

from .models import WishItemModel
from .forms import WishItemForm, EmailReserveForm


class WishlistMyView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    template_name = "wishlist/my.html"
    context_object_name = "wishitems"

    def get_queryset(self) -> QuerySet[WishItemModel]:
        user = cast(User, self.request.user)
        profile = cast(ProfileModel, user.profile)  # type: ignore[attr-defined]
        return profile.wishitems.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = cast(User, self.request.user)
        share_url = self.request.build_absolute_uri(
            reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})  # type: ignore[attr-defined]
        )
        context["share_url"] = share_url
        return context


class WishlistProfileView(ListView):  # type: ignore[type-arg]
    template_name = "wishlist/profile.html"
    context_object_name = "wishitems"

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase:
        profile_id = kwargs.get("profile_id")

        if request.user.is_authenticated and profile_id == request.user.profile.id:  # type: ignore[attr-defined]
            return redirect("wishlist_me")

        return super().dispatch(request, *args, **kwargs)

    def get_profile(self) -> ProfileModel:
        return get_object_or_404(ProfileModel, id=self.kwargs["profile_id"])

    def get_queryset(self) -> QuerySet[WishItemModel]:
        profile = self.get_profile()
        if self.request.user.is_authenticated and self.request.user.profile == profile:  # type: ignore[attr-defined]
            return profile.wishitems.all()
        return profile.wishitems.filter(is_private=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context["owner"] = profile

        if self.request.user.is_authenticated:
            context["is_owner"] = self.request.user.profile == profile  # type: ignore[attr-defined]
            context["is_following"] = self.request.user.profile.is_following(profile)  # type: ignore[attr-defined]
        else:
            context["is_owner"] = False
            context["is_following"] = False

        return context


class WishItemDetailView(UserPassesTestMixin, DetailView):  # type: ignore[type-arg]
    model = WishItemModel
    template_name = "wishitem/detail.html"
    context_object_name = "wishitem"
    pk_url_kwarg = "wishitem_id"

    def test_func(self) -> bool:
        wishitem = self.get_object()
        return not wishitem.is_private or (wishitem.profile.user == self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = EmailReserveForm()
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        wishitem = self.object
        user = request.user

        if not user.is_authenticated:
            form = EmailReserveForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    registration_token, created = (
                        RegistrationTokenModel.objects.get_or_create(
                            email=email,
                            defaults={
                                "token": str(uuid.uuid4()),
                                "wishitem": wishitem,
                            },
                        )
                    )
                    if not created:
                        if registration_token.is_expired:
                            registration_token.token = str(uuid.uuid4())
                            registration_token.expires_at = timezone.now() + timedelta(
                                hours=24
                            )
                        registration_token.wishitem = wishitem
                        registration_token.save()

                    # Отправка письма
                    confirmation_url = f"{settings.FULL_DOMAIN}/confirm_email/{registration_token.token}/"
                    send_first_reservation_email.delay(email, confirmation_url)
                    return self.render_to_response(
                        self.get_context_data(form=EmailReserveForm(), email_sent=True)
                    )
            else:
                return self.render_to_response(self.get_context_data(form=form))

        if wishitem.profile.user == user:
            return render(
                request,
                template_name="403.html",
                context={"message": "Вы не можете зарезервировать свое желание"},
                status=403,
            )
        else:
            if wishitem.reserved == user.profile:  # type: ignore[attr-defined]
                wishitem.reserved = None
            elif wishitem.reserved is None:
                wishitem.reserved = user.profile  # type: ignore[attr-defined]
            else:
                return render(
                    request,
                    template_name="403.html",
                    context={"message": "Это желание уже кто-то зарезервировал"},
                    status=403,
                )
            wishitem.reserved_at = timezone.now()
            wishitem.save()

        # Отправка письма
        send_reservation_email.delay(user.email, wishitem.id)
        return redirect("wishitem_detail", wishitem_id=wishitem.id)


class WishItemCreateView(LoginRequiredMixin, CreateView):  # type: ignore[type-arg]
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem/form.html"
    success_url = reverse_lazy("wishlist_me")

    def form_valid(self, form: WishItemForm) -> HttpResponse:
        user = cast(User, self.request.user)
        self.object = form.save(profile=user.profile)  # type: ignore[attr-defined]
        return super().form_valid(form)


class WishItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # type: ignore[type-arg]
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem/form.html"
    success_url = reverse_lazy("wishlist_me")
    pk_url_kwarg = "wishitem_id"

    def test_func(self) -> bool:
        return bool(self.get_object().profile.user == self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.META.get(
            "HTTP_REFERER", reverse("wishlist_me")
        )
        return context


class WishItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # type: ignore[type-arg]
    model = WishItemModel
    template_name = "wishitem/delete.html"
    success_url = reverse_lazy("wishlist_me")
    pk_url_kwarg = "wishitem_id"
    context_object_name = "wishitem"

    def test_func(self) -> bool:
        return bool(self.get_object().profile.user == self.request.user)
