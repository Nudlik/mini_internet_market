from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.decorators import action as _action
from rest_framework.response import Response

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

    @_action(detail=True, methods=['GET'])
    def payment(self, request, pk):
        qs = self.get_queryset().filter(pk=pk)
        if not qs.exists():
            return Response(
                data={'error': _('Такой корзины у вас нет')},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            data={'success': _('Мы выслали вам письмо на почту с сылкой для оплаты покупки')},
            status=status.HTTP_200_OK
        )
