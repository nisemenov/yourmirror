from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from tests.factories import UserFactory
from tests.values import VarStr

from profiles.forms import EmailRegistrationForm
from profiles.models import ProfileModel

if TYPE_CHECKING:
    from django.test import Client
    from tests.conftest import BasicAssertsReverse, BasicAssertsTemplate


pytestmark = pytest.mark.django_db


def test_register_view(
    client: Client, basic_asserts_reverse: BasicAssertsReverse
) -> None:
    url = reverse("register")
    data = {
        "email": VarStr.USER_EMAIL,
        "first_name": VarStr.USER_NAME,
        "password1": VarStr.USER_PASSWORD,
        "password2": VarStr.USER_PASSWORD,
    }
    response = client.post(url, data)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "wishlist_me")
    assert ProfileModel.objects.filter(
        user__first_name=VarStr.USER_NAME,
        user__username=VarStr.USER_EMAIL,
    ).exists()


def test_login_view(client: Client, basic_asserts_reverse: BasicAssertsReverse) -> None:
    user = cast(User, UserFactory())
    url = reverse("login")
    data = {
        "username": user.username,
        "password": "testpass123",
    }
    response = client.post(url, data)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "wishlist_me")


def test_email_registration_form_valid() -> None:
    form_data = {
        "email": VarStr.USER_EMAIL,
        "password1": VarStr.USER_PASSWORD,
        "password2": VarStr.USER_PASSWORD,
    }
    form = EmailRegistrationForm(data=form_data)
    assert form.is_valid()

    user = form.save()
    assert user.email == VarStr.USER_EMAIL
    assert user.username == VarStr.USER_EMAIL
    assert user.profile.id


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
