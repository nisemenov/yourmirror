from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import WishItemModel
from .forms import WishItemForm


class WishItemListView(LoginRequiredMixin, ListView):
    model = WishItemModel
    template_name = "wishlist.html"
    context_object_name = "wishitems"

    def get_queryset(self):
        return self.request.user.wishitems.all()


class WishItemDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WishItemModel
    template_name = "wishitem_detail.html"
    context_object_name = "wishitem"

    def test_func(self):
        wishitem = self.get_object()
        return not wishitem.is_private or wishitem.user == self.request.user


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
