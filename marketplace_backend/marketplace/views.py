from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, CreateOrderSerializer
from core.permissions import IsMerchantAndSubscribed
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsMerchantAndSubscribed()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Customers see active products from active merchants
        # Merchants see their own products
        user = self.request.user
        if user.role == 'MERCHANT':
             return Product.objects.filter(merchant=user)
        
        # Customers logic:
        # Prompt: "Customer ... Browse active merchants ONLY ... Browse merchant products"
        # "Merchant CANNOT ... Appear to customers UNTIL Subscription status = approved"
        
        return Product.objects.filter(is_active=True, merchant__merchant_profile__is_subscribed=True)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'MERCHANT':
            return Order.objects.filter(merchant=user).order_by('-created_at')
        return Order.objects.filter(customer=user).order_by('-created_at')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if request.user.role != 'CUSTOMER':
             return Response({"error": "Only customers can place orders"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        merchant_id = serializer.validated_data['merchant_id']
        items_data = serializer.validated_data['items']
        
        try:
             merchant = User.objects.get(pk=merchant_id, role='MERCHANT')
        except User.DoesNotExist:
             return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Verify strict subscription check (Frontend should know, but backend must enforce)
        if not hasattr(merchant, 'merchant_profile') or not merchant.merchant_profile.is_subscribed:
             return Response({"error": "Merchant is not active"}, status=status.HTTP_403_FORBIDDEN)
             
        order = Order.objects.create(customer=request.user, merchant=merchant)
        
        total_items = 0
        for item in items_data:
             try:
                 product = Product.objects.get(pk=item['product_id'], merchant=merchant)
                 OrderItem.objects.create(
                     order=order,
                     product=product,
                     quantity=item['quantity'],
                     price=product.price
                 )
                 total_items += 1
             except Product.DoesNotExist:
                 return Response({"error": f"Product {item['product_id']} not found or does not belong to merchant"}, status=status.HTTP_400_BAD_REQUEST)
        
        if total_items == 0:
             transaction.set_rollback(True)
             return Response({"error": "No valid products in order"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
