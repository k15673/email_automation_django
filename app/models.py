from django.db import models
from django.contrib.auth.models import User

class EmailLog(models.Model):
    recipient=models.EmailField()
    subject=models.CharField(max_length=200)
    status=models.CharField(max_length=50)
    time=models.DateTimeField(auto_now_add=True)