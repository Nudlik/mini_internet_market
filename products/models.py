from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Цена'))
    discount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Скидочная цена'))
    quantity = models.PositiveIntegerField(verbose_name=_('Количество'))
    description = models.TextField(verbose_name=_('Описание'))
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория')
    )
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('Владелец'),
    )

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        ordering = ['id']

    def __str__(self):
        return self.name
