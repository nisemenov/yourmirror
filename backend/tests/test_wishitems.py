from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from typing import TYPE_CHECKING, Any, cast

import pytest

from django.contrib.auth.models import User
from django.core import mail
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from services.models import RegistrationTokenModel
from wishitems.forms import CustomClearableFileInput, WishItemForm
from wishitems.models import WishItemModel

from tests.factories import RegistrationTokenFactory, UserFactory, WishItemFactory
from tests.values import VarStr

if TYPE_CHECKING:
    from django.test import Client
    from tests.conftest import (
        BasicAssertsTemplate,
        BasicAssertsReverse,
        AssertsTaskEmails,
    )


pytestmark = pytest.mark.django_db


# FORM
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


# VIEW
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
        WishItemFactory(profile=user_2.profile, is_private=True),
    )

    client.force_login(user_1)
    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    assert response.status_code == 403


def test_wishitem_create_view(
    client: Client,
) -> None:
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


@pytest.mark.parametrize(
    "word",
    (
        VarStr.WISHITEM_RESERVE,
        VarStr.WISHITEM_RESERVED_BY_USER,
    ),
)
def test_wishitem_detail_view_my_without_buttons(
    client: Client, word: str, basic_asserts_template_with_not: BasicAssertsTemplate
) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            profile=user.profile,
        ),
    )
    client.force_login(user)

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    basic_asserts_template_with_not(cast(HttpResponse, response), word)


# ANONYMOUS VIEW
@pytest.mark.parametrize(
    "word",
    (
        VarStr.WISHITEM_RESERVED,
        VarStr.WISHITEM_UPDATE,
        VarStr.WISHITEM_DELETE,
    ),
)
def test_wishitem_detail_view_anon_without_buttons(
    client: Client, word: str, basic_asserts_template_with_not: BasicAssertsTemplate
) -> None:
    wishitem = cast(WishItemModel, WishItemFactory())

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.get(url)
    basic_asserts_template_with_not(cast(HttpResponse, response), word)


def test_wishitem_detail_view_anon_private(client: Client) -> None:
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


# ITEM RESERVATION
def test_wishitem_detail_post_to_reserve(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
    basic_asserts_reverse: BasicAssertsReverse,
    asserts_task_emails: AssertsTaskEmails,
) -> None:
    user = cast(User, UserFactory())
    client.force_login(user)
    wishitem = cast(WishItemModel, WishItemFactory())
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url)
    basic_asserts_reverse(
        cast(HttpResponseRedirect, response),
        "wishitem_detail",
        {"wishitem_id": wishitem.id},
    )
    asserts_task_emails(mail.outbox, wishitem.title, user.email)

    response = client.get(url)
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.WISHITEM_RESERVED_BY_USER
    )

    wishitem.refresh_from_db()
    assert wishitem.reserved_at
    assert wishitem.reserved_at > wishitem.created_at


def test_wishitem_detail_post_to_reserve_double_reservation(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    wishitem = cast(WishItemModel, WishItemFactory())
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    client.post(url, data={"email": user_1.email})

    response = client.post(url, data={"email": user_2.email})
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.WISHITEM_DOUBLE_RESERVE_ERROR, 403
    )

    wishitem.refresh_from_db()
    assert wishitem.reserved
    assert wishitem.reserved.user == user_1


def test_wishitem_detail_my_post_to_reserve(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            profile=user.profile,
        ),
    )
    client.force_login(user)
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url)
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.WISHITEM_MY_RESERVE_ERROR, 403
    )


def test_wishitem_detail_my_post_to_reserve_without_auth(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            profile=user.profile,
        ),
    )
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url, data={"email": user.email})
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.WISHITEM_MY_RESERVE_ERROR, 403
    )


def test_wishitem_detail_post_to_reserve_without_auth(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
    basic_asserts_reverse: BasicAssertsReverse,
    asserts_task_emails: AssertsTaskEmails,
) -> None:
    user = cast(User, UserFactory())
    wishitem = cast(WishItemModel, WishItemFactory())
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url, data={"email": user.email})
    basic_asserts_reverse(
        cast(HttpResponseRedirect, response),
        "wishitem_detail",
        {"wishitem_id": wishitem.id},
    )
    asserts_task_emails(mail.outbox, wishitem.title, user.email)

    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_RESERVED)


def test_wishitem_detail_post_to_reserve_anon(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
    asserts_registration_token: Callable[[QuerySet[RegistrationTokenModel]], None],
    asserts_task_emails: AssertsTaskEmails,
) -> None:
    wishitem = cast(WishItemModel, WishItemFactory())
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url, data={"email": VarStr.USER_EMAIL})
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.WISHITEM_FIRST_RESERVATION_EMAIL
    )
    asserts_task_emails(
        mail.outbox, VarStr.FIRST_RESERVATION_EMAIL_SUBJECT, VarStr.USER_EMAIL
    )

    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_RESERVE)

    reg_tokens = RegistrationTokenModel.objects.filter(
        email=VarStr.USER_EMAIL,
        wishitem=wishitem,
    )
    asserts_registration_token(reg_tokens)


def test_wishitem_detail_post_with_wrong_email_form(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    wishitem = cast(WishItemModel, WishItemFactory())

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url, data={"email": "not_email"})
    basic_asserts_template(
        cast(HttpResponse, response), "Введите правильный адрес электронной почты."
    )


def test_wishitem_detail_post_to_reserve_private(client: Client) -> None:
    user = cast(User, UserFactory())
    client.force_login(user)
    wishitem = cast(WishItemModel, WishItemFactory(is_private=True))
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url, data={"email": user.email})
    assert response.status_code == 403

    wishitem.refresh_from_db()
    assert not wishitem.reserved


def test_wishitem_detail_post_to_reserve_without_auth_exp_token(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    wishitem = cast(WishItemModel, WishItemFactory())
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            token=VarStr.REGISTRATION_TOKEN_TOKEN,
            email=VarStr.USER_EMAIL,
            wishitem=wishitem,
            expires_at=(timezone.now() - timedelta(hours=24)),
        ),
    )
    assert not wishitem.reserved

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem.id})
    response = client.post(url, data={"email": VarStr.USER_EMAIL})
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.WISHITEM_FIRST_RESERVATION_EMAIL
    )

    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.WISHITEM_RESERVE)

    reg_token.refresh_from_db()
    assert reg_token.token != VarStr.REGISTRATION_TOKEN_TOKEN
    assert not reg_token.is_expired


def test_wishitem_detail_post_to_reserve_anon_only_last_item(
    client: Client,
    asserts_registration_token: Callable[[QuerySet[RegistrationTokenModel]], None],
) -> None:
    wishitem_1, wishitem_2 = WishItemFactory.create_batch(2)

    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem_1.id})
    client.post(url, data={"email": VarStr.USER_EMAIL})
    url = reverse("wishitem_detail", kwargs={"wishitem_id": wishitem_2.id})
    client.post(url, data={"email": VarStr.USER_EMAIL})

    reg_tokens = RegistrationTokenModel.objects.filter(
        email=VarStr.USER_EMAIL,
    )
    asserts_registration_token(reg_tokens)
    assert reg_tokens[0].wishitem == wishitem_2
