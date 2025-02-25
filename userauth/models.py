from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.validators import RegexValidator


# Create your models here.
class User(AbstractUser):
    is_approved = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)  # Optional phone number

    

    def __str__(self):
        return self.username
    


def default_profile_picture():
    return "profile_pics/default.webp"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)  # Optional bio
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='profile_pics/default.webp')  # Profile picture
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for profile creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for profile updates
    last_checked = models.DateTimeField(default=now)  # Stores last seen time


    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_profile_picture_url(self):
        """Returns a valid profile picture URL, handling missing files."""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return "/media/profile_pics/default.webp"  # Ensure a fallback image