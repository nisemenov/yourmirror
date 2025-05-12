from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from tests.values import VarStr
from wishitems.models import WishItemModel
from wishitems.forms import CustomClearableFileInput, WishItemForm
from tests.factories import UserFactory, WishItemFactory

if TYPE_CHECKING:
    from django.test import Client
    from tests.conftest import BasicAssertsTemplate, BasicAssertsReverse


pytestmark = pytest.mark.django_db


# FORMS
def test_wishitem_form() -> None:
    user = cast(User, UserFactory())
    form_data = {
        "title": VarStr.WISHITEM_TITLE,
        "description": VarStr.WISHITEM_DESCRIPTION,
        "link": VarStr.WISHITEM_LINK,
        "price": "1000",
        "price_currency": "₽",
        "is_private": True,
    }
    form = WishItemForm(data=form_data)
    assert form.is_valid()

    form.save(profile=user.profile)
    assert len(WishItemModel.objects.filter(profile=user.profile)) == 1


def test_wishitem_form_missing_required() -> None:
    form = WishItemForm(data={})
    assert not form.is_valid()
    assert "title" in form.errors


def test_wishitem_form_invalid_url() -> None:
    form_data = {
        "title": VarStr.WISHITEM_TITLE,
        "link": "not-a-url",
    }
    form = WishItemForm(data=form_data)
    assert not form.is_valid()
    assert "link" in form.errors


def test_custom_clearable_file_input() -> None:
    widget = CustomClearableFileInput()
    assert "custom_clearable_file_input" in widget.template_name


# VIEWS
def test_wishlist_my_empty_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    client.force_login(user)
    url = reverse("wishlist_me")
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_MY_EMPTY)


def test_wishlist_profile_empty_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    client.force_login(user_2)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_1.profile.id})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_PROFILE_EMPTY)


def test_wishlist_my_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user.profile,
        ),
    )
    client.force_login(user)
    response = client.get(reverse("wishlist_me"))
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_TITLE)


def test_wishlist_profile_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user_1.profile,
            is_private=False,
        ),
    )

    client.force_login(user_2)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_1.profile.id})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_TITLE)


def test_wishlist_profile_with_private_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    cast(
        WishItemModel,
        WishItemFactory(
            profile=user_1.profile,
            is_private=True,
        ),
    )

    client.force_login(user_2)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_1.profile.id})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_PROFILE_EMPTY)


def test_wishitem_detail_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user.profile,
        ),
    )

    client.force_login(user)
    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_TITLE)


def test_wishitem_detail_view_private(client: Client) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    wishitem = cast(
        WishItemModel,
        WishItemFactory(profile=user_1.profile, is_private=True),
    )

    client.force_login(user_2)
    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    assert response.status_code == 403


def test_wishitem_create_view(client: Client) -> None:
    user = cast(User, UserFactory())
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


def test_wishitem_update_view(client: Client) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user.profile,
        ),
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


def test_delete_view(client: Client) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            profile=user.profile,
        ),
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
def test_wishitem_detail_anon(
    client: Client, word: str, basic_asserts_template_with_not: BasicAssertsTemplate
) -> None:
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            is_private=False,
        ),
    )

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    basic_asserts_template_with_not(cast(HttpResponse, response), word)


def test_wishitem_detail_view_private_anon(client: Client) -> None:
    wishitem = cast(WishItemModel, WishItemFactory(is_private=True))

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
def test_wishitem_views_login_req(
    client: Client,
    basic_asserts_reverse: BasicAssertsReverse,
    url_name: str,
    kwargs: dict[str, Any],
) -> None:
    wishitem = cast(WishItemModel, WishItemFactory())
    if kwargs:
        url = reverse(url_name, kwargs={"wishitem_id": wishitem.id})
    else:
        url = reverse(url_name)
    response = client.post(url)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "login")


def test_wishlist_profile_view_anon(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user.profile,
            is_private=False,
        ),
    )

    url = reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_TITLE)
