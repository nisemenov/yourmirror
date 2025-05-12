from typing import Any, cast

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
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

from .models import WishItemModel
from .forms import WishItemForm


class WishlistMyView(LoginRequiredMixin, ListView):  # type: ignore[type-arg]
    template_name = "wishlist/my.html"
    context_object_name = "wishitems"

    def get_queryset(self) -> QuerySet[WishItemModel]:
        user = cast(User, self.request.user)
        return user.profile.wishitems.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = cast(User, self.request.user)
        share_url = self.request.build_absolute_uri(
            reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})
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

        if request.user.is_authenticated and profile_id == request.user.profile.id:
            return redirect("wishlist_me")

        return super().dispatch(request, *args, **kwargs)

    def get_profile(self) -> ProfileModel:
        return get_object_or_404(ProfileModel, id=self.kwargs["profile_id"])

    def get_queryset(self) -> QuerySet[WishItemModel]:
        profile = self.get_profile()
        if self.request.user.is_authenticated and self.request.user.profile == profile:
            return profile.wishitems.all()
        return profile.wishitems.filter(is_private=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context["owner"] = profile

        if self.request.user.is_authenticated:
            context["is_owner"] = self.request.user.profile == profile
            context["is_following"] = self.request.user.profile.is_following(profile)
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
        return not wishitem.is_private or wishitem.profile.user == self.request.user

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = request.user
        if isinstance(user, User):
            self.object = self.get_object()

            if self.object.reserved:
                self.object.reserved = None
            else:
                self.object.reserved = user.profile

            self.object.save()
        return redirect("wishitem_detail", wishitem_id=self.object.id)


class WishItemCreateView(LoginRequiredMixin, CreateView):  # type: ignore[type-arg]
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem/form.html"
    success_url = reverse_lazy("wishlist_me")

    def form_valid(self, form: WishItemForm) -> HttpResponse:
        user = cast(User, self.request.user)
        self.object = form.save(profile=user.profile)
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
