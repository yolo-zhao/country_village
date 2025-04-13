# users/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class TouristProfile(models.Model):
    """
    游客用户扩展信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    # 可以添加其他游客相关的字段

    class Meta:
        verbose_name = _("游客信息")
        verbose_name_plural = _("游客信息列表")

    def __str__(self):
        return f"{self.nickname or self.user.username} (游客)"

class FarmerProfile(models.Model):
    """
    农户用户扩展信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    farm_name = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    # 可以添加其他农户相关的字段

    class Meta:
        verbose_name = _("农户信息")
        verbose_name_plural = _("农户信息列表")

    def __str__(self):
        return f"{self.farm_name or self.user.username} (农户)"