# users/views.py
from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import User
from .models import TouristProfile, FarmerProfile
from .serializers import UserSerializer, TouristProfileSerializer, FarmerProfileSerializer, UserCreationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken # 导入 ObtainAuthToken 基类
from rest_framework.authtoken.models import Token # 导入 Token 模型
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings



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


# 新增视图类

class CurrentUserView(APIView):
    """
    获取当前登录用户信息的视图
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        # 获取用户角色
        if user.is_superuser or user.is_staff:
            data['role'] = 'admin'
        elif hasattr(user, 'touristprofile'):
            data['role'] = 'tourist'
            data['profile'] = TouristProfileSerializer(user.touristprofile).data
        elif hasattr(user, 'farmerprofile'):
            data['role'] = 'farmer'
            data['profile'] = FarmerProfileSerializer(user.farmerprofile).data
        else:
            data['role'] = 'unknown'
            
        return Response(data)


class UpdateUserInfoView(APIView):
    """
    更新当前用户信息的视图
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        
        # 更新基本信息
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        
        user.save()
        
        # 更新资料信息
        if 'profile' in request.data:
            profile_data = request.data['profile']
            
            if hasattr(user, 'touristprofile'):
                profile = user.touristprofile
                if 'nickname' in profile_data:
                    profile.nickname = profile_data['nickname']
                if 'contact_phone' in profile_data:
                    profile.contact_phone = profile_data['contact_phone']
                profile.save()
                profile_serializer = TouristProfileSerializer(profile)
            
            elif hasattr(user, 'farmerprofile'):
                profile = user.farmerprofile
                if 'farm_name' in profile_data:
                    profile.farm_name = profile_data['farm_name']
                if 'contact_phone' in profile_data:
                    profile.contact_phone = profile_data['contact_phone']
                profile.save()
                profile_serializer = FarmerProfileSerializer(profile)
        
        # 返回更新后的用户信息
        return Response({
            'message': '用户信息更新成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile': profile_serializer.data if 'profile' in locals() else None
            }
        })


class ChangePasswordView(APIView):
    """
    修改密码的视图
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({'error': '请提供旧密码和新密码'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证旧密码
        if not user.check_password(old_password):
            return Response({'error': '旧密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 设置新密码
        user.set_password(new_password)
        user.save()
        
        # 更新Token
        try:
            token = Token.objects.get(user=user)
            token.delete()
            Token.objects.create(user=user)
        except Token.DoesNotExist:
            Token.objects.create(user=user)
        
        return Response({'message': '密码修改成功'})


class PasswordResetView(APIView):
    """
    请求密码重置的视图
    """
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': '请提供邮箱地址'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            # 生成重置令牌
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # 构建重置链接
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}&uid={uid}"
            
            # 发送邮件
            subject = '密码重置请求'
            message = f"""
            您收到此邮件是因为您请求重置密码。请点击以下链接重置密码：
            
            {reset_link}
            
            如果您没有请求重置密码，请忽略此邮件。
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': '密码重置链接已发送到您的邮箱'})
            except Exception as e:
                return Response({'error': f'发送邮件失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except User.DoesNotExist:
            # 为安全起见，即使用户不存在也返回相同的消息
            return Response({'message': '密码重置链接已发送到您的邮箱（如果该邮箱存在）'})


class PasswordResetConfirmView(APIView):
    """
    确认密码重置的视图
    """
    def post(self, request):
        token = request.data.get('token')
        uid = request.data.get('uid')
        new_password = request.data.get('new_password')
        
        if not token or not uid or not new_password:
            return Response({'error': '请提供所有必要的信息'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 解码用户ID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            # 验证令牌
            if not default_token_generator.check_token(user, token):
                return Response({'error': '无效或已过期的令牌'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 重置密码
            user.set_password(new_password)
            user.save()
            
            # 更新Token
            try:
                old_token = Token.objects.get(user=user)
                old_token.delete()
            except Token.DoesNotExist:
                pass
            Token.objects.create(user=user)
            
            return Response({'message': '密码重置成功'})
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': '无效的用户ID'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    用户登出的视图
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 删除用户的Token
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': '登出成功'})
        except Token.DoesNotExist:
            return Response({'error': '用户未登录'}, status=status.HTTP_400_BAD_REQUEST)

