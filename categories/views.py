from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
