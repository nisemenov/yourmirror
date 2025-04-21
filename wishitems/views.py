from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from profiles.models import ProfileModel

from .models import WishItemModel
from .forms import WishItemForm


class WishlistView(LoginRequiredMixin, ListView):
    template_name = "wishlist.html"
    context_object_name = "wishitems"

    def get_profile(self):
        profile_id = self.kwargs.get("profile_id")
        if profile_id:
            return get_object_or_404(ProfileModel, id=profile_id)
        return self.request.user.profile

    def get_queryset(self):
        return self.get_profile().user.wishitems.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_profile()
        req_user = self.request.user

        context["owner"] = profile.user
        context["is_owner"] = profile.user == req_user
        context["is_following"] = (
            req_user.profile.is_following(other_user=context["owner"])
            if not context["is_owner"]
            else None
        )

        return context


class WishItemDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WishItemModel
    template_name = "wishitem_detail.html"
    context_object_name = "wishitem"

    def test_func(self):
        wishitem = self.get_object()
        return not wishitem.is_private or wishitem.user == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user == request.user:
            # Нельзя резервировать свой айтем — просто редирект
            return redirect("wishitem_detail", slug=self.object.slug)

        # Тоггл логика
        if self.object.reserved == request.user:
            # Снять бронь
            self.object.reserved = None
        elif self.object.reserved is None:
            # Забронировать
            self.object.reserved = request.user

        self.object.save()
        return redirect("wishitem_detail", slug=self.object.slug)


class WishItemCreateView(LoginRequiredMixin, CreateView):
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem_form.html"
    success_url = reverse_lazy("wishlist")

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return super().form_valid(form)


class WishItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WishItemModel
    form_class = WishItemForm
    template_name = "wishitem_form.html"
    success_url = reverse_lazy("wishlist")

    def test_func(self):
        return self.get_object().user == self.request.user


class WishItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WishItemModel
    template_name = "wishitem_delete.html"
    success_url = reverse_lazy("wishlist")

    def test_func(self):
        return self.get_object().user == self.request.user
