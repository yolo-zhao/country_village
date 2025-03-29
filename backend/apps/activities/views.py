from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Activity, ActivityCategory, ActivityReview, ActivityPhoto
from .forms import ReservationForm, ActivityReviewForm, ActivityPhotoForm, CreateActivityForm

def activity_list(request):
    activities = Activity.objects.all()
    categories = ActivityCategory.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = ActivityCategory.objects.get(name=category_slug)
            activities = activities.filter(category=category)
        except ActivityCategory.DoesNotExist:
            pass
    context = {
        'activities': activities,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'activities/activity_list.html', context)

def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    reservation_form = ReservationForm()
    review_form = ActivityReviewForm()
    photo_form = ActivityPhotoForm()
    reviews = ActivityReview.objects.filter(activity=activity).order_by('-created_at')
    photos = ActivityPhoto.objects.filter(activity=activity).order_by('-uploaded_at')

    if request.method == 'POST':
        if 'reserve' in request.POST:
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reservation.activity = activity
                reservation.user = request.user
                reservation.save()
                return redirect('activities:activity_detail', activity_id=activity.id) # 刷新页面或跳转到成功页面
        elif 'review' in request.POST:
            review_form = ActivityReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.activity = activity
                review.user = request.user
                review.save()
                return redirect('activities:activity_detail', activity_id=activity.id)
        elif 'photo' in request.POST:
            photo_form = ActivityPhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.activity = activity
                photo.user = request.user
                photo.save()
                return redirect('activities:activity_detail', activity_id=activity.id)

    context = {
        'activity': activity,
        'reservation_form': reservation_form,
        'review_form': review_form,
        'photo_form': photo_form,
        'reviews': reviews,
        'photos': photos,
    }
    return render(request, 'activities/activity_detail.html', context)

@login_required
def farmer_activity_list(request):
    activities = Activity.objects.filter(farmer=request.user)
    return render(request, 'activities/farmer_activity_list.html', {'activities': activities})

@login_required
def create_activity(request):
    if not hasattr(request.user, 'farmerprofile'):
        return redirect('home') # 或者显示错误信息

    form = CreateActivityForm()
    if request.method == 'POST':
        form = CreateActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.farmer = request.user
            activity.save()
            form.save_m2m() # 保存多对多字段 (tags)
            return redirect('activities:farmer_activity_list') # 跳转到农户活动列表

    return render(request, 'activities/create_activity.html', {'form': form})