from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, cast, runtime_checkable

import pytest

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from services.models import RegistrationTokenModel
from tests.values import VarStr


pytest_plugins = ["tests.factories"]


@runtime_checkable
class BasicAssertsReverse(Protocol):
    def __call__(
        self,
        response: HttpResponse,
        reverse_url: str,
        url_kwargs: dict[str, Any] | None = ...,
    ) -> None: ...


@runtime_checkable
class BasicAssertsTemplate(Protocol):
    def __call__(
        self,
        response: HttpResponse,
        word: str,
        status_code: int = ...,
    ) -> None: ...


@runtime_checkable
class AssertsUser(Protocol):
    def __call__(
        self,
        users: QuerySet[User],
        basic_fields: bool = ...,
        profile: bool = ...,
    ) -> None: ...


@pytest.fixture
def basic_asserts_reverse() -> BasicAssertsReverse:
    def asserts(
        response: HttpResponse,
        reverse_url: str,
        url_kwargs: dict[str, Any] | None = None,
    ) -> None:
        response = cast(HttpResponseRedirect, response)
        assert response.status_code == 302
        assert reverse(reverse_url, kwargs=url_kwargs) in response.url

    return asserts


@pytest.fixture
def basic_asserts_template() -> BasicAssertsTemplate:
    def asserts(response: HttpResponse, word: str, status_code: int = 200) -> None:
        assert response.status_code == status_code
        assert word.encode() in response.content

    return asserts


@pytest.fixture
def basic_asserts_template_with_not() -> BasicAssertsTemplate:
    def asserts(response: HttpResponse, word: str, status_code: int = 200) -> None:
        assert response.status_code == status_code
        assert word.encode() not in response.content

    return asserts


@pytest.fixture
def asserts_registration_token() -> Callable[[QuerySet[RegistrationTokenModel]], None]:
    def asserts(reg_tokens: QuerySet[RegistrationTokenModel]) -> None:
        assert reg_tokens.exists()
        assert len(reg_tokens) == 1
        assert not reg_tokens[0].is_expired

    return asserts


@pytest.fixture
def asserts_user() -> AssertsUser:
    def asserts(
        users: QuerySet[User],
        basic_fields: bool = False,
        profile: bool = False,
    ) -> None:
        assert users.exists()
        assert len(users) == 1
        if basic_fields:
            assert users[0].email == VarStr.USER_EMAIL
            assert users[0].username == VarStr.USER_EMAIL
        if profile:
            assert users[0].profile.id

    return asserts
