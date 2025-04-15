# backend/apps/activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

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

urlpatterns = [
    path('', include(router.urls)),
]