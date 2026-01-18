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
        plans = []
        subscription_plans = settings.get_subscription_plans()
        for i, plan in enumerate(subscription_plans or []):
            plan_data = {
                'id': i,
                'name': plan.get('name', f'Plan {i}'),
                'price': plan.get('price', 0),
                'duration_days': plan.get('duration_days', 30),
                'max_products': plan.get('max_products'),
                'description': plan.get('description', ''),
            }
            plans.append(plan_data)
        return Response(plans)

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

    def partial_update(self, request, *args, **kwargs):
        """Allow admins to approve or reject subscriptions"""
        if request.user.role != 'ADMIN':
            return Response({"error": "Only admins can update subscriptions"}, status=status.HTTP_403_FORBIDDEN)
        
        subscription = self.get_object()
        status_update = request.data.get('status')
        
        if status_update == 'APPROVED':
            SubscriptionService.approve_subscription(subscription)
        elif status_update == 'REJECTED':
            reason = request.data.get('rejection_reason', 'No reason provided')
            SubscriptionService.reject_subscription(subscription, reason)
        
        return Response(MerchantSubscriptionSerializer(subscription).data)

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
