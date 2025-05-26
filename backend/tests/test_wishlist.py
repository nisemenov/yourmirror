from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from tests.values import VarStr
from wishitems.models import WishItemModel
from tests.factories import UserFactory, WishItemFactory

if TYPE_CHECKING:
    from django.test import Client
    from tests.conftest import BasicAssertsTemplate, BasicAssertsReverse


pytestmark = pytest.mark.django_db


def test_wishlist_my_empty_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    client.force_login(cast(User, UserFactory()))
    url = reverse("wishlist_me")
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_MY_EMPTY)


def test_wishlist_profile_empty_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    client.force_login(user_1)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_2.profile.id})  # type: ignore[attr-defined]
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_PROFILE_EMPTY)


def test_wishlist_my_view(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
    basic_asserts_reverse: BasicAssertsReverse,
) -> None:
    user = cast(User, UserFactory())
    cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user.profile,  # type: ignore[attr-defined]
        ),
    )
    client.force_login(user)

    url = reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})  # type: ignore[attr-defined]
    response = client.get(url)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "wishlist_me")

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
            profile=user_2.profile,  # type: ignore[attr-defined]
            is_private=False,
        ),
    )

    client.force_login(user_1)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_2.profile.id})  # type: ignore[attr-defined]
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_TITLE)


def test_wishlist_profile_with_private_view(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    cast(
        WishItemModel,
        WishItemFactory(
            profile=user_2.profile,  # type: ignore[attr-defined]
            is_private=True,
        ),
    )

    client.force_login(user_1)
    url = reverse("wishlist_profile", kwargs={"profile_id": user_2.profile.id})  # type: ignore[attr-defined]
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_PROFILE_EMPTY)


# ANONYMOUS
def test_wishlist_profile_empty_view_anon(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    url = reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})  # type: ignore[attr-defined]
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHILIST_PROFILE_EMPTY)


def test_wishlist_profile_view_anon(
    client: Client, basic_asserts_template: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    cast(
        WishItemModel,
        WishItemFactory(
            title=VarStr.WISHITEM_TITLE,
            profile=user.profile,  # type: ignore[attr-defined]
            is_private=False,
        ),
    )

    url = reverse("wishlist_profile", kwargs={"profile_id": user.profile.id})  # type: ignore[attr-defined]
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_TITLE)
