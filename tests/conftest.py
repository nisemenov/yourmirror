from django.urls import reverse
import pytest


pytest_plugins = ["tests.factories"]


@pytest.fixture
def basic_asserts_login():
    def asserts(response, reverse_url, url_kwargs={}):
        assert response.status_code == 302
        assert response.url == reverse(reverse_url, kwargs=url_kwargs)

    return asserts
