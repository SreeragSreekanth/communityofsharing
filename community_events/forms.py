from django import forms
from .models import Announcement, Event
from django.utils import timezone


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']



class EventForm(forms.ModelForm):
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M')  # Set min value dynamically
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date']

