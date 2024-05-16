from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name=_('Пользователь'),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name=_('Товар'),
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Количество'))
    is_discount = models.BooleanField(default=False, verbose_name=_('Активна ли скидка'))

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.user.username
