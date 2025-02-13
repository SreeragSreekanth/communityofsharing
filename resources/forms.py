from django import forms
from .models import Item, ItemImage
from django.core.exceptions import ValidationError
from django.utils import timezone

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'availability_start','availability_end']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'availability_start': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'availability_end': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
        }


    def clean_availability_start(self):
        availability_start = self.cleaned_data.get('availability_start')
        if availability_start and availability_start < timezone.now().date():
            raise ValidationError("Availability start date cannot be in the past.")
        return availability_start

    def clean_availability_end(self):
        availability_end = self.cleaned_data.get('availability_end')
        if availability_end and availability_end < timezone.now().date():
            raise ValidationError("Availability end date cannot be in the past.")
        return availability_end

    def clean(self):
        cleaned_data = super().clean()
        availability_start = cleaned_data.get('availability_start')
        availability_end = cleaned_data.get('availability_end')

        if availability_start and availability_end and availability_start > availability_end:
            raise ValidationError("Availability start date must be before availability end date.")

        return cleaned_data

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']