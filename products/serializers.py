from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(source='category.name', read_only=True)

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
        return obj.category.name

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance
