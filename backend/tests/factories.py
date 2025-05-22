import factory
from faker import Faker

from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from services.models import RegistrationTokenModel
from wishitems.models import WishItemModel

from tests.values import VarStr


fake = Faker()


class RegistrationTokenFactory(
    factory.django.DjangoModelFactory[RegistrationTokenModel]
):
    class Meta:
        model = RegistrationTokenModel


class UserFactory(factory.django.DjangoModelFactory[User]):
    class Meta:
        model = User
        skip_postgeneration_save = True  # for DeprecationWarning

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.django.Password(VarStr.USER_PASSWORD)


def faker_image_file():
    image_bytes = fake.image(image_format="png", hue="blue", luminosity="light")
    return ContentFile(image_bytes, "faker.png")


class WishItemFactory(factory.django.DjangoModelFactory[WishItemModel]):
    class Meta:
        model = WishItemModel

    title = factory.Faker("sentence", nb_words=3, locale="ru_RU")
    description = factory.Faker("text", max_nb_chars=100, locale="ru_RU")
    link = factory.Faker("url")

    profile = factory.LazyAttribute(lambda _: UserFactory().profile)

    is_private = False
