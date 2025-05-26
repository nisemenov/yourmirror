from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from profiles.models import FollowModel
from tests.factories import UserFactory

if TYPE_CHECKING:
    from django.test import Client
    from tests.conftest import BasicAssertsReverse


pytestmark = pytest.mark.django_db


def test_follow_model() -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    profile_1, profile_2 = user_1.profile, user_2.profile  # type: ignore[attr-defined]

    follow = FollowModel.objects.create(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    )
    assert profile_1.following.count() == 1
    assert profile_2.followers.count() == 1
    assert profile_1.is_following(profile_2) is True

    follow.delete()
    assert profile_1.following.count() == 0
    assert profile_2.followers.count() == 0
    assert profile_1.is_following(profile_2) is False


# VIEWS
def test_follow_create_view(
    client: Client, basic_asserts_reverse: BasicAssertsReverse
) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    profile_1, profile_2 = user_1.profile, user_2.profile  # type: ignore[attr-defined]

    client.force_login(user_1)

    url = reverse("follow_create", kwargs={"profile_id": profile_2.id})
    response = client.post(url, HTTP_REFERER=f"/wishlist/{profile_2.id}/")

    basic_asserts_reverse(
        cast(HttpResponseRedirect, response),
        "wishlist_profile",
        {"profile_id": profile_2.id},
    )
    assert FollowModel.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    ).exists()

    response = client.post(url, HTTP_REFERER=f"/wishlist/{profile_2.id}/")

    basic_asserts_reverse(
        cast(HttpResponseRedirect, response),
        "wishlist_profile",
        {"profile_id": profile_2.id},
    )
    assert not FollowModel.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    ).exists()


def test_follow_self_create_view() -> None:
    user = cast(User, UserFactory())
    profile = user.profile  # type: ignore[attr-defined]

    with pytest.raises(ValueError, match="User can't follow themselves"):
        FollowModel.objects.create(  # pyright: ignore[reportAttributeAccessIssue]
            follower=profile, following=profile
        )


def test_following_view(client: Client) -> None:
    user_1, user_2 = UserFactory.create_batch(2)
    profile_1, profile_2 = user_1.profile, user_2.profile  # type: ignore[attr-defined]

    client.force_login(user_1)

    FollowModel.objects.create(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    )

    response = client.get(reverse("following"))
    assert response.status_code == 200
    assert "profiles" in response.context
    assert list(response.context["profiles"]) == list(profile_1.following)


# ANONYMOUS VIEWS
@pytest.mark.parametrize(
    ("url_name", "profile_id"),
    (
        (
            "following",
            False,
        ),
        (
            "follow_create",
            True,
        ),
        (
            "settings",
            False,
        ),
    ),
)
def test_profile_views_login_req(
    client: Client,
    basic_asserts_reverse: BasicAssertsReverse,
    url_name: str,
    profile_id: bool,
) -> None:
    user = cast(User, UserFactory())
    profile = user.profile  # type: ignore[attr-defined]
    if profile_id:
        url = reverse(url_name, kwargs={"profile_id": profile.id})
    else:
        url = reverse(url_name)
    response = client.post(url)
    basic_asserts_reverse(cast(HttpResponseRedirect, response), "login")
