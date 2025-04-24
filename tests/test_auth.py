import pytest

from django.urls import reverse

from profiles.forms import EmailRegistrationForm
from tests.factories import UserFactory
from tests.values import VarStr


pytestmark = pytest.mark.django_db


def test_register_view(client, basic_asserts_reverse):
    url = reverse("register")
    data = {
        "email": VarStr.USER_EMAIL,
        "password1": VarStr.USER_PASSWORD1,
        "password2": VarStr.USER_PASSWORD2,
    }
    response = client.post(url, data)
    basic_asserts_reverse(response, "wishlist_me")


def test_login_view(client, basic_asserts_reverse):
    user = UserFactory()
    url = reverse("login")
    data = {
        "username": user.username,
        "password": "testpass123",
    }
    response = client.post(url, data)
    basic_asserts_reverse(response, "wishlist_me")


def test_email_registration_form_valid():
    form_data = {
        "email": VarStr.USER_EMAIL,
        "password1": VarStr.USER_PASSWORD1,
        "password2": VarStr.USER_PASSWORD2,
    }
    form = EmailRegistrationForm(data=form_data)
    assert form.is_valid()

    user = form.save()
    assert user.email == VarStr.USER_EMAIL
    assert user.username == VarStr.USER_EMAIL
    assert user.profile.id
