from django.urls import path
from . import views

urlpatterns = [
    path('', views.reminder_list, name='reminder_list'),
    path('create/', views.create_reminder, name='create_reminder'),
    path('mark_taken/<int:reminder_id>/', views.mark_taken, name='mark_taken'),
    path('due/', views.due_reminders, name='due_reminders'),
]
