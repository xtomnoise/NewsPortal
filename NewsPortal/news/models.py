from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.cache import cache

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_r = self.posts.aggregate(s=Sum('rating'))['s']
        self_comms_r = self.user.comment_set.aggregate(s=Sum('rating'))['s']
        other_comms_r = self.posts.aggregate(s=Sum('comment__rating'))['s']
        self.rating = posts_r * 3 + self_comms_r + other_comms_r
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers', blank=True)

    def __str__(self):
        return f'{self.category_name}'


class CategorySubscribers(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.category} - {self.subscribers}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    POSTKINDS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    category = models.ManyToManyField('Category', through='PostCategory')

    post_kind = models.CharField(max_length=2,
                                 choices=POSTKINDS,
                                 default=article)
    time_create = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def preview(self):
        return f'{self.text[:123]}...'

    def __str__(self):
        return f'{self.title}: {self.time_create.strftime("%d-%b-%y")}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    time_create = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    text = models.TextField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()
