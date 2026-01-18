from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from subscriptions.models import MerchantSubscription
from django.utils import timezone
from datetime import timedelta
from users.models import MerchantProfile

User = get_user_model()

class MerchantRestrictionTest(APITestCase):
    def setUp(self):
        # Create Merchant
        self.merchant = User.objects.create_user(email="merchant@test.com", password="password", role='MERCHANT')
        MerchantProfile.objects.create(user=self.merchant, business_name="Test Store")
        
        # Create Customer
        self.customer = User.objects.create_user(email="customer@test.com", password="password", role='CUSTOMER')


    def test_merchant_cannot_create_product_without_subscription(self):
        self.client.force_authenticate(user=self.merchant)
        url = '/api/merchant/products/'
        data = {'name': 'Test Product', 'price': 100.00, 'description': 'desc'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_merchant_can_create_product_with_subscription(self):
        self.client.force_authenticate(user=self.merchant)
        # Manually create Approved Subscription
        sub = MerchantSubscription.objects.create(
             merchant=self.merchant,
             plan='MONTHLY',
             status='APPROVED',
             start_date=timezone.now(),
             end_date=timezone.now() + timedelta(days=30)
        )
        # Note: logic checks active subscription OR profile flag? 
        # My implementation core/permissions.py checks DB directly for Active Subscription logic!
        # So I don't strictly need to update profile.is_subscribed for permission to pass, 
        # but viewsets might check it for listing restrictions.
        # Let's set it anyway as app logic should update it.
        self.merchant.merchant_profile.is_subscribed = True
        self.merchant.merchant_profile.save()
        
        url = '/api/merchant/products/'
        data = {'name': 'Test Product', 'price': 100.00, 'description': 'desc'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
