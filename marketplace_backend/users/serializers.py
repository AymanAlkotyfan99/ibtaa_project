from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MerchantProfile, CustomerProfile

User = get_user_model()

class MerchantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        fields = ['business_name', 'is_subscribed']
        read_only_fields = ['is_subscribed']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)
    business_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'business_name']

    def validate(self, attrs):
        if attrs['role'] == 'MERCHANT' and not attrs.get('business_name'):
             raise serializers.ValidationError({"business_name": "Required for merchants."})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        role = validated_data['role']
        business_name = validated_data.pop('business_name', '')
        
        # Use create_user manager method
        user = User.objects.create_user(email=email, password=password, role=role)

        if role == 'MERCHANT':
            MerchantProfile.objects.create(user=user, business_name=business_name)
        elif role == 'CUSTOMER':
            CustomerProfile.objects.create(user=user)
        
        return user
