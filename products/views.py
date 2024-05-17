from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from products.filters import ProductFilterSet
from products.models import Product
from products.permissions import IsOwner
from products.serializers import ProductSerializer, ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilterSet
    perms_methods = {
        'list': [AllowAny],
        'update': [IsOwner | IsAdminUser],
        'partial_update': [IsOwner | IsAdminUser],
        'destroy': [IsOwner | IsAdminUser],
    }
    choice_serializer = {
        'list': ProductListSerializer,
        'retrieve': ProductListSerializer,
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        return self.choice_serializer.get(self.action, self.serializer_class)
