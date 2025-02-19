from django.utils.deprecation import MiddlewareMixin
from borrow_requests.models import BorrowRequest

class BorrowRequestNotificationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.pending_borrow_requests = BorrowRequest.objects.filter(
                lender=request.user, status="pending"
            ).count()
        else:
            request.pending_borrow_requests = 0
