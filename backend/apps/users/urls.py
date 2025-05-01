from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegistrationView, CustomAuthToken, PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tourist-profiles', views.TouristProfileViewSet)#游客
router.register(r'farmer-profiles', views.FarmerProfileViewSet)#农户




urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),#用户注册
    path('login/', CustomAuthToken.as_view(), name='login'),#用户登录
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # 新增接口
    path('me/', views.CurrentUserView.as_view(), name='current-user'),  # 当前用户信息
    path('update-info/', views.UpdateUserInfoView.as_view(), name='update-user-info'),  # 更新用户信息
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),  # 修改密码
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),  # 密码重置请求
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),  # 密码重置确认
    path('logout/', views.LogoutView.as_view(), name='logout'),  # 用户登出
]