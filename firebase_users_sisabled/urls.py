from django.urls import path
from .views import list_users, create_reminder, list_reminders

urlpatterns = [
    path("users/", list_users, name="list_users"),
    path("reminders/create/", create_reminder, name="create_reminder"),
    path("reminders/", list_reminders, name="list_reminders"),
]
