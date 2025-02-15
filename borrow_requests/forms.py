from django import forms
from .models import BorrowRequest


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = []


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search by name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name'}),
    )