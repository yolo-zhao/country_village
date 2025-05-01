# users/views.py
from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import User
from .models import TouristProfile, FarmerProfile
from .serializers import UserSerializer, TouristProfileSerializer, FarmerProfileSerializer, UserCreationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken # 导入 ObtainAuthToken 基类
from rest_framework.authtoken.models import Token # 导入 Token 模型



class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        role = request.data.get('role', None)
        if role == 'tourist':
            TouristProfile.objects.create(user=user)
        elif role == 'farmer':
            FarmerProfile.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': '注册成功',
                         'user_id': user.id,
                         'username': user.username,
                         'role': role
                         }, status=status.HTTP_201_CREATED, headers=headers)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        role = None
        if user.is_superuser or user.is_staff:
            role = 'admin'
        if role is None:
            try:
                if hasattr(user, 'touristprofile') and user.touristprofile is not None:
                    role = 'tourist'
                elif hasattr(user, 'farmerprofile') and user.farmerprofile is not None:
                    role = 'farmer'
            except (TouristProfile.DoesNotExist, FarmerProfile.DoesNotExist):
                pass

        return Response({
            'success': True,
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': role,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户信息的 API 视图集 (只读)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TouristProfileViewSet(viewsets.ModelViewSet):
    """
    游客信息的 API 视图集
    """
    queryset = TouristProfile.objects.all()
    serializer_class = TouristProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # 需要登录才能操作


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TouristProfile.objects.filter(user=self.request.user)
        return TouristProfile.objects.none()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmerProfileViewSet(viewsets.ModelViewSet):
    """
    农户信息的 API 视图集
    """
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # 需要登录才能操作


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FarmerProfile.objects.filter(user=self.request.user)
        return FarmerProfile.objects.none()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

