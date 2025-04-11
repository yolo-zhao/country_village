from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.activity_list, name='activity_list'),
    path('farmer/activities/', views.farmer_activity_list, name='farmer_activity_list'),
    path('farmer/activities/create/', views.create_activity, name='create_activity'),
    path('<int:activity_id>/', views.activity_detail, name='activity_detail'),
]