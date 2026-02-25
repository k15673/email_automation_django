from app.auth_views import logout_get
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path,include

urlpatterns = [    path('accounts/logout/', logout_get, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

 path('admin/',admin.site.urls),
 path('',include('app.urls'))
]