from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_approved = models.BooleanField(default=False)
    

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    bio = models.TextField(blank=True, null=True)  # Optional bio
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for profile creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for profile updates

    def __str__(self):
        return f"{self.user.username}'s Profile"