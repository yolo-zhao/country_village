# backend/apps/core/serializers.py
from rest_framework import serializers
from .models import SystemAnnouncement, Feedback, HelpArticle
from django.contrib.auth.models import User

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAnnouncement
        fields = ['id', 'title', 'content', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class FeedbackSerializer(serializers.ModelSerializer):
    user_info = UserBriefSerializer(source='user', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_info', 'title', 'content', 'created_at', 'status', 'admin_reply', 'reply_at']
        read_only_fields = ['id', 'created_at', 'reply_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }

class HelpArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpArticle
        fields = ['id', 'title', 'content', 'category', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']