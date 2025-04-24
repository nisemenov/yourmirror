from django.urls import reverse
import pytest


pytest_plugins = ["tests.factories"]


@pytest.fixture
def basic_asserts_reverse():
    def asserts(response, reverse_url: str, url_kwargs={}):
        assert response.status_code == 302
        assert reverse(reverse_url, kwargs=url_kwargs) in response.url

    return asserts


@pytest.fixture
def basic_asserts_template():
    def asserts(response, word):
        assert response.status_code == 200
        assert word.encode() in response.content

    return asserts


@pytest.fixture
def basic_asserts_template_with_not():
    def asserts(response, word):
        assert response.status_code == 200
        assert word.encode() not in response.content

    return asserts
