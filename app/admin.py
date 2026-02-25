from django.contrib import admin
from .models import EmailLog

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "subject", "status", "time")
    search_fields = ("recipient", "subject", "status")
    list_filter = ("status",)
