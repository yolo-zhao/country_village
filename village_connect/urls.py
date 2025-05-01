"""
URL configuration for village_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# 项目主 urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# 导入 drf-yasg 相关模块
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 设置 API 文档信息
schema_view = get_schema_view(
   openapi.Info(
      title="乡村旅游平台 API",
      default_version='v1',
      description="乡村旅游平台 API 文档",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API 文档 URL - 使用 drf-yasg
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API 应用路由
    path('api/', include('backend.apps.users.urls')),
    path('api/', include('backend.apps.products.urls')),
    path('api/', include('backend.apps.core.urls')),
    path('api/', include('backend.apps.activities.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)