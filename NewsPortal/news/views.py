from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm


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

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post_create'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post_update'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')