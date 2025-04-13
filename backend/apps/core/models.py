from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

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

class HomePageOrder(models.Model):
    """
    首页内容排序 (可以根据需要设计更复杂的排序逻辑)
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("首页排序")
        verbose_name_plural = _("首页排序")  # 复数形式通常与单数相同，如果意义不同可以修改
        ordering = ['order']