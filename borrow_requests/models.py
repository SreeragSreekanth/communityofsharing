from django.db import models
from django.contrib.auth import get_user_model
from resources.models import Item
from django.utils import timezone

User = get_user_model()

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]

    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrow_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def mark_as_returned(self):
        """Mark the item as returned and record the timestamp."""
        self.status = 'returned'
        self.returned_at = timezone.now()
        self.save()

    def mark_as_approved(self):
        """Mark the item as returned and record the timestamp."""
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.borrower.username} → {self.item.name} ({self.status})"