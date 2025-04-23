import factory
from factory.declarations import Sequence, LazyAttribute

from django.contrib.auth.models import User

from wishitems.models import WishItemModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # for DeprecationWarning

    username = Sequence(lambda n: f"user_{n}")
    email = LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.django.Password("testpass123")


class WishItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishItemModel

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text", max_nb_chars=100)
    link = factory.Faker("url")
    is_private = False

    profile = factory.LazyAttribute(lambda _: UserFactory().profile)
