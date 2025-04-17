from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404, redirect, render

from wishitems.models import WishItemModel

from .forms import WishItemForm


@login_required
def wishlist(request):
    if request.method == "POST":
        form = WishItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("wishlist")
    else:
        form = WishItemForm()

    wishitems = request.user.wishitems.all()
    return render(request, "wishlist.html", {"wishitems": wishitems, "form": form})


@login_required
def wishlist_retriev(request, wishitem_id):
    wishitem = get_object_or_404(WishItemModel, pk=wishitem_id)
    return render(request, "wishlist_retrieve.html", {"wishitem": wishitem})
