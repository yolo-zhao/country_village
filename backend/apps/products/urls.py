from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('farmer/products/', views.farmer_product_list, name='farmer_product_list'),
    path('farmer/products/create/', views.create_product, name='create_product'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    # 购物车相关的 URL
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # 结账相关的 URL
    path('checkout/', views.checkout, name='checkout'),
]