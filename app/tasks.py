from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailLog


@shared_task
def send_scheduled_email(subject, message, recipient):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )

        EmailLog.objects.create(
            recipient=recipient,
            subject=subject,
            status="SENT (scheduled)",
            time=timezone.now(),
        )

    except Exception as e:
        EmailLog.objects.create(
            recipient=recipient,
            subject=subject,
            status=f"FAILED (scheduled): {type(e).__name__}",
            time=timezone.now(),
        )