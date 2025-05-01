from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class SystemAnnouncement(models.Model):
    """
    系统公告
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("系统公告")
        verbose_name_plural = _("系统公告列表")

    def __str__(self):
        return self.title

class Feedback(models.Model):
    """
    用户反馈
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待处理'),
            ('processing', '处理中'),
            ('resolved', '已解决'),
            ('closed', '已关闭'),
        ],
        default='pending'
    )
    admin_reply = models.TextField(blank=True, null=True)
    reply_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("用户反馈")
        verbose_name_plural = _("用户反馈列表")

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class HelpArticle(models.Model):
    """
    帮助中心文章
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('account', '账户相关'),
            ('activities', '活动相关'),
            ('products', '农产品相关'),
            ('payment', '支付相关'),
            ('other', '其他问题'),
        ]
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("帮助文章")
        verbose_name_plural = _("帮助文章列表")

    def __str__(self):
        return self.title

