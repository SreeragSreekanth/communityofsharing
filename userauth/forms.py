from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Profile
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


# Signup Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        help_text=""
    )
    first_name = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter you firstname'}),
        help_text=""
    )
    last_name = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter you lastname'}),
        help_text=""
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        help_text=""
    )
    phone_number = forms.CharField(
        required=True,
        max_length=10,
        validators=[MinLengthValidator(10)],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone number'}),
        help_text=""
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
        help_text="",
        label="password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        help_text="",
        label="confirm your password"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        help_text=""
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        help_text=""
    )


class EditProfileForm(forms.ModelForm):
    remove_picture = forms.BooleanField(required=False, label="Remove profile picture")  # Checkbox for deletion

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture','remove_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        remove_picture = cleaned_data.get("remove_picture")

        if remove_picture:
            cleaned_data["profile_picture"] = None  # Ensure the field is set to None

        return cleaned_data