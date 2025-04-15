# backend/apps/activities/views.py
from rest_framework import viewsets, permissions
from .models import ActivityCategory, Tag, Activity, ActivityImage, Reservation, ActivityReview, ActivityPhoto, ActivityCheckIn, ActivityLike, ActivityComment
from .serializers import ActivityCategorySerializer, TagSerializer, ActivitySerializer, ActivityImageSerializer, ReservationSerializer, ActivityReviewSerializer, ActivityPhotoSerializer, ActivityCheckInSerializer, ActivityLikeSerializer, ActivityCommentSerializer

class ActivityCategoryViewSet(viewsets.ModelViewSet):
    queryset = ActivityCategory.objects.all()
    serializer_class = ActivityCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

class ActivityImageViewSet(viewsets.ModelViewSet):
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能管理自己的预约

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityReviewViewSet(viewsets.ModelViewSet):
    queryset = ActivityReview.objects.all()
    serializer_class = ActivityReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityPhotoViewSet(viewsets.ModelViewSet):
    queryset = ActivityPhoto.objects.all()
    serializer_class = ActivityPhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityCheckInViewSet(viewsets.ModelViewSet):
    queryset = ActivityCheckIn.objects.all()
    serializer_class = ActivityCheckInSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能创建打卡记录

    def get_queryset(self):
        return ActivityCheckIn.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityLikeViewSet(viewsets.ModelViewSet):
    queryset = ActivityLike.objects.all()
    serializer_class = ActivityLikeSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能点赞

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityCommentViewSet(viewsets.ModelViewSet):
    queryset = ActivityComment.objects.all()
    serializer_class = ActivityCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)