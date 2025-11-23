from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Medical Reminder API is running!"})

urlpatterns = [
    path('', home),   # 👈 add this line
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
    path('api/reminders/', include('reminders.urls')),
]
