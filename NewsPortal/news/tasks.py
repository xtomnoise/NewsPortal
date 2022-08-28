from celery import shared_task
from .models import Post, CategorySubscribers, Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta


@shared_task
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


@shared_task
def task_notify_new_cat_post(pcid):
    post = Post.objects.get(pk=pcid)
    for cat in post.category.all():
        for sub in CategorySubscribers.objects.filter(category=cat):
            msg = EmailMultiAlternatives(
                subject=post.title,
                body=post.text,
                from_email='auddrct@yandex.ru',
                to=[sub.subscribers.email],
            )

            html_content = render_to_string(
                'email/post_created.html',
                {
                    'post': post,
                    'recipient': sub.subscribers.email,
                    'username': sub.subscribers.username
                }
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()
