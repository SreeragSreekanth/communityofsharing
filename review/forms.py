from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.HiddenInput()  # We'll use JavaScript for the star input
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
