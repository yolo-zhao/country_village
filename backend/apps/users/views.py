
# users/views.py
from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import User
from .models import TouristProfile, FarmerProfile
from .serializers import UserSerializer, TouristProfileSerializer, FarmerProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer



class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # 使用 UserSerializer 来创建用户

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # 根据 role 创建对应的 Profile
        role = request.data.get('role', None)
        if role == 'tourist':
            TouristProfile.objects.create(user=user)
        elif role == 'farmer':
            FarmerProfile.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED, headers=headers)

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
        """
        确保用户只能看到和修改自己的 TouristProfile。
        """
        return TouristProfile.objects.filter(user=self.request.user)

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
        """
        确保用户只能看到和修改自己的 FarmerProfile。
        """
        return FarmerProfile.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

