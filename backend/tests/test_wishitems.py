import pytest

from django.urls import reverse

from tests.values import VarStr
from wishitems.models import WishItemModel
from wishitems.forms import WishItemForm
from tests.factories import UserFactory, WishItemFactory


pytestmark = pytest.mark.django_db


# FORMS
def test_wishitem_form():
    user = UserFactory()
    form_data = {
        "title": VarStr.WISHITEM_TITLE,
        "link": VarStr.WISHITEM_LINK,
        "description": VarStr.WISHITEM_DESCRIPTION,
        "is_private": True,
    }
    form = WishItemForm(data=form_data)
    assert form.is_valid()

    form.save(profile=user.profile)
    assert len(WishItemModel.objects.filter(profile=user.profile)) == 1


# VIEWS
def test_wishlist_my_empty_view(client, basic_asserts_template):
    user = UserFactory()
    client.force_login(user)
    url = reverse("wishlist_me")
    response = client.get(url)
    basic_asserts_template(response, VarStr.WISHILIST_MY_EMPTY)


def test_wishlist_profile_empty_view(client, basic_asserts_template):
    user_1, user_2 = UserFactory.create_batch(2)
    client.force_login(user_2)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_1.profile.id})
    response = client.get(url)
    basic_asserts_template(response, VarStr.WISHILIST_PROFILE_EMPTY)


def test_wishlist_my_view(client, basic_asserts_template):
    user = UserFactory()
    WishItemFactory(
        title=VarStr.WISHITEM_TITLE,
        profile=user.profile,
    )
    client.force_login(user)
    response = client.get(reverse("wishlist_me"))
    basic_asserts_template(response, VarStr.WISHITEM_TITLE)


def test_wishlist_profile_view(client, basic_asserts_template):
    user_1, user_2 = UserFactory.create_batch(2)
    WishItemFactory(
        title=VarStr.WISHITEM_TITLE,
        profile=user_1.profile,
        is_private=False,
    )

    client.force_login(user_2)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_1.profile.id})
    response = client.get(url)
    basic_asserts_template(response, VarStr.WISHITEM_TITLE)


def test_wishlist_profile_with_private_view(client, basic_asserts_template):
    user_1, user_2 = UserFactory.create_batch(2)
    WishItemFactory(
        profile=user_1.profile,
        is_private=True,
    )

    client.force_login(user_2)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_1.profile.id})
    response = client.get(url)
    basic_asserts_template(response, VarStr.WISHILIST_PROFILE_EMPTY)


def test_wishitem_detail_view(client, basic_asserts_template):
    user = UserFactory()
    wishitem = WishItemFactory(
        title=VarStr.WISHITEM_TITLE,
        profile=user.profile,
    )

    client.force_login(user)
    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    basic_asserts_template(response, VarStr.WISHITEM_TITLE)


def test_wishitem_detail_view_private(client):
    user_1, user_2 = UserFactory.create_batch(2)
    wishitem = WishItemFactory(profile=user_1.profile, is_private=True)

    client.force_login(user_2)
    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    assert response.status_code == 403


def test_wishitem_create_view(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("wishitem_create")
    data = {
        "title": VarStr.WISHITEM_TITLE,
        "link": VarStr.WISHITEM_LINK,
        "description": VarStr.WISHITEM_DESCRIPTION,
        "is_private": False,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert WishItemModel.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
        title=VarStr.WISHITEM_TITLE,
        profile=user.profile,
    ).exists()


def test_wishitem_update_view(client):
    user = UserFactory()
    wishitem = WishItemFactory(
        title=VarStr.WISHITEM_TITLE,
        profile=user.profile,
    )
    client.force_login(user)
    url = reverse("wishitem_update", kwargs={"wishitem_id": wishitem.id})
    data = {
        "title": "new_title",
    }
    response = client.post(url, data)

    assert response.status_code == 302
    wishitem.refresh_from_db()
    assert wishitem.title == "new_title"


def test_delete_view(client):
    user = UserFactory()
    wishitem = WishItemFactory(
        profile=user.profile,
    )
    client.force_login(user)
    url = reverse("wishitem_delete", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url)
    assert response.status_code == 302
    assert not WishItemModel.objects.filter(id=wishitem.id).exists()  # pyright: ignore[reportAttributeAccessIssue]


# ANONYMOUS VIEWS
@pytest.mark.parametrize(
    "word",
    (
        VarStr.WISHITEM_RESERVED,
        VarStr.WISHITEM_UPDATE,
        VarStr.WISHITEM_DELETE,
    ),
)
def test_wishitem_detail_anon(client, word, basic_asserts_template_with_not):
    wishitem = WishItemFactory(
        is_private=False,
    )

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    basic_asserts_template_with_not(response, word)


def test_wishitem_detail_view_private_anon(client):
    wishitem = WishItemFactory(is_private=True)

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.parametrize(
    ("url_name", "kwargs"),
    (
        (
            "wishlist_me",
            False,
        ),
        (
            "wishitem_create",
            False,
        ),
        (
            "wishitem_update",
            True,
        ),
        (
            "wishitem_delete",
            True,
        ),
    ),
)
def test_wishitem_views_login_req(client, basic_asserts_reverse, url_name, kwargs):
    wishitem = WishItemFactory()
    if kwargs:
        url = reverse(url_name, kwargs={"wishitem_id": wishitem.id})
    else:
        url = reverse(url_name)
    response = client.post(url)
    basic_asserts_reverse(response, "login")


def test_wishlist_profile_view_anon(client, basic_asserts_template):
    user = UserFactory()
    WishItemFactory(
        title=VarStr.WISHITEM_TITLE,
        profile=user.profile,
        is_private=False,
    )

    url = reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})
    response = client.get(url)
    basic_asserts_template(response, VarStr.WISHITEM_TITLE)
