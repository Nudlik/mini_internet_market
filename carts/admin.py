from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'display_price', 'total_price']

    @admin.display(description=_('Общая цена'))
    def total_price(self, cart):
        if cart.is_discount:
            return cart.quantity * cart.product.discount
        return cart.quantity * cart.product.price

    @admin.display(description=_('Цена за 1 ед.'))
    def display_price(self, cart):
        if cart.is_discount:
            return cart.product.discount
        return cart.product.price
