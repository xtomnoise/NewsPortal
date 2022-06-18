from django.db import models
from django.db.models import Sum, Count, Max
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_r = self.posts.aggregate(Sum('rating')).get('rating__sum')
        self_comm_r = self.user.comment_set.aggregate(s=Sum('rating')).get('s')
        others_comm_r = self.posts.aggregate(s=Sum('comment__rating')).get('s')
        self.rating = 3 * posts_r + self_comm_r + others_comm_r
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    POSTKINDS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    category = models.ManyToManyField('Category', through='PostCategory', default=None)

    post_kind = models.CharField(max_length=2,
                                 choices=POSTKINDS,
                                 default=article)
    time_create = models.DateTimeField(auto_now=True)
    date_create = time_create.strftime("%d-%b-%y")
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
        if len(self.text) >= 124:
            return f'{self.text[:124]}...'
        else:
            return self.text


class PostCategory(models.Model):
    post = models.Forei10gnKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, )

    time_create = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    text = models.TextField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()