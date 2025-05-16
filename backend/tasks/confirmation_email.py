from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings


@shared_task  # type: ignore[misc]
def send_confirmation_email(email: str, confirmation_url: str) -> None:
    send_mail(
        subject="Подтверждение регистрации",
        message=f"Пожалуйста, подтвердите вашу регистрацию, перейдя по ссылке: {confirmation_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
