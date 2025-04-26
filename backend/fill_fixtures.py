import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telewish.settings")
django.setup()


def main():
    import factory
    from profiles.models import ProfileModel
    from tests.factories import WishItemFactory, faker_image_file

    for profile in ProfileModel.objects.all():
        WishItemFactory.create_batch(
            size=5,
            profile=profile,
            picture=factory.LazyFunction(faker_image_file),
        )


if __name__ == "__main__":
    main()
