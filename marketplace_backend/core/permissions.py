from rest_framework import permissions
from django.utils import timezone
from subscriptions.models import MerchantSubscription

class IsMerchantAndSubscribed(permissions.BasePermission):
    """
    Allows access only to merchants with an active, approved subscription.
    """
    message = "Active subscription required."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role != 'MERCHANT':
            return False
            
        # Check for active subscription
        # Must be APPROVED and end_date >= now
        
        # Optimization: We could check profile.is_subscribed first, 
        # but to be strictly safely logic-driven we check the subscription record.
        # Actually, profile.is_subscribed is intended to be the cache.
        # But checking DB is safer for "STRICT" enforcement.
        
        active_sub = MerchantSubscription.objects.filter(
            merchant=request.user,
            status='APPROVED',
            end_date__gte=timezone.now()
        ).exists()
        
        if not active_sub:
            # We explicitly define the error dictionary for DRF to render
            # But BasePermission just returns False. 
            # View will handle the 403.
            # To give custom JSON body { "error": ... } we might need a custom exception handler 
            # or rely on DRF's default 403 details.
            # "Backend MUST return: HTTP 403 Forbidden ... Clear API error responses: { error: SUBSCRIPTION_REQUIRED ... }"
            return False
            
        return True
