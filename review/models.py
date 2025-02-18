from django.db import models
from django.contrib.auth import get_user_model
from borrow_requests.models import BorrowRequest

User =get_user_model()

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    transaction = models.ForeignKey(BorrowRequest, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'recipient')

    def __str__(self):
        return f"Review from {self.reviewer} to {self.recipient} - {self.rating} Stars"
