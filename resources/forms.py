from django import forms
from .models import Item, ItemImage
from django.core.exceptions import ValidationError
from django.utils import timezone

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'expiry_date', 'availability_start', 'availability_end']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'availability_start': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'availability_end': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
        }
        help_texts = {
            'quantity': 'Enter the number of available items (optional).',
            'expiry_date': 'Specify an expiry date if applicable (optional).',
            'availability_start': 'Start date of availability (optional).',
            'availability_end': 'End date of availability (optional).',
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        return quantity  # Allow blank values

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now().date():
            raise ValidationError("Expiry date cannot be in the past.")
        return expiry_date  # Allow blank values


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