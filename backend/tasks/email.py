import uuid
from celery import Task, shared_task

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from wishitems.models import WishItemModel


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # type: ignore[misc]
def send_confirmation_email(self: Task, email: str, confirmation_url: str) -> None:
    try:
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Пожалуйста, подтвердите вашу регистрацию, перейдя по ссылке: {confirmation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # type: ignore[misc]
def send_first_reservation_email(
    self: Task,
    email: str,
    confirmation_url: str,
) -> None:
    try:
        html_message = render_to_string(
            "emails/confirm_first_reservation.html",
            {
                "confirmation_url": confirmation_url,
            },
        )

        send_mail(
            subject="Подтверждение почты",
            message=f"Пожалуйста, подтвердите вашу почту, перейдя по ссылке: {confirmation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message,
        )
    except Exception as e:
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # type: ignore[misc]
def send_reservation_email(self: Task, email: str, wishitem_id: uuid.UUID) -> None:
    try:
        wishitem = WishItemModel.objects.get(id=wishitem_id)
        wishitem_url = f"{settings.FULL_DOMAIN}/wishitem/{wishitem.id}"
        wishlist_url = f"{settings.FULL_DOMAIN}/wishlist/{wishitem.profile.id}"
        register_url = f"{settings.FULL_DOMAIN}/register"
        html_message = render_to_string(
            "emails/reservation_email.html",
            {
                "wishlist_url": wishlist_url,
                "wishitem_url": wishitem_url,
                "register_url": register_url,
                "title": wishitem.title,
                "profile": wishitem.profile.user.first_name,
            },
        )

        send_mail(
            subject=wishitem.title,
            message=f"Вы только что зарезервировали желание: {wishitem_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message,
        )
    except Exception as e:
        raise self.retry(exc=e)
