from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from carts.models import Cart
from products.serializers import ProductSerializer


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=False)
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'product',
            'quantity',
            'price',
            'total_price',
            'is_discount',
        ]

    def get_product(self, obj):
        return obj.product.name

    def get_price(self, obj):
        if obj.is_discount:
            return obj.quantity * obj.product.discount
        return obj.quantity * obj.product.price

    def get_total_price(self, obj):
        if obj.is_discount:
            return obj.product.discount
        return obj.product.price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id',
            'product',
            'quantity',
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                _('Количество должно быть больше нуля')
            )
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance
