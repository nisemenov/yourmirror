import factory
from factory.declarations import Sequence, LazyAttribute

from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # for DeprecationWarning

    username = Sequence(lambda n: f"user_{n}")
    email = LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.django.Password("testpass123")
