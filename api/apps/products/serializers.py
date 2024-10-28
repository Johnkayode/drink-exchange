from rest_framework import serializers
from api.apps.products.models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            "uid",
            "name",
        )
        read_only_fields = (
            "uid",
        )


class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "uid",
            "name",
            "business",
            "categories",
            "description",
            "sku_number",
            "base_price",
            "min_price",
            "max_price",
            "quantity",
            "is_available",
            "created_at",
        )
        read_only_fields = (
            "uid",
            "business",
            "created_at",
        )
        extra_kwargs = {'base_price': {'required': True}, 'description': {'required': False}}
        

    def create(self, validated_data):
        validated_data["business"] = self.context["request"].user.business
        categories_data = validated_data.pop('categories', [])
        instance = super().create(validated_data)

        for category_data in categories_data:
            category, __ = ProductCategory.objects.get_or_create(**category_data)
            instance.categories.add(category)

        return instance

    def update(self, instance, validated_data):
        instance =  super().update(instance, validated_data)
        categories_data = validated_data.pop('categories', [])
        categories = []
        for category_data in categories_data:
            category, __ = ProductCategory.objects.get_or_create(**category_data)
            categories.append(category)
        instance.categories.set(categories)
        return instance