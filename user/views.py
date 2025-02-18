from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from userauth.models import Profile
from userauth.forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Avg
from resources.models import Item  # Assuming the Item model is in the 'resources' app
from datetime import date
from borrow_requests.models import BorrowRequest
from django.db.models import Q
from review.models import Review




User = get_user_model()

# User Dashboard View
@login_required
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
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.cleaned_data.get('remove_picture'):  # Check if the user wants to remove the image
                profile.profile_picture.delete(save=False)  # Delete the image file
                profile.profile_picture = None 
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('user_dashboard')
    else:
        form = EditProfileForm(instance=profile)
    
    context = {'form': form,'profile': profile}
    return render(request, 'edit_profile.html', context)


@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    available_items = Item.objects.filter(owner=user)

    # Check if there is a completed transaction between users
    has_borrow_request = BorrowRequest.objects.filter(
        (Q(borrower=request.user, item__owner=user) | Q(borrower=user, item__owner=request.user)),
        status="returned"
    ).exists()

    # Check if the logged-in user has already reviewed this user
    user_already_reviewed = Review.objects.filter(reviewer=request.user, recipient=user).exists()

    # Get all reviews for this user
    reviews = Review.objects.filter(recipient=user).select_related('reviewer')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else "No ratings yet"

    return render(request, 'view_profile.html', {
        'profile_user': user,
        'available_items': available_items,
        'user_has_borrow_request': has_borrow_request,
        'user_already_reviewed': user_already_reviewed,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })
