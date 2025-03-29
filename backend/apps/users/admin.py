from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import TouristProfile, FarmerProfile

# 定义 TouristProfile 的内联管理
class TouristProfileInline(admin.StackedInline):
    model = TouristProfile
    can_delete = False
    verbose_name_plural = '游客信息'

# 定义 FarmerProfile 的内联管理
class FarmerProfileInline(admin.StackedInline):
    model = FarmerProfile
    can_delete = False
    verbose_name_plural = '农户信息'

# 继承 Django 的 UserAdmin 并添加内联
class UserAdmin(BaseUserAdmin):
    inlines = (TouristProfileInline, FarmerProfileInline)

# 重新注册 User 模型
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 如果您希望单独管理 Profile，也可以注册它们
# admin.site.register(TouristProfile)
# admin.site.register(FarmerProfile)