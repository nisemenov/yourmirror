import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY

from tests.factories import UserFactory
from tests.values import VarStr

pytestmark = pytest.mark.django_db

User = get_user_model()


# VIEW
def test_render_view(client, basic_asserts_template):
    user = UserFactory()
    client.force_login(user)

    response = client.get(reverse("settings"))

    basic_asserts_template(response, "Настройки")
    assert "form" in response.context


# FORMS
def test_update_user_data(client, basic_asserts_reverse):
    user = UserFactory(
        email=VarStr.USER_EMAIL,
        first_name=VarStr.USER_NAME,
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


def test_password_change(client, basic_asserts_reverse):
    user = UserFactory()
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


def test_duplicate_email(client, basic_asserts_template):
    UserFactory(email="existing@mail.com")
    user = UserFactory(email=VarStr.USER_EMAIL)
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
    client,
    basic_asserts_template,
    current_password,
    new_password1,
    new_password2,
    word,
):
    user = UserFactory()
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
