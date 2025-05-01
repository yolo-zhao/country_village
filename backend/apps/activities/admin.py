from django.contrib import admin
from django.utils.html import format_html
from .models import ActivityCategory, Tag, Activity, ActivityImage, Reservation, ActivityReview, ActivityPhoto, ActivityCheckIn, ActivityLike, ActivityComment

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    def get_list_display(self, request):
        return ['分类名称']
        
    def 分类名称(self, obj):
        return obj.name

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    def get_list_display(self, request):
        return ['标签名称']
        
    def 标签名称(self, obj):
        return obj.name

class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1
    verbose_name = '活动图片'
    verbose_name_plural = '活动图片'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('标题', '分类', '标签列表', '开始时间', '结束时间', '地点', '最大参与人数', '农户')
    list_filter = ('category', 'tags', 'start_time', 'created_at')
    search_fields = ('title', 'description', 'location', 'farmer__username')
    inlines = [ActivityImageInline]
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_time'
    list_per_page = 20
    
    def 标题(self, obj):
        return obj.title
    
    def 分类(self, obj):
        return obj.category.name
    
    def 标签列表(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    def 开始时间(self, obj):
        return obj.start_time
    
    def 结束时间(self, obj):
        return obj.end_time
    
    def 地点(self, obj):
        return obj.location
    
    def 最大参与人数(self, obj):
        return obj.max_participants
    
    def 农户(self, obj):
        return obj.farmer.username

@admin.register(ActivityImage)
class ActivityImageAdmin(admin.ModelAdmin):
    list_display = ('所属活动', '图片预览', '图片说明')
    search_fields = ('activity__title', 'caption')
    list_filter = ('activity',)
    
    def 所属活动(self, obj):
        return obj.activity.title
    
    def 图片预览(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return ""
    
    def 图片说明(self, obj):
        return obj.caption or '-'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('活动名称', '预约用户', '预约日期', '联系人', '联系电话', '预约状态', '创建时间')
    list_filter = ('status', 'reservation_date', 'created_at')
    search_fields = ('activity__title', 'user__username', 'contact_name', 'contact_phone')
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    def 活动名称(self, obj):
        return obj.activity.title
    
    def 预约用户(self, obj):
        return obj.user.username
    
    def 预约日期(self, obj):
        return obj.reservation_date
    
    def 联系人(self, obj):
        return obj.contact_name
    
    def 联系电话(self, obj):
        return obj.contact_phone
    
    def 预约状态(self, obj):
        status_map = {
            'pending': '待审核',
            'confirmed': '已确认',
            'cancelled': '已取消',
            'completed': '已完成'
        }
        return status_map.get(obj.status, obj.status)
    
    def 创建时间(self, obj):
        return obj.created_at

@admin.register(ActivityReview)
class ActivityReviewAdmin(admin.ModelAdmin):
    list_display = ('活动名称', '评价用户', '评分', '评价内容', '评价时间', '自动回复')
    list_filter = ('rating', 'created_at')
    search_fields = ('activity__title', 'user__username', 'comment')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def 活动名称(self, obj):
        return obj.activity.title
    
    def 评价用户(self, obj):
        return obj.user.username
    
    def 评分(self, obj):
        return f"{obj.rating}星"
    
    def 评价内容(self, obj):
        return obj.comment
    
    def 评价时间(self, obj):
        return obj.created_at
    
    def 自动回复(self, obj):
        return obj.auto_reply or '-'

@admin.register(ActivityPhoto)
class ActivityPhotoAdmin(admin.ModelAdmin):
    list_display = ('活动名称', '上传用户', '图片预览', '图片说明', '上传时间')
    list_filter = ('uploaded_at', 'activity')
    search_fields = ('activity__title', 'user__username', 'caption')
    date_hierarchy = 'uploaded_at'
    
    def 活动名称(self, obj):
        return obj.activity.title
    
    def 上传用户(self, obj):
        return obj.user.username
    
    def 图片预览(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return ""
    
    def 图片说明(self, obj):
        return obj.caption or '-'
    
    def 上传时间(self, obj):
        return obj.uploaded_at

@admin.register(ActivityCheckIn)
class ActivityCheckInAdmin(admin.ModelAdmin):
    list_display = ('活动名称', '打卡用户', '打卡时间')
    list_filter = ('check_in_time',)
    search_fields = ('activity__title', 'user__username')
    date_hierarchy = 'check_in_time'
    
    def 活动名称(self, obj):
        return obj.activity.title
    
    def 打卡用户(self, obj):
        return obj.user.username
    
    def 打卡时间(self, obj):
        return obj.check_in_time

@admin.register(ActivityLike)
class ActivityLikeAdmin(admin.ModelAdmin):
    list_display = ('点赞用户', '内容类型', '对象ID', '点赞时间')
    list_filter = ('content_type', 'liked_at')
    search_fields = ('user__username',)
    date_hierarchy = 'liked_at'
    
    def 点赞用户(self, obj):
        return obj.user.username
    
    def 内容类型(self, obj):
        return obj.content_type
    
    def 对象ID(self, obj):
        return obj.object_id
    
    def 点赞时间(self, obj):
        return obj.liked_at

@admin.register(ActivityComment)
class ActivityCommentAdmin(admin.ModelAdmin):
    list_display = ('评论用户', '内容类型', '对象ID', '评论预览', '评论时间', '自动回复')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'text')
    date_hierarchy = 'created_at'
    
    def 评论用户(self, obj):
        return obj.user.username
    
    def 内容类型(self, obj):
        return obj.content_type
    
    def 对象ID(self, obj):
        return obj.object_id
    
    def 评论预览(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    
    def 评论时间(self, obj):
        return obj.created_at
    
    def 自动回复(self, obj):
        return obj.auto_reply or '-'