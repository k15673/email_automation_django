from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reports/pdf/", views.pdf_report, name="pdf_report"),
    path("report/", views.pdf_report, name="report"),
    path("bulk/", views.bulk_email, name="bulk"), 
]



