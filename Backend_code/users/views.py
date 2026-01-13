from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView

# Member Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Add Librarian (Admin Only)
class AddLibrarianView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        data = request.data.copy()
        data['role'] = 'ADMIN'
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Librarian added successfully", "user": serializer.data})

# Get Current User
class UserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Ensure superusers/staff are represented as ADMIN for frontend checks
        role = user.role
        if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False):
            role = 'ADMIN'

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'phone': user.phone,
            'address': user.address,
            'is_staff': getattr(user, 'is_staff', False),
            'is_superuser': getattr(user, 'is_superuser', False),
        })

# Get Total User Count (Admin Only)
class UserCountView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        count = User.objects.count()
        return Response({'count': count})
