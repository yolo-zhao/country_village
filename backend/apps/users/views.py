from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TouristProfileForm, FarmerProfileForm, UserForm
from .models import TouristProfile, FarmerProfile


@login_required
def tourist_profile(request):
    try:
        tourist_profile = request.user.touristprofile
    except TouristProfile.DoesNotExist:
        tourist_profile = TouristProfile(user=request.user)

    user_form = UserForm(instance=request.user)
    profile_form = TouristProfileForm(instance=tourist_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = TouristProfileForm(request.POST, instance=tourist_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:tourist_profile') # 假设您有一个名为 tourist_profile 的 URL

    return render(request, 'users/tourist_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def farmer_profile(request):
    try:
        farmer_profile = request.user.farmerprofile
    except FarmerProfile.DoesNotExist:
        farmer_profile = FarmerProfile(user=request.user)

    user_form = UserForm(instance=request.user)
    profile_form = FarmerProfileForm(instance=farmer_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = FarmerProfileForm(request.POST, instance=farmer_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:farmer_profile') # 假设您有一个名为 farmer_profile 的 URL

    return render(request, 'users/farmer_profile.html', {'user_form': user_form, 'profile_form': profile_form})