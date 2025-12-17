from django.urls import path
from . import views

urlpatterns = [
    path("", views.reminder_list),
    path("create/", views.create_reminder),
    path("mark-taken/<int:reminder_id>/", views.mark_taken),
    path("due/", views.due_reminders),
]
