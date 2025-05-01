# backend/apps/activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# 主路由
router = DefaultRouter()
router.register(r'activity-categories', views.ActivityCategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'activity-images', views.ActivityImageViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'activity-reviews', views.ActivityReviewViewSet)
router.register(r'activity-photos', views.ActivityPhotoViewSet)
router.register(r'activity-check-ins', views.ActivityCheckInViewSet)
router.register(r'activity-likes', views.ActivityLikeViewSet)
router.register(r'activity-comments', views.ActivityCommentViewSet)

# 创建嵌套路由，将预约作为活动的子资源
activities_router = routers.NestedSimpleRouter(router, r'activities', lookup='activity')
activities_router.register(r'reservations', views.ActivityReservationViewSet, basename='activity-reservations')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(activities_router.urls)),  # 添加嵌套路由
    
    # 新增接口
    path('my-activities/', views.UserActivitiesView.as_view(), name='user-activities'),  # 我的活动
    path('search/', views.ActivitySearchView.as_view(), name='activity-search'),  # 活动搜索
    path('recommendations/', views.ActivityRecommendationsView.as_view(), name='activity-recommendations'),  # 活动推荐
    path('statistics/', views.ActivityStatisticsView.as_view(), name='activity-statistics'),  # 活动统计
    path('nearby/', views.NearbyActivitiesView.as_view(), name='nearby-activities'),  # 附近活动
    path('popular/', views.PopularActivitiesView.as_view(), name='popular-activities'),  # 热门活动
    path('calendar/', views.ActivityCalendarView.as_view(), name='activity-calendar'),  # 活动日历
]