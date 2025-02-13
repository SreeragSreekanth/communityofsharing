from django.db import models
from django.contrib.auth import get_user_model
from resources.models import Item

User = get_user_model()

class BorrowRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrow_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.borrower.username} requested {self.item.name} ({self.status})"