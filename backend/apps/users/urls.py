from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegistrationView, CustomAuthToken

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tourist-profiles', views.TouristProfileViewSet)#游客
router.register(r'farmer-profiles', views.FarmerProfileViewSet)#农户




urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),#用户注册
    path('login/', CustomAuthToken.as_view(), name='login'),#用户登录
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]