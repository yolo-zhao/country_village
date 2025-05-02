from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'messages', views.UserMessageViewSet, basename='messages')
router.register(r'system', views.SystemNotificationViewSet, basename='system')
router.register(r'activity-reminders', views.ActivityReminderViewSet, basename='activity-reminders')

urlpatterns = [
    path('', include(router.urls)),
    
    # 通知管理接口
    path('settings/', views.NotificationSettingsView.as_view(), name='notification-settings'),  # 通知设置
    path('mark-read/', views.MarkNotificationsReadView.as_view(), name='mark-notifications-read'),  # 标记通知为已读
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),  # 标记所有通知为已读
    path('delete/', views.DeleteNotificationView.as_view(), name='delete-notification'),  # 删除通知
    path('count/', views.UnreadNotificationCountView.as_view(), name='unread-notification-count'),  # 未读通知数量
    path('latest/', views.LatestNotificationsView.as_view(), name='latest-notifications'),  # 最新通知
    
    # 特定类型通知接口
    path('activities/', views.ActivityNotificationsView.as_view(), name='activity-notifications'),  # 活动相关通知
    path('orders/', views.OrderNotificationsView.as_view(), name='order-notifications'),  # 订单相关通知
    path('comments/', views.CommentNotificationsView.as_view(), name='comment-notifications'),  # 评论通知
] 