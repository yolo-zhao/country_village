from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/tourist/', views.tourist_profile, name='tourist_profile'),
    path('profile/farmer/', views.farmer_profile, name='farmer_profile'),
]