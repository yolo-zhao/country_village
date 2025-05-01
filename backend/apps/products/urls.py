# backend/apps/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'product-images', views.ProductImageViewSet)
router.register(r'product-inquiries', views.ProductInquiryViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cart-items', views.CartItemViewSet)
# 暂时注释掉，因为 OrderViewSet 尚未实现
# router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    
    # 购物车快捷路由 - 前端通过 /cart/ 也能访问购物车
    path('cart/', views.CartSingleView.as_view(), name='cart-single'),
    path('cart/add_item/', views.CartAddItemView.as_view(), name='cart-add-item'),
    path('cart/items/<int:item_id>/', views.CartItemOperationView.as_view(), name='cart-item-operation'),
    path('cart/items/', views.CartItemsView.as_view(), name='cart-items'),
    
    # 新增接口
    path('search/', views.ProductSearchView.as_view(), name='product-search'),
    path('recommendations/', views.ProductRecommendationsView.as_view(), name='product-recommendations'),
    path('favorites/', views.ProductFavoritesView.as_view(), name='product-favorites'),
    # 暂时注释掉，因为 OrderViewSet 尚未实现
    # path('my-orders/', views.UserOrdersView.as_view(), name='user-orders'),
    # path('payment/create/', views.PaymentCreateView.as_view(), name='payment-create'),
    # path('payment/callback/', views.PaymentCallbackView.as_view(), name='payment-callback'),
    path('categories/', views.ProductCategoryView.as_view(), name='product-categories'),
    path('popular/', views.PopularProductsView.as_view(), name='popular-products'),
]