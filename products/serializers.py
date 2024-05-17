from rest_framework import serializers

from categories.serializers import CategoryProductSerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'discount',
            'quantity',
            'description',
            'category',
        ]

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError('Category is required')
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'discount',
            'quantity',
            'description',
            'category',
        ]

    def get_category(self, obj):
        return obj.category.name if hasattr(obj.category, 'name') else None
