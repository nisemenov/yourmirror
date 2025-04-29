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


class WishlistMyView(LoginRequiredMixin, ListView):
    template_name = "wishlist/my.html"
    context_object_name = "wishitems"

    def get_queryset(self):
        return self.request.user.profile.wishitems.all()


class WishlistProfileView(ListView):
    template_name = "wishlist/profile.html"
    context_object_name = "wishitems"

    def dispatch(self, request, *args, **kwargs):
        profile_id = kwargs.get("profile_id")

        if request.user.is_authenticated and profile_id == request.user.profile.id:
            return redirect("wishlist_me")

        return super().dispatch(request, *args, **kwargs)

    def get_profile(self):
        return get_object_or_404(ProfileModel, id=self.kwargs["profile_id"])

    def get_queryset(self):
        profile = self.get_profile()
        if self.request.user.is_authenticated and self.request.user.profile == profile:
            return profile.wishitems.all()
        return profile.wishitems.filter(is_private=False)

    def get_context_data(self, **kwargs):
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


class WishItemDetailView(UserPassesTestMixin, DetailView):
    model = WishItemModel
    template_name = "wishitem/detail.html"
    context_object_name = "wishitem"
    pk_url_kwarg = "wishitem_id"

    def test_func(self):
        wishitem = self.get_object()
        return not wishitem.is_private or wishitem.profile.user == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.reserved:
            self.object.reserved = None
        else:
            self.object.reserved = request.user.profile

        self.object.save()
        return redirect("wishitem_detail", wishitem_id=self.object.id)


class WishItemCreateView(LoginRequiredMixin, CreateView):
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem/form.html"
    success_url = reverse_lazy("wishlist_me")

    def form_valid(self, form):
        self.object = form.save(profile=self.request.user.profile)
        return super().form_valid(form)


class WishItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem/form.html"
    success_url = reverse_lazy("wishlist_me")
    pk_url_kwarg = "wishitem_id"

    def test_func(self):
        return self.get_object().profile.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.request.META.get(
            "HTTP_REFERER", reverse("wishlist_me")
        )
        return context


class WishItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WishItemModel
    template_name = "wishitem/delete.html"
    success_url = reverse_lazy("wishlist_me")
    pk_url_kwarg = "wishitem_id"
    context_object_name = "wishitem"

    def test_func(self):
        return self.get_object().profile.user == self.request.user
