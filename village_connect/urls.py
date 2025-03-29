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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('core.urls')), # 包含 core 应用的 URL
    # path('users/', include('users.urls')),
    # path('activities/', include('activities.urls')),
    # path('products/', include('products.urls')),
    path('activities/', include('backend.apps.activities.urls')),
    path('core/', include('backend.apps.core.urls')),
    path('products/', include('backend.apps.products.urls')),
    path('users/', include('backend.apps.users.urls')),
]
