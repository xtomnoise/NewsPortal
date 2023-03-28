import time

from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, User, Category, Author
from datetime import datetime, timedelta
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.shortcuts import redirect

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.cache import cache

import logging


# logger = logging.getLogger('django')


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-time_create'
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset

        return context


class PostCreate(PermissionRequiredMixin,
                 LoginRequiredMixin,
                 CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    context_object_name = 'post_create'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        # post = form.save(commit=False)
        # post.author = self.request.user.author
        auth = self.request.user.author
        form.instance.author = auth
        d_from = datetime.now().date()
        d_to = d_from + timedelta(days=1)
        posts = Post.objects.filter(
            author=auth,
            time_create__range=(d_from, d_to),
        )
        print(posts)

        if len(posts) >= 10:
            return redirect('posts_limit')
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     user = User.objects.get(id=request.user.id)
    #     author = Author.objects.get(user=user)
    #     text = request.text
    #     title = request.title
    #     d_from = datetime.now().date()
    #     d_to = d_from + timedelta(days=1)
    #     posts = Post.objects.filter(author=author, time_create__range=(d_from, d_to))
    #     if len(posts) >= 3:
    #         return redirect('limit/')
    #     return redirect('success/')


class PostsLimit(TemplateView):
    template_name = 'posts_limit.html'


class PostUpdate(PermissionRequiredMixin,
                 LoginRequiredMixin,
                 UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    context_object_name = 'post_update'
    permission_required = ('news.change_post',)


class PostDelete(PermissionRequiredMixin,
                 LoginRequiredMixin,
                 DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)


class CategoriesList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories'


def unsubscribe(request):
    user = request.user
    id = request.GET['pk']
    category = Category.objects.get(pk=id)
    category.subscribers.remove(user)

    return redirect(request.META.get('HTTP_REFERER'))


def subscribe(request):
    user = request.user
    id = request.GET['pk']
    category = Category.objects.get(pk=id)
    category.subscribers.add(user)

    return redirect(request.META.get('HTTP_REFERER'))
