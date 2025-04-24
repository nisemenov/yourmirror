import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telewish.settings")
django.setup()


def main():
    from profiles.models import ProfileModel
    from tests.factories import WishItemFactory

    for profile in ProfileModel.objects.all():
        WishItemFactory.create_batch(size=5, profile=profile)


if __name__ == "__main__":
    main()
