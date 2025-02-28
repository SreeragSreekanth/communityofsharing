from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from borrow_requests.models import BorrowRequest
from django.db.models import Q
from django.contrib.auth import get_user_model
from user.decorators import user_only


User = get_user_model()

@login_required
@user_only
def leave_review(request, user_id):
    recipient = get_object_or_404(User, id=user_id)

    has_transaction = BorrowRequest.objects.filter(
        (Q(borrower=request.user, item__owner=recipient) |
         Q(borrower=recipient, item__owner=request.user)),
        status="returned"
    ).exists()

    if not has_transaction:
        messages.error(request, "You can only review users you've completed a transaction with.")
        return redirect('view_profile', user_id=recipient.id)

    if Review.objects.filter(reviewer=request.user, recipient=recipient).exists():
        messages.warning(request, "You have already reviewed this user.")
        return redirect('view_profile', user_id=recipient.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            print("Form is valid, saving:", form.cleaned_data)  # Debug
            review = form.save(commit=False)
            review.reviewer = request.user
            review.recipient = recipient
            review.transaction = BorrowRequest.objects.filter(
                (Q(borrower=request.user, item__owner=recipient) |
                 Q(borrower=recipient, item__owner=request.user)),
                status="returned"
            ).first()
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('view_profile', user_id=recipient.id)
        else:
            print("Form validation failed, errors:", form.errors)  # Debug
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form, 'recipient': recipient})

@login_required
@user_only
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated successfully.")
            return redirect('view_profile', user_id=review.recipient.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    review.delete()
    messages.success(request, "Your review has been deleted successfully.")
    return redirect('view_profile', user_id=review.recipient.id)

