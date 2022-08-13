from django.contrib import admin
from .models import Category, Post, CategorySubscribers, Author

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(CategorySubscribers)
admin.site.register(Author)