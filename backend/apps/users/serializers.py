# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TouristProfile, FarmerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',] # 根据需要添加更多字段


class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user
class TouristProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # 嵌套 User 信息，只读

    class Meta:
        model = TouristProfile
        fields = ['user', 'nickname', 'contact_phone']

class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # 嵌套 User 信息，只读


    class Meta:
        model = FarmerProfile
        fields = ['user', 'farm_name', 'contact_phone']