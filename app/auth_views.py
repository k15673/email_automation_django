from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_get(request):
    logout(request)
    return redirect("/accounts/login/")
