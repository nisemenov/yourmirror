from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from profiles.models import FollowModel, ProfileModel

from .forms import EmailRegistrationForm


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    next_page = "wishlist"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


def register(request):
    if request.method == "POST":
        form = EmailRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("wishlist")
    else:
        form = EmailRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


class FollowingView(LoginRequiredMixin, ListView):
    template_name = "following.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return self.request.user.profile.following


class FollowItemCreateView(LoginRequiredMixin, ListView):
    def post(self, request, profile_id):
        target_profile = get_object_or_404(ProfileModel, id=profile_id)
        me = request.user

        if target_profile.user == me:
            return redirect("wishlist_me")

        follow_obj, created = FollowModel.objects.get_or_create(
            user=me,
            following=target_profile.user,
        )

        if not created:
            follow_obj.delete()

        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def settings(request):
    return render(request, "settings.html")
