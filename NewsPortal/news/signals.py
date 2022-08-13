from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import PostCategory, CategorySubscribers

from django.template.loader import render_to_string

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_new_cat_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.category.all():
            for sub in CategorySubscribers.objects.filter(category=cat):
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.text,
                    from_email='auddrct@yandex.ru',
                    to=[sub.subscribers.email],
                )

                html_content = render_to_string(
                    'email/post_created.html',
                    {
                        'post': instance,
                        'recipient': sub.subscribers.email,
                        'username': sub.subscribers.username
                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()
