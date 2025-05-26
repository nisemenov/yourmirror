from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, cast

import uuid
import pytest

from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from tests.factories import RegistrationTokenFactory, UserFactory, WishItemFactory
from tests.values import VarStr

from services.models import RegistrationTokenModel
from wishitems.models import WishItemModel

if TYPE_CHECKING:
    from django.test import Client
    from tests.conftest import (
        BasicAssertsTemplate,
        BasicAssertsReverse,
        AssertsUser,
        AssertsTaskEmails,
    )


pytestmark = pytest.mark.django_db


# CONFIRM_EMAIL
def test_confirm_email_create_user(
    client: Client,
    basic_asserts_reverse: BasicAssertsReverse,
    asserts_user: AssertsUser,
) -> None:
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            email=VarStr.USER_EMAIL,
        ),
    )
    url = reverse("confirm_email", kwargs={"token": reg_token.token})
    response = client.get(url)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "home")

    users = User.objects.filter(email=VarStr.USER_EMAIL)
    asserts_user(users=users, basic_fields=True, profile=True)
    assert not RegistrationTokenModel.objects.filter(email=VarStr.USER_EMAIL).exists()


def test_confirm_email_expired(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            expires_at=(timezone.now() - timedelta(hours=24)),
        ),
    )
    url = reverse("confirm_email", kwargs={"token": reg_token.token})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.CONFIRM_EMAIL_EXPIRED)


# CONFIRM_FIRST_RESERVATION_EMAIL
def test_confirm_first_reservation_email_view(
    client: Client,
    basic_asserts_reverse: BasicAssertsReverse,
    asserts_user: AssertsUser,
    asserts_task_emails: AssertsTaskEmails,
) -> None:
    wishitem = cast(WishItemModel, WishItemFactory())
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            email=VarStr.USER_EMAIL,
            wishitem=wishitem,
        ),
    )

    url = reverse("confirm_first_reservation_email", kwargs={"token": reg_token.token})
    response = client.get(url)
    basic_asserts_reverse(
        cast(HttpResponseRedirect, response),
        "wishitem_detail",
        {"wishitem_id": wishitem.id},
    )
    asserts_task_emails(mail.outbox, wishitem.title, VarStr.USER_EMAIL)

    users = User.objects.filter(email=VarStr.USER_EMAIL)
    asserts_user(users=users)

    user = users[0]
    wishitem.refresh_from_db()
    assert not user.has_usable_password()
    assert wishitem.reserved
    assert user == wishitem.reserved.user
    assert not RegistrationTokenModel.objects.filter(email=VarStr.USER_EMAIL).exists()


def test_confirm_first_reservation_email_expired_tok(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            expires_at=(timezone.now() - timedelta(hours=24)),
        ),
    )
    url = reverse("confirm_first_reservation_email", kwargs={"token": reg_token.token})
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.CONFIRM_EMAIL_EXPIRED)


def test_confirm_first_reservation_with_race_conditions(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            is_private=False,
            reserved=cast(User, UserFactory()).profile,
        ),
    )
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            email=VarStr.USER_EMAIL,
            wishitem=wishitem,
        ),
    )
    url = reverse("confirm_first_reservation_email", kwargs={"token": reg_token.token})
    response = client.get(url)
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.CONFIRM_FIRST_RESERVATION_RACE_CONDITION
    )


def test_confirm_first_reservation_with_deleted_wishitem(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    wishitem = cast(
        WishItemModel,
        WishItemFactory(
            is_private=False,
        ),
    )
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            email=VarStr.USER_EMAIL,
            wishitem=wishitem,
        ),
    )
    wishitem.delete()

    url = reverse("confirm_first_reservation_email", kwargs={"token": reg_token.token})
    response = client.get(url)
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.CONFIRM_EMAIL_INVALID_TOK
    )


# COMMON
@pytest.mark.parametrize(
    "url",
    (
        "confirm_email",
        "confirm_first_reservation_email",
    ),
)
def test_confirms_with_invalid_token(
    client: Client,
    url: str,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    url = reverse(url, kwargs={"token": uuid.uuid4()})
    response = client.get(url)
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.CONFIRM_EMAIL_INVALID_TOK
    )
