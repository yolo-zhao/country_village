from django.contrib import admin
from .models import ActivityCategory, Tag, Activity, ActivityImage, Reservation, ActivityReview, ActivityPhoto, ActivityCheckIn, ActivityLike, ActivityComment



class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'end_time', 'farmer')
    list_filter = ('category', 'farmer', 'start_time')
    search_fields = ('title', 'description', 'location')
    inlines = [ActivityImageInline]
    prepopulated_fields = {'slug': ('title',)}

# admin.site.register(Activity, ActivityAdmin)
# admin.site.register(ActivityCategory)
# admin.site.register(Tag)
# admin.site.register(Reservation)
# admin.site.register(ActivityReview)
# admin.site.register(ActivityPhoto)
# admin.site.register(ActivityCheckIn)
# # 对于通用外键模型，可以直接注册
# admin.site.register(ActivityLike)
# admin.site.register(ActivityComment)
admin.site.register(ActivityCategory)
admin.site.register(Tag)
admin.site.register(Activity)
admin.site.register(ActivityImage)
admin.site.register(Reservation)
admin.site.register(ActivityReview)
admin.site.register(ActivityPhoto)
admin.site.register(ActivityCheckIn)
admin.site.register(ActivityLike)
admin.site.register(ActivityComment)