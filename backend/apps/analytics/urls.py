from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dashboard', views.AnalyticsDashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    
    # 用户分析相关接口
    path('user-behavior/', views.UserBehaviorAnalyticsView.as_view(), name='user-behavior'),
    path('user-growth/', views.UserGrowthAnalyticsView.as_view(), name='user-growth'),
    path('user-retention/', views.UserRetentionAnalyticsView.as_view(), name='user-retention'),
    
    # 活动分析相关接口
    path('popular-activities/', views.PopularActivitiesAnalyticsView.as_view(), name='popular-activities'),
    path('activity-engagement/', views.ActivityEngagementAnalyticsView.as_view(), name='activity-engagement'),
    path('activity-conversion/', views.ActivityConversionAnalyticsView.as_view(), name='activity-conversion'),
    
    # 产品分析相关接口
    path('popular-products/', views.PopularProductsAnalyticsView.as_view(), name='popular-products'),
    path('product-views/', views.ProductViewsAnalyticsView.as_view(), name='product-views'),
    path('cart-abandonment/', views.CartAbandonmentAnalyticsView.as_view(), name='cart-abandonment'),
    
    # 销售分析相关接口
    path('sales/', views.SalesAnalyticsView.as_view(), name='sales'),
    path('revenue/', views.RevenueAnalyticsView.as_view(), name='revenue'),
    path('orders/', views.OrdersAnalyticsView.as_view(), name='orders'),
    
    # 区域分析相关接口
    path('regional-activity/', views.RegionalActivityAnalyticsView.as_view(), name='regional-activity'),
    path('regional-sales/', views.RegionalSalesAnalyticsView.as_view(), name='regional-sales'),
    
    # 导出报表接口
    path('export-report/', views.ExportReportView.as_view(), name='export-report'),
] 