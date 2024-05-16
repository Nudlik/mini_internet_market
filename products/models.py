from django.db import models

from categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Скидочная цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
