from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def view_notifications(request):
    # Fetch all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark unread notifications as read
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)

    return render(request, 'notifications.html', {'notifications': notifications})