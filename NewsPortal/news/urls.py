from django.urls import path
# Импортируем созданное нами представление
from .views import (
    PostList, PostDetail, PostSearch, PostCreate,
    PostUpdate, PostDelete, CategoriesList, subscribe, unsubscribe,
    PostsLimit,
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='post_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/', CategoriesList.as_view(), name='categories'),
    path('categories/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('categories/subscribe/', subscribe, name='subscribe'),
    path('limit/', PostsLimit.as_view(), name='posts_limit'),
]
