import pytest

from django.urls import reverse

from profiles.models import FollowModel
from tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_follow_model():
    user_1, user_2 = UserFactory.create_batch(2)
    profile_1, profile_2 = user_1.profile, user_2.profile

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


def test_follow_create_view(client, basic_asserts_reverse):
    user_1, user_2 = UserFactory.create_batch(2)
    profile_1, profile_2 = user_1.profile, user_2.profile

    client.force_login(user_1)

    url = reverse("follow_create", kwargs={"profile_id": profile_2.id})
    response = client.post(url, HTTP_REFERER=f"/wishlist/{profile_2.id}/")

    basic_asserts_reverse(response, "wishlist_profile", {"profile_id": profile_2.id})
    assert FollowModel.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    ).exists()

    response = client.post(url, HTTP_REFERER=f"/wishlist/{profile_2.id}/")

    basic_asserts_reverse(response, "wishlist_profile", {"profile_id": profile_2.id})
    assert not FollowModel.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    ).exists()


def test_follow_self_create_view():
    profile = UserFactory().profile

    with pytest.raises(ValueError, match="User can't follow themselves"):
        FollowModel.objects.create(  # pyright: ignore[reportAttributeAccessIssue]
            follower=profile, following=profile
        )


def test_following_view(client):
    user_1, user_2 = UserFactory.create_batch(2)
    profile_1, profile_2 = user_1.profile, user_2.profile

    client.force_login(user_1)

    FollowModel.objects.create(  # pyright: ignore[reportAttributeAccessIssue]
        follower=profile_1, following=profile_2
    )

    response = client.get(reverse("following"))
    assert response.status_code == 200
    assert "profiles" in response.context
    assert list(response.context["profiles"]) == list(profile_1.following)
