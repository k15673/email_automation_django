from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

from .models import EmailLog
from .tasks import send_scheduled_email


def login_view(request):
    return render(request, "login.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def bulk_email(request):

    if request.method == "POST":

        recipients_raw = request.POST.get("recipients", "")
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        schedule_time = request.POST.get("schedule_time")

        recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

        if not recipients or not subject or not message:
            return HttpResponse("❌ Please fill recipients, subject, and message.")

        scheduled_count = 0
        sent_count = 0

        for recipient in recipients:

            try:
                if schedule_time:
                    eta = timezone.make_aware(datetime.fromisoformat(schedule_time))

                    send_scheduled_email.apply_async(
                        args=[subject, message, recipient],
                        eta=eta
                    )

                    EmailLog.objects.create(
                        recipient=recipient,
                        subject=subject,
                        status="SCHEDULED",
                        time=timezone.now(),
                    )

                    scheduled_count += 1

                else:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient],
                        fail_silently=False,
                    )

                    EmailLog.objects.create(
                        recipient=recipient,
                        subject=subject,
                        status="SENT",
                        time=timezone.now(),
                    )

                    sent_count += 1

            except Exception as e:
                EmailLog.objects.create(
                    recipient=recipient,
                    subject=subject,
                    status=f"FAILED: {type(e).__name__}",
                    time=timezone.now(),
                )

        return HttpResponse(
            f"✅ Sent {sent_count} emails, Scheduled {scheduled_count}. Check Admin → EmailLog."
        )

    return render(request, "bulk.html")


@login_required
def pdf_report(request):

    response = HttpResponse(content_type="application/pdf")

    if request.GET.get("download") == "1":
        response["Content-Disposition"] = 'attachment; filename="email_report.pdf"'
    else:
        response["Content-Disposition"] = 'inline; filename="email_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    logs = EmailLog.objects.all().order_by("-time")

    data = [["To", "Subject", "Status", "Time"]]
    for log in logs:
        data.append([
            log.recipient,
            log.subject,
            log.status,
            str(log.time),
        ])

    table = Table(data)
    doc.build([table])

    return response
