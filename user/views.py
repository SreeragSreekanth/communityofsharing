from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from userauth.models import Profile
from userauth.forms import EditProfileForm,PasswordChangeCustomForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Avg
from resources.models import Item  # Assuming the Item model is in the 'resources' app
from datetime import date
from borrow_requests.models import BorrowRequest
from django.db.models import Q
from review.models import Review
from user.decorators import user_only
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone




User = get_user_model()

# User Dashboard View
@login_required
@user_only
def user_dashboard(request):
    profile = request.user.profile

    # Fetch reviews received by the logged-in user
    received_reviews = Review.objects.filter(recipient=request.user)

    context = {
        'profile': profile,
        'received_reviews': received_reviews,
    }
    return render(request, 'user_dashboard.html', context)

# Edit Profile View
@login_required
@user_only
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure profile exists

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.cleaned_data.get('remove_picture'):
                if profile.profile_picture  and profile.profile_picture.name != "profile_pics/default.webp":  # Ensure profile_picture exists before deleting
                    profile.profile_picture.delete(save=False)  # Delete the file
                profile.profile_picture = "profile_pics/default.webp"  # Set profile_picture to None
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('user_dashboard')
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})



@login_required
def view_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    profile = profile_user.profile
    now = timezone.now().date()

    # Get items owned by the user that are available for borrowing
    borrowed_item_ids = BorrowRequest.objects.filter(status='approved').values_list('item_id', flat=True)
    
    available_items = Item.objects.filter(
        owner=profile_user,
        availability_start__lte=now,
        availability_end__gte=now
    ).exclude(id__in=borrowed_item_ids)

    # Check if there is a completed transaction between users (for reviewing eligibility)
    has_borrow_request = BorrowRequest.objects.filter(
        (Q(borrower=request.user, item__owner=profile_user) | Q(borrower=profile_user, item__owner=request.user)),
        status="returned"
    ).exists()

    # Check if the logged-in user has already reviewed this user
    user_already_reviewed = Review.objects.filter(reviewer=request.user, recipient=profile_user).exists()

    # Get all reviews for this user
    reviews = Review.objects.filter(recipient=profile_user).select_related('reviewer')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else "No ratings yet"

    return render(request, 'view_profile.html', {
        'profile_user': profile_user,
        'available_items': available_items,
        'user_has_borrow_request': has_borrow_request,
        'user_already_reviewed': user_already_reviewed,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been updated successfully!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeCustomForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})