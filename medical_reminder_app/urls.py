from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("firebase/", include("firebase_users.urls")),
    path('api/accounts/', include('accounts.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
    path('api/reminders/', include('reminders.urls')),
]
