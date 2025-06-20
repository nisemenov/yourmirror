from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, cast

import pytest

from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from tests.factories import RegistrationTokenFactory, UserFactory
from tests.values import VarStr

from services.forms import EmailRegistrationForm
from services.models import RegistrationTokenModel

if TYPE_CHECKING:
    from collections.abc import Callable
    from django.db.models import QuerySet
    from django.test import Client
    from tests.conftest import (
        BasicAssertsReverse,
        BasicAssertsTemplate,
        AssertsTaskEmails,
    )


pytestmark = pytest.mark.django_db


# REGISTER
# FORM
def test_email_registration_form_valid() -> None:
    form_data = {
        "email": VarStr.USER_EMAIL,
        "first_name": VarStr.USER_NAME,
        "password1": VarStr.USER_PASSWORD,
        "password2": VarStr.USER_PASSWORD,
    }
    form = EmailRegistrationForm(data=form_data)
    assert form.is_valid()

    user = form.save()
    assert user.email == VarStr.USER_EMAIL
    assert user.username == VarStr.USER_EMAIL
    assert user.first_name == VarStr.USER_NAME
    assert user.profile.id


# VIEW
def test_register_view_get(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    url = reverse("register")
    response = client.get(url)
    basic_asserts_template(cast(HttpResponse, response), VarStr.USER_REG_VIEW)


def test_register_view_post(
    client: Client,
    asserts_registration_token: Callable[[QuerySet[RegistrationTokenModel]], None],
    basic_asserts_template: BasicAssertsTemplate,
    asserts_task_emails: AssertsTaskEmails,
) -> None:
    url = reverse("register")
    data = {
        "email": VarStr.USER_EMAIL,
        "first_name": VarStr.USER_NAME,
        "password1": VarStr.USER_PASSWORD,
        "password2": VarStr.USER_PASSWORD,
    }
    response = client.post(url, data)
    basic_asserts_template(cast(HttpResponse, response), VarStr.USER_REG_EMAIL_SENT)
    asserts_task_emails(
        mail.outbox, VarStr.CONFIRMATION_EMAIL_SUBJECT, VarStr.USER_EMAIL
    )

    reg_tokens = RegistrationTokenModel.objects.filter(
        email=VarStr.USER_EMAIL,
        first_name=VarStr.USER_NAME,
    )
    asserts_registration_token(reg_tokens)


def test_register_view_post_expired_tok(
    client: Client,
    asserts_registration_token: Callable[[QuerySet[RegistrationTokenModel]], None],
    basic_asserts_template: BasicAssertsTemplate,
    asserts_task_emails: AssertsTaskEmails,
) -> None:
    reg_token = cast(
        RegistrationTokenModel,
        RegistrationTokenFactory(
            email=VarStr.USER_EMAIL,
            expires_at=(timezone.now() - timedelta(hours=24)),
        ),
    )
    assert reg_token.is_expired

    url = reverse("register")
    data = {
        "email": VarStr.USER_EMAIL,
        "first_name": VarStr.USER_NAME,
        "password1": VarStr.USER_PASSWORD,
        "password2": VarStr.USER_PASSWORD,
    }
    response = client.post(url, data)
    basic_asserts_template(cast(HttpResponse, response), VarStr.USER_REG_EMAIL_SENT)
    asserts_task_emails(
        mail.outbox, VarStr.CONFIRMATION_EMAIL_SUBJECT, VarStr.USER_EMAIL
    )

    reg_tokens = RegistrationTokenModel.objects.filter(
        email=VarStr.USER_EMAIL,
        first_name=VarStr.USER_NAME,
    )
    asserts_registration_token(reg_tokens)

    reg_token.refresh_from_db()
    assert reg_token.id == reg_tokens[0].id


def test_register_user_already_exists_with_password(
    client: Client,
    basic_asserts_template: BasicAssertsTemplate,
) -> None:
    user = cast(User, UserFactory(username=VarStr.USER_EMAIL, email=VarStr.USER_EMAIL))

    url = reverse("register")
    data = {
        "email": VarStr.USER_EMAIL,
        "first_name": VarStr.USER_NAME,
        "password1": "newpassword123",
        "password2": "newpassword123",
    }

    response = client.post(url, data)
    basic_asserts_template(
        cast(HttpResponse, response), VarStr.USER_REG_HAS_USABLE_PASSWORD
    )

    user.refresh_from_db()
    assert user.check_password(VarStr.USER_PASSWORD)
    assert user.first_name == ""


def test_register_user_exists_without_password(
    client: Client,
    basic_asserts_reverse: BasicAssertsReverse,
) -> None:
    user = cast(User, UserFactory(username=VarStr.USER_EMAIL, email=VarStr.USER_EMAIL))
    user.set_unusable_password()
    user.save()

    url = reverse("register")
    data = {
        "email": VarStr.USER_EMAIL,
        "first_name": VarStr.USER_NAME,
        "password1": VarStr.USER_PASSWORD,
        "password2": VarStr.USER_PASSWORD,
    }

    response = client.post(url, data)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "wishlist_me")

    user.refresh_from_db()
    assert user.first_name == VarStr.USER_NAME
    assert user.check_password(VarStr.USER_PASSWORD)


# LOGIN
def test_login_view(client: Client, basic_asserts_reverse: BasicAssertsReverse) -> None:
    user = cast(User, UserFactory())
    url = reverse("login")
    data = {
        "username": user.username,
        "password": "testpass123",
    }
    response = client.post(url, data)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "wishlist_me")
