# backend/apps/core/serializers.py
from rest_framework import serializers
from .models import SystemAnnouncement

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAnnouncement
        fields = ['id', 'title', 'content', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']