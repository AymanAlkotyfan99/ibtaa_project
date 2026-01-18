from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MerchantSubscription
from .serializers import MerchantSubscriptionSerializer, SubscriptionPlanSerializer
from core.models import AdminSettings
from django.utils import timezone
from datetime import timedelta
from services.subscription_service import SubscriptionService

class SubscriptionPlansView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        settings = AdminSettings.load()
        serializer = SubscriptionPlanSerializer(settings)
        return Response(serializer.data)

class MerchantSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return MerchantSubscription.objects.all().order_by('-created_at')
        elif user.role == 'MERCHANT':
            return MerchantSubscription.objects.filter(merchant=user).order_by('-created_at')
        return MerchantSubscription.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != 'MERCHANT':
            raise permissions.PermissionDenied("Only merchants can subscribe.")
        serializer.save(merchant=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        sub = self.get_object()
        if sub.status != 'PENDING':
            return Response({"error": "Subscription not pending"}, status=status.HTTP_400_BAD_REQUEST)
        
        SubscriptionService.approve_subscription(sub)
        
        return Response(MerchantSubscriptionSerializer(sub).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        sub = self.get_object()
        if sub.status != 'PENDING':
             return Response({"error": "Subscription not pending"}, status=status.HTTP_400_BAD_REQUEST)
             
        reason = request.data.get('reason', 'No reason provided')
        SubscriptionService.reject_subscription(sub, reason)
        
        return Response(MerchantSubscriptionSerializer(sub).data)
