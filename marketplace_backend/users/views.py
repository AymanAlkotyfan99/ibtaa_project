from rest_framework import generics, permissions, views
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
        if user.role == 'MERCHANT':
            # Handle case where profile might be missing (data integrity)
            profile = getattr(user, 'merchant_profile', None)
            if profile:
                data['is_subscribed'] = profile.is_subscribed
                data['business_name'] = profile.business_name
        return Response(data)
