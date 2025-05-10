from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from django.urls import reverse


if TYPE_CHECKING:
    from collections.abc import Callable
    from django.http import HttpResponse


pytest_plugins = ["tests.factories"]


@pytest.fixture
def basic_asserts_reverse() -> Callable[[HttpResponse, str, dict], None]:
    def asserts(response: HttpResponse, reverse_url: str, url_kwargs: dict | None = {}):
        assert response.status_code == 302
        assert reverse(reverse_url, kwargs=url_kwargs) in response.url

    return asserts


@pytest.fixture
def basic_asserts_template() -> Callable[
    [
        HttpResponse,
        str,
    ],
    None,
]:
    def asserts(response: HttpResponse, word: str):
        assert response.status_code == 200
        assert word.encode() in response.content

    return asserts


@pytest.fixture
def basic_asserts_template_with_not() -> Callable[
    [
        HttpResponse,
        str,
    ],
    None,
]:
    def asserts(response: HttpResponse, word: str):
        assert response.status_code == 200
        assert word.encode() not in response.content

    return asserts
