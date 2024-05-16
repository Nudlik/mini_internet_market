import django_filters
from django.db.models import Q

from categories.models import Category
from products.models import Product


class ProductFilterSet(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    title_or_description = django_filters.CharFilter(
        method='title_or_description_',
        label='Поиск по заголовку или описанию'
    )
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    full_sub_category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        method='full_sub_category_',
        label='Поиск по категории и по подкатегории'
    )
    quantity__gte = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['name', 'category', 'title_or_description', 'full_sub_category']

    def title_or_description_(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))

    def full_sub_category_(self, queryset, name, value):
        return queryset.filter(Q(category__child_category=value) | Q(category=value))
