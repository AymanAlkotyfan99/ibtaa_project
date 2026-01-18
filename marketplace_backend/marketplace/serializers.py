from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    merchant_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'is_active', 'merchant', 'merchant_name', 'created_at']
        read_only_fields = ['merchant', 'created_at', 'merchant_name']

    def get_merchant_name(self, obj):
        if hasattr(obj.merchant, 'merchant_profile'):
            return obj.merchant.merchant_profile.business_name
        return obj.merchant.email

    def create(self, validated_data):
        validated_data['merchant'] = self.context['request'].user
        return super().create(validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = ['price'] 

class OrderCreateItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    merchant_name = serializers.ReadOnlyField(source='merchant.merchant_profile.business_name')
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'merchant', 'merchant_name', 'status', 'items', 'created_at']
        read_only_fields = ['customer', 'merchant', 'status', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    merchant_id = serializers.IntegerField()
    items = OrderCreateItemSerializer(many=True)
