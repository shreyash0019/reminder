import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medical_reminder_app.settings")

app = Celery("medical_reminder_app")

# Load settings from Django settings, using CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py inside all installed apps
app.autodiscover_tasks()

# ✅ Celery Beat schedule (for periodic tasks)
app.conf.beat_schedule = {
    "send-reminders-every-minute": {
        "task": "reminders.tasks.send_reminder_notifications",
        "schedule": crontab(minute="*"),  # har 1 min
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
