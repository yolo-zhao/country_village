# backend/apps/activities/serializers.py
from rest_framework import serializers
from .models import ActivityCategory, Tag, Activity, ActivityImage, Reservation, ActivityReview, ActivityPhoto, ActivityCheckIn, ActivityLike, ActivityComment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',] # 可以根据需要添加更多字段
        ref_name = 'ActivityUserSerializer'  # 添加唯一的ref_name

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = ['id', 'image', 'caption']
        read_only_fields = ['id']

class ActivitySerializer(serializers.ModelSerializer):
    category = ActivityCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=ActivityCategory.objects.all(),
        write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    farmer = UserSerializer(read_only=True)
    images = ActivityImageSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'title', 'slug', 'description', 'start_time', 'end_time', 'location', 
                 'category', 'category_id', 'tags', 'cover_image', 'max_participants', 
                 'status', 'farmer', 'created_at', 'updated_at', 'images']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'farmer', 'images']
    
    def validate(self, data):
        """
        额外的验证以确保category被设置
        """
        if 'category' not in data:
            raise serializers.ValidationError({"category": "活动分类不能为空"})
        return data
    
    def create(self, validated_data):
        """
        自定义创建方法，确保category被正确设置
        """
        tags_data = validated_data.pop('tags', [])
        instance = Activity.objects.create(**validated_data)
        
        # 添加标签
        if tags_data:
            instance.tags.set(tags_data)
            
        return instance

class ReservationSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'activity', 'user', 'reservation_date', 'contact_name', 'contact_phone', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'activity', 'user']

class ActivityReviewSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ActivityReview
        fields = ['id', 'activity', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'activity', 'user', 'auto_reply']

class ActivityPhotoSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ActivityPhoto
        fields = ['id', 'activity', 'user', 'image', 'caption', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'activity', 'user']

class ActivityCheckInSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ActivityCheckIn
        fields = ['id', 'activity', 'user', 'check_in_time']
        read_only_fields = ['id', 'check_in_time', 'activity', 'user']

class ActivityLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # content_object 可以通过 SerializerMethodField 实现，这里先省略简化
    class Meta:
        model = ActivityLike
        fields = ['id', 'user', 'content_type', 'object_id', 'liked_at']
        read_only_fields = ['id', 'liked_at', 'user']

class ActivityCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # content_object 可以通过 SerializerMethodField 实现，这里先省略简化
    class Meta:
        model = ActivityComment
        fields = ['id', 'user', 'content_type', 'object_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'auto_reply', 'content_type', 'object_id']