from rest_framework import views, permissions, status
from rest_framework.response import Response
from .models import AdminSettings
from .serializers import AdminSettingsSerializer

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
