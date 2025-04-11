from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('farmer/products/', views.farmer_product_list, name='farmer_product_list'),
    path('farmer/products/create/', views.create_product, name='create_product'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]