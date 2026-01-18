from rest_framework import views, permissions, status, viewsets
from rest_framework.response import Response
from .models import AdminSettings
from .serializers import AdminSettingsSerializer
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()

class AdminSettingsView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        settings = AdminSettings.load()
        serializer = AdminSettingsSerializer(settings)
        return Response(serializer.data)

    def patch(self, request):
        settings = AdminSettings.load()
        serializer = AdminSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = User.objects.all()
        
        # Search by email or full_name
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(email__icontains=search) | queryset.filter(full_name__icontains=search)
        
        # Filter by role
        role = self.request.query_params.get('role', '')
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by is_active
        is_active = self.request.query_params.get('is_active', '')
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.order_by('-date_joined')

    def partial_update(self, request, *args, **kwargs):
        """Allow partial updates of user role and is_active status"""
        user = self.get_object()
        
        if 'role' in request.data:
            user.role = request.data['role']
        if 'is_active' in request.data:
            user.is_active = request.data['is_active']
        
        user.save()
        return Response(UserSerializer(user).data)
