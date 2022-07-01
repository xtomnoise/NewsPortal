from django.db import models
from django.db.models import Sum, Count, Max
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_r = self.posts.aggregate(s=Sum('rating'))['s']
        self_comms_r = self.user.comment_set.aggregate(s=Sum('rating'))['s']
        other_comms_r = self.posts.aggregate(s=Sum('comment__rating'))['s']
        self.rating = posts_r * 3 + self_comms_r + other_comms_r
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)


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
