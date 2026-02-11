from django.urls import path
from . import views

urlpatterns = [
    path('', views.reminder_list, name='reminder_list'),
    path('create/', views.create_reminder, name='create_reminder'),

    # Mark as taken
    path('mark-taken/<int:reminder_id>/', views.mark_taken, name='mark_taken'),

    # Get due reminders (list for frontend)
    path('due/', views.get_due_reminders, name='get_due_reminders'),

    # Get due reminder count
    path('due/count/', views.due_reminder_count, name='due_reminder_count'),

    # Trigger sending notifications
    path('send-due/', views.send_due_notifications, name='send_due_notifications'),
]
