from django import forms
from .models import SystemAnnouncement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = SystemAnnouncement
        fields = ['title', 'content', 'is_active']