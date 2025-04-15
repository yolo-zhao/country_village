from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'announcements', views.SystemAnnouncementViewSet)

# app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
]