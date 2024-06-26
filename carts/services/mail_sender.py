from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_mail_purchase(title, message, email):
    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
