from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    availability_start = models.DateField(null=True, blank=True, help_text="Start date of availability")
    availability_end = models.DateField(null=True, blank=True, help_text="End date of availability")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def is_borrowed(self):
        return self.borrow_history.filter(returned_at__isnull=True).exists()
    
    
    def __str__(self):
        return self.name


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return f"Image for {self.item.name}"