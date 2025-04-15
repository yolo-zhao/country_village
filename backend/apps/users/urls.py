from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegistrationView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tourist-profiles', views.TouristProfileViewSet)#游客
router.register(r'farmer-profiles', views.FarmerProfileViewSet)#农户




urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),#用户注册
]