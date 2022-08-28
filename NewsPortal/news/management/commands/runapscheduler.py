import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ...models import Post, CategorySubscribers, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def week_news_mailing():
    for cat in Category.objects.all():
        for sub in CategorySubscribers.objects.filter(category=cat):
            d_to = datetime.now() + timedelta(days=1)
            d_from = d_to - timedelta(days=7)
            posts = Post.objects.filter(
                category=cat,
                time_create__range=(d_from, d_to),
            )
            print('ПОСТЫ:', posts)
            print('ЮЗЕР:', sub.subscribers.username)
            msg = EmailMultiAlternatives(
                subject=f'Привет,{sub.subscribers.username}! новые статьи в {cat}!',
                from_email='auddrct@yandex.ru',
                to=[sub.subscribers.email],
            )

            html_content = render_to_string(
                'email/week_news_mailing.html',
                {
                    'recipient': sub.subscribers.email,
                    'username': sub.subscribers.username,
                    'posts': posts,
                }
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        # добавляем работу нашему задачнику
        scheduler.add_job(
            week_news_mailing,
            trigger=CronTrigger(day_of_week="sun", hour="00", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
