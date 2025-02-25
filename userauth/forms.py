from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Profile
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import secrets
import string
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm # Add this line
from django.contrib.auth import get_user_model



phone_number_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message='Phone number must start with 6, 7, 8, or 9 and be 10 digits long.'
)

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
        validators=[
            MinLengthValidator(10),
            phone_number_validator  # Enforce 6-9 start here
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone number'}),
        help_text="Enter a 10-digit phone number starting with 6, 7, 8, or 9."
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
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2','phone_number']

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
    

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None, email_template_name='password_reset_email.html',
             use_https=False, request=None, **kwargs):
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        
        if active_users.exists():
            user = active_users[0]
            # Generate a secure 12-character password
            characters = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(secrets.choice(characters) for _ in range(12))
            user.set_password(new_password)
            user.save()
            
            # Send email with the new password
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            
            email_context = {
                'new_password': new_password,
                'protocol': 'https' if use_https else 'http',
                'domain': domain_override or request.get_host(),
            }
            
            message = render_to_string(email_template_name, email_context)
            send_mail(
                "Your New Password - NeighborLink",
                message,
                'sreeragsreekanth236@gmail.com',  # Replace with your email
                [user.email],
                fail_silently=False,
                html_message=message
            )


class PasswordChangeCustomForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']