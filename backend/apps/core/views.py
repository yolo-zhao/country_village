# backend/apps/core/views.py
from rest_framework import viewsets, permissions
from .models import SystemAnnouncement
from .serializers import SystemAnnouncementSerializer

class SystemAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = SystemAnnouncement.objects.all().order_by('-created_at')
    serializer_class = SystemAnnouncementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]