import json
import logging

import stripe
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.decorators import action as _action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from carts.models import Cart
from carts.serializers import CartListSerializer, CartSerializer
from carts.services.mail_sender import send_mail_purchase
from carts.services.payment import stripe_checkout_session
from config import settings

logger = logging.getLogger(__name__)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    choice_serializer = {
        'list': CartListSerializer,
        'retrieve': CartListSerializer,
    }

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.count()

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

        qs = qs.first()
        domain_url = '/'.join(self.request.build_absolute_uri().rsplit('/')[:3])
        session = stripe_checkout_session(
            price=qs.product.price,
            name=qs.product.name,
            description=qs.product.description,
            quantity=qs.quantity,
            domain_url=domain_url,
        )

        logger.debug(json.dumps(session, indent=4, ensure_ascii=False))

        # здесь будет точка входа для вебхука

        payment_link = session.url
        send_mail_purchase.delay(
            title=f'Оплата покупки',
            message=f'Покупка {qs.quantity} ед. {qs.product.name} цена за ед. {qs.product.price}\n'
                    f'Ссылка: {payment_link}',
            email=request.user.email,
        )
        return Response(
            data={'success': _('Мы выслали вам письмо на почту с сылкой для оплаты покупки')},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook(request):
    """ Обработка событий stripe """
    try:
        event = None
        payload = request.body
        sig_header = request.headers['STRIPE_SIGNATURE']
    except KeyError as e:
        logger.error(e)
        return Response({'error': 'Вебхук для страйпа'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        logger.error(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        logger.error(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Handle the event
    logger.debug('Unhandled event type {}'.format(event['type']))
    if event['type'] == 'checkout.session.completed':
        # логика вычета количества таваров из корзины и из общего кол-ва товаров
        # возможность записи покупки, логирование в базу и тд.
        print(event)

    return Response({'success': True})


@api_view(['GET'])
def success(request):
    """ Успешная оплата """

    logger.info('Успешная оплата')
    return Response({'success': True})


@api_view(['GET'])
def canceled(request):
    """ Отмена оплаты """

    logger.info('Отмена оплаты')
    return Response({'canceled': True})
