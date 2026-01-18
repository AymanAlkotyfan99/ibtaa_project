from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MerchantSubscriptionViewSet, SubscriptionPlansView

router = DefaultRouter()
router.register(r'subscriptions', MerchantSubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('merchant/', include(router.urls)), # /api/merchant/subscriptions/
    path('admin/', include(router.urls)), # /api/admin/subscriptions/ (Same viewset, perm logic inside)
    path('plans/', SubscriptionPlansView.as_view(), name='plans'),
]
