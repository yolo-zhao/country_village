from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('announcement/create/', views.create_announcement, name='create_announcement'),
    # 您可能还需要编辑和删除公告的 URL
]