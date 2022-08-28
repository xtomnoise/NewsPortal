import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mail_every_monday_8am': {
        'task': 'news.tasks.week_news_mailing',
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),
    },
}
