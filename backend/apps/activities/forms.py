from django import forms
from .models import Reservation, ActivityReview, ActivityPhoto, Activity

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'contact_name', 'contact_phone']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'})
        }

class ActivityReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, str(i) + '星') for i in range(1, 6)], widget=forms.RadioSelect)
    class Meta:
        model = ActivityReview
        fields = ['rating', 'comment']

class ActivityPhotoForm(forms.ModelForm):
    class Meta:
        model = ActivityPhoto
        fields = ['image', 'caption']

class CreateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'category', 'tags', 'description', 'start_time', 'end_time', 'location', 'cover_image', 'max_participants']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tags': forms.CheckboxSelectMultiple,
        }