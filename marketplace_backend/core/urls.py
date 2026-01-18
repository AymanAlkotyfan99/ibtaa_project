from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminSettingsView, AdminUsersViewSet

router = DefaultRouter()
router.register(r'users', AdminUsersViewSet, basename='admin-users')

urlpatterns = [
    path('settings/', AdminSettingsView.as_view(), name='admin-settings'),
    path('', include(router.urls)),
]
