from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'announcements', views.SystemAnnouncementViewSet)
# 修复：FeedbackViewSet不存在，改用API视图
# router.register(r'feedback', views.FeedbackViewSet)
# 修复：HelpArticleViewSet不存在，改用API视图
# router.register(r'help', views.HelpArticleViewSet)

# app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    
    # 新增接口
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),  # 文件上传接口
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),  # 反馈接口
    path('help/', views.HelpCenterView.as_view(), name='help'),  # 帮助中心接口
    path('weather/', views.WeatherInfoView.as_view(), name='weather'),  # 天气信息接口
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),  # 控制面板数据接口
    path('search/', views.GlobalSearchView.as_view(), name='global-search'),  # 全局搜索接口
    # AI助手接口
    path('ai-assistant/', views.AIAssistantView.as_view(), name='ai-assistant'),
    path('ai-assistant/status/', views.AIAssistantView.as_view(), name='ai-assistant-status'),
]