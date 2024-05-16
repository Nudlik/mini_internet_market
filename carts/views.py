from rest_framework import viewsets

from carts.models import Cart
from carts.serializers import CartListSerializer, CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    choice_serializer = {
        'list': CartListSerializer,
        'retrieve': CartListSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.choice_serializer.get(self.action, self.serializer_class)
