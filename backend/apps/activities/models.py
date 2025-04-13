from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class ActivityCategory(models.Model):
    """
    活动分类
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("活动分类")
        verbose_name_plural = _("活动分类列表")

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    活动标签 (可选)
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _("标签")
        verbose_name_plural = _("标签列表")

    def __str__(self):
        return self.name

class Activity(models.Model):
    """
    乡村体验活动
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True) # 用于生成友好的 URL
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE, related_name='activities')
    tags = models.ManyToManyField(Tag, blank=True)
    cover_image = models.ImageField(upload_to='activities/covers/')
    max_participants = models.PositiveIntegerField(default=0)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("活动")
        verbose_name_plural = _("活动列表")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ActivityImage(models.Model):
    """
    活动实景照片
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='activities/images/')
    caption = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("活动图片")
        verbose_name_plural = _("活动图片列表")

    def __str__(self):
        return self.caption or self.image.name

class Reservation(models.Model):
    """
    活动预约
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_reservations')
    reservation_date = models.DateField()
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待审核'),
            ('confirmed', '已确认'),
            ('cancelled', '已取消'),
            ('completed', '已完成'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("预约")
        verbose_name_plural = _("预约列表")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} 预约了 {self.activity.title} ({self.reservation_date})"

class ActivityReview(models.Model):
    """
    活动评价
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_reviews')
    rating = models.IntegerField(
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("活动评价")
        verbose_name_plural = _("活动评价列表")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} 对 {self.activity.title} 的评价"

class ActivityPhoto(models.Model):
    """
    游客上传的活动照片
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='user_photos')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_activity_photos')
    image = models.ImageField(upload_to='activities/user_photos/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("活动照片")
        verbose_name_plural = _("活动照片列表")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} 上传的 {self.activity.title} 照片"

class ActivityCheckIn(models.Model):
    """
    活动打卡记录
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='check_ins')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_check_ins')
    check_in_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("活动打卡")
        verbose_name_plural = _("活动打卡记录")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} 在 {self.activity.title} 打卡"

class ActivityLike(models.Model):
    """
    活动相关内容的点赞
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("活动点赞")
        verbose_name_plural = _("活动点赞列表")
        unique_together = ('user', 'content_type', 'object_id')

class ActivityComment(models.Model):
    """
    活动相关内容的评论
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("活动评论")
        verbose_name_plural = _("活动评论列表")