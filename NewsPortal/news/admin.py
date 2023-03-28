from django.contrib import admin
from .models import Category, Post, CategorySubscribers, Author

def like_post(modeladmin, request, queryset):
    for q in queryset:
        q.rating += 1
        q.save()
like_post.short_description = 'Поставить лайк'


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'rating', 'author', 'post_kind', 'time_create')
    list_filter = ('author', 'post_kind')
    actions = [like_post]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(CategorySubscribers)
admin.site.register(Author)