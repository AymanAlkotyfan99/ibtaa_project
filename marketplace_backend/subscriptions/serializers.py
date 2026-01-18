from rest_framework import serializers
from .models import MerchantSubscription
from core.models import AdminSettings

class SubscriptionPlanSerializer(serializers.Serializer):
    monthly_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    yearly_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    sham_cash_account = serializers.CharField()
    sham_cash_number = serializers.CharField()

class MerchantSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantSubscription
        fields = ['id', 'plan', 'payment_proof_image', 'status', 'start_date', 'end_date', 'rejection_reason', 'created_at']
        read_only_fields = ['status', 'start_date', 'end_date', 'rejection_reason', 'created_at']

    def create(self, validated_data):
        validated_data['merchant'] = self.context['request'].user
        return super().create(validated_data)
