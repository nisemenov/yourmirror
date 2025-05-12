from __future__ import annotations

from typing import TYPE_CHECKING, cast
from collections.abc import Callable

import pytest

from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.urls import reverse

from tests.factories import UserFactory
from tests.values import VarStr


if TYPE_CHECKING:
    from django.test import Client


pytestmark = pytest.mark.django_db


# VIEW
def test_render_view(client: Client, basic_asserts_template: Callable) -> None:
    user = cast(User, UserFactory())
    client.force_login(user)

    response = client.get(reverse("settings"))

    basic_asserts_template(response, "Настройки")
    assert "form" in response.context


# FORM
def test_update_user_data(client: Client, basic_asserts_reverse: Callable) -> None:
    user = cast(
        User,
        UserFactory(
            email=VarStr.USER_EMAIL,
            first_name=VarStr.USER_NAME,
        ),
    )
    client.force_login(user)

    response = client.post(
        reverse("settings"),
        {
            "email": "new@mail.com",
            "first_name": "new_first_name",
        },
    )
    user.refresh_from_db()

    basic_asserts_reverse(response, "settings")
    assert user.email == "new@mail.com"
    assert user.first_name == "new_first_name"


def test_password_change(client: Client, basic_asserts_reverse: Callable) -> None:
    user = cast(User, UserFactory())
    user.set_password(VarStr.USER_PASSWORD)
    user.save()
    client.force_login(user)

    response = client.post(
        reverse("settings"),
        {
            "email": VarStr.USER_EMAIL,
            "current_password": VarStr.USER_PASSWORD,
            "new_password1": "newsecurepass123",
            "new_password2": "newsecurepass123",
        },
    )

    user.refresh_from_db()

    assert user.check_password("newsecurepass123")
    basic_asserts_reverse(response, "settings")

    session = client.session
    assert SESSION_KEY in session


def test_duplicate_email(client: Client, basic_asserts_template: Callable) -> None:
    UserFactory(email="existing@mail.com")
    user = cast(User, UserFactory(email=VarStr.USER_EMAIL))
    client.force_login(user)

    response = client.post(
        reverse("settings"),
        {
            "email": "existing@mail.com",
        },
    )

    user.refresh_from_db()
    assert user.email == VarStr.USER_EMAIL
    basic_asserts_template(response, "уже существует")


@pytest.mark.parametrize(
    ("current_password", "new_password1", "new_password2", "word"),
    (
        (
            "wrongpass",
            "newpass",
            "newpass",
            "Неверный текущий пароль",
        ),
        (
            VarStr.USER_PASSWORD,
            "newpass",
            "newpass1",
            "Пароли не совпадают",
        ),
    ),
)
def test_wrong_password(
    client: Client,
    basic_asserts_template: Callable,
    current_password: str,
    new_password1: str,
    new_password2: str,
    word: str,
):
    user = cast(User, UserFactory())
    user.set_password(VarStr.USER_PASSWORD)
    user.save()
    client.force_login(user)

    response = client.post(
        reverse("settings"),
        {
            "email": VarStr.USER_EMAIL,
            "current_password": current_password,
            "new_password1": new_password1,
            "new_password2": new_password2,
        },
    )

    user.refresh_from_db()
    assert not user.check_password(new_password1)
    basic_asserts_template(response, word)
