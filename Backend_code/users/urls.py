# from rest_framework import generics
# from .serializers import RegisterSerializer
# from rest_framework.permissions import AllowAny

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]


from django.urls import path
from .views import RegisterView, AddLibrarianView, UserMeView, UserCountView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add refresh endpoint
    path('add-librarian/', AddLibrarianView.as_view(), name='add-librarian'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('count/', UserCountView.as_view(), name='user-count'),
]
