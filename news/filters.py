from django import forms
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Post, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='любая'
    )
    text = CharFilter(field_name='text', label='Текст содержит', lookup_expr='icontains')
    data = DateFilter(field_name='time_in', label='Дата', lookup_expr='gt')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = ['text', 'time_in']
