import stripe
from rest_framework.reverse import reverse

from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
WEB_HOOK_DESCRIPTION = 'checkout.session.completed'


def stripe_checkout_session(
        price: str,
        name: str,
        description: str,
        quantity: int,
        domain_url: str,
) -> stripe.checkout.Session:
    """ Создание сеанса stripe """

    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': int(price) * 100,
                    'product_data': {
                        'name': name,
                        'description': description,
                    }
                },
                'quantity': quantity,
            },
        ],
        mode='payment',
        success_url=domain_url + reverse('carts:success'),
        cancel_url=domain_url + reverse('carts:canceled'),
    )
    return session


def create_webhook() -> dict:
    """ Создание webhook """

    try:
        web_hook_url = reverse('users:webhook')
        web_hook = get_webhook()
        if web_hook is None:
            web_hook = stripe.WebhookEndpoint.create(
                enabled_events=['checkout.session.completed'],
                url=f'{settings.STRIPE_WEBHOOK_URL}{web_hook_url}',
                description='checkout.session.completed',
            )
        return web_hook
    except Exception as e:
        print(f'Ошибка при создании webhook {e}')


def get_webhook() -> dict | None:
    """ Получение webhook """

    try:
        web_hooks: dict = stripe.WebhookEndpoint.list()
        for web_hook in web_hooks['data']:
            if web_hook.get('description') == WEB_HOOK_DESCRIPTION:
                return web_hook
        return None
    except Exception as e:
        print(f'Ошибка при получении webhook {e}')
