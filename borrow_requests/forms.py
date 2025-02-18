from django import forms
from .models import BorrowRequest
from django.utils import timezone


class BorrowRequestForm(forms.ModelForm):
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}), 
        required=True
    )

    class Meta:
        model = BorrowRequest
        fields = ['return_date']

class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search by name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name'}),
    )