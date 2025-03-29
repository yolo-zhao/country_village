from django.shortcuts import render, redirect
from .models import SystemAnnouncement, HomePageOrder
from django.contrib.admin.views.decorators import staff_member_required

def homepage(request):
    announcements = SystemAnnouncement.objects.filter(is_active=True).order_by('-created_at')
    # 这里可以添加获取活动和产品的逻辑，并根据 HomePageOrder 进行排序
    activities = [] # 示例
    products = []   # 示例

    context = {
        'announcements': announcements,
        'activities': activities,
        'products': products,
    }
    return render(request, 'core/homepage.html', context)

@staff_member_required
def create_announcement(request):
    # 如果您想提供一个非 Admin 界面的公告创建方式
    from .forms import AnnouncementForm
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:homepage') # 假设您的首页 URL name 是 homepage
    else:
        form = AnnouncementForm()
    return render(request, 'core/create_announcement.html', {'form': form})

# 您可能还需要编辑和删除公告的视图 (同样可以使用 @staff_member_required 装饰器)