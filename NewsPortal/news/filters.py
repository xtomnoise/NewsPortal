from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
import django.forms


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Tag',
        empty_label='All',
    )
    time_create = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # 'time_create': ['gt']
            # количество товаров должно быть больше или равно
            # 'category': ['exact'],
        }
