from rest_framework import serializers
from .models import MerchantSubscription
from core.models import AdminSettings

class SubscriptionPlanSerializer(serializers.Serializer):
    subscription_plans = serializers.ListField()

class MerchantSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(read_only=True)
    merchant_email = serializers.SerializerMethodField()
    business_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MerchantSubscription
        fields = ['id', 'plan', 'plan_name', 'payment_proof_image', 'notes', 'status', 'start_date', 'end_date', 'rejection_reason', 'created_at', 'submitted_at', 'merchant_email', 'business_name']
        read_only_fields = ['status', 'start_date', 'end_date', 'rejection_reason', 'created_at', 'submitted_at', 'plan_name', 'merchant_email', 'business_name']

    def get_merchant_email(self, obj):
        return obj.merchant.email
    
    def get_business_name(self, obj):
        if hasattr(obj.merchant, 'merchant_profile'):
            return obj.merchant.merchant_profile.business_name
        return None

    def create(self, validated_data):
        validated_data['merchant'] = self.context['request'].user
        
        # Get plan name from AdminSettings
        plan_id = validated_data.get('plan')
        try:
            settings = AdminSettings.load()
            if 0 <= plan_id < len(settings.subscription_plans):
                plan = settings.subscription_plans[plan_id]
                validated_data['plan_name'] = plan.get('name', f'Plan {plan_id}')
        except:
            pass
        
        return super().create(validated_data)
