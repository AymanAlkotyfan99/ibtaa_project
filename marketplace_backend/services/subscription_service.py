from django.utils import timezone
from datetime import timedelta

class SubscriptionService:
    @staticmethod
    def approve_subscription(subscription):
        subscription.status = 'APPROVED'
        subscription.start_date = timezone.now()
        
        days = 30 if subscription.plan == 'MONTHLY' else 365
        subscription.end_date = subscription.start_date + timedelta(days=days)
        subscription.save()
        
        # Update Merchant Profile
        if hasattr(subscription.merchant, 'merchant_profile'):
            profile = subscription.merchant.merchant_profile
            profile.is_subscribed = True
            profile.save()
        
        return subscription

    @staticmethod
    def reject_subscription(subscription, reason):
        subscription.status = 'REJECTED'
        subscription.rejection_reason = reason
        subscription.save()
        return subscription
