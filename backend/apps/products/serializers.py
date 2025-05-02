# backend/apps/products/serializers.py
from rest_framework import serializers
from .models import Product, ProductImage, ProductInquiry, Cart, CartItem
from django.contrib.auth.models import User

#user模型
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email']
        ref_name = 'ProductUserSerializer'  # 添加唯一的ref_name
#产品图片
class ProductImageSerializer(serializers.ModelSerializer):
    image_display_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'image_display_url', 'caption']
        
    def get_image_display_url(self, obj):
        """返回用于显示的图片URL"""
        return obj.get_image_url() or (obj.image.url if obj.image else "")
#产品
class ProductSerializer(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True) # 显示农场主信息
    images = ProductImageSerializer(many=True, read_only=True) # 显示产品图片列表

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'farmer', 'created_at', 'updated_at', 'status', 'images']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'farmer', 'images']

class ProductInquirySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # 显示咨询用户
    product = ProductSerializer(read_only=True) # 显示咨询产品

    class Meta:
        model = ProductInquiry
        fields = ['id', 'product', 'user', 'name', 'contact', 'message', 'created_at', 'response', 'responded_at']
        read_only_fields = ['id', 'created_at', 'product', 'user', 'responded_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField() # 添加 total_price 字段

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'items']