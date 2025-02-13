from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from resources.models import Item
from django.utils import timezone 
from django.db import models


User = get_user_model()
# Helper function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser



@login_required
@user_passes_test(is_superuser)  # Only superusers can access this view
def admin_dashboard(request):
    # Fetch analytics data
    total_users = User.objects.filter(is_superuser=False).count()
    approved_users = User.objects.filter(is_approved=True, is_superuser=False).count()
    pending_users = User.objects.filter(is_approved=False, is_superuser=False).count()

    # Item analytics
    total_items = Item.objects.count()
    now = timezone.now().date()  # Get the current date

    # Available items: Items with availability_start and/or availability_end in the future or ongoing
    available_items = Item.objects.filter(
        availability_start__lte=now,  # Start date is today or earlier
        availability_end__gte=now    # End date is today or later
    ).count()

    # Unavailable items: Items with no dates OR end date has passed
    unavailable_items = Item.objects.filter(
        models.Q(availability_end__lt=now) |  # End date has passed
        models.Q(availability_start__isnull=True, availability_end__isnull=True)  # No dates set
    ).count()

    context = {
        'total_users': total_users,
        'approved_users': approved_users,
        'pending_users': pending_users,
        'total_items': total_items,
        'available_items': available_items,
        'unavailable_items': unavailable_items,
    }
    return render(request, 'admin_dashboard.html', context)


# Manage Users View (List all users)
@login_required
@user_passes_test(is_superuser)  # Only superusers can access this view
def manage_users(request):
    users = User.objects.filter(is_approved=True,is_superuser=False)
    return render(request, 'manage_users.html', {'users': users})

# Pending Users View (List users awaiting approval)
@login_required
@user_passes_test(is_superuser)
def pending_users(request):
    pending_users = User.objects.filter(is_approved=False)
    return render(request, 'pending_users.html', {'pending_users': pending_users})

# Approve User
@login_required
@user_passes_test(is_superuser)
def approve_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f"User '{user.username}' has been approved.")
    return redirect('pending_users')

# Decline User
@login_required
@user_passes_test(is_superuser)
def decline_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()  # Delete the user account
    messages.success(request, f"User '{user.username}' has been declined and removed.")
    return redirect('pending_users')

# Delete User
@login_required
@user_passes_test(is_superuser)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, f"User '{user.username}' has been deleted.")
    return redirect('manage_users')


@login_required
@user_passes_test(is_superuser)
def manage_items(request):
    query = request.GET.get('search', '')
    items = Item.objects.filter(name__icontains=query) if query else Item.objects.all()
    return render(request, 'manage_items.html', {'items': items})