from __future__ import annotations

from typing import Any, Protocol, cast, runtime_checkable

import pytest

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


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
    def asserts(response: HttpResponse, word: str) -> None:
        assert response.status_code == 200
        assert word.encode() in response.content

    return asserts


@pytest.fixture
def basic_asserts_template_with_not() -> BasicAssertsTemplate:
    def asserts(response: HttpResponse, word: str) -> None:
        assert response.status_code == 200
        assert word.encode() not in response.content

    return asserts
