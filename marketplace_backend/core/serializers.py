from rest_framework import serializers
from .models import AdminSettings
import json

class AdminSettingsSerializer(serializers.ModelSerializer):
    subscription_plans = serializers.SerializerMethodField()
    
    class Meta:
        model = AdminSettings
        fields = '__all__'
    
    def get_subscription_plans(self, obj):
        """Parse subscription_plans JSON string to list"""
        try:
            if isinstance(obj.subscription_plans, str):
                return json.loads(obj.subscription_plans)
            return obj.subscription_plans or []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def to_internal_value(self, data):
        """Convert subscription_plans array to JSON string for storage"""
        internal_data = super().to_internal_value(data)
        if 'subscription_plans' in internal_data:
            plans = internal_data['subscription_plans']
            if isinstance(plans, list):
                internal_data['subscription_plans'] = json.dumps(plans)
        return internal_data

