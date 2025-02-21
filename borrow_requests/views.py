from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from resources.models import Item
from .models import BorrowRequest
from .forms import BorrowRequestForm, SearchForm
from django.utils.timezone import now
from django.core.paginator import Paginator
from notifications.models import Notification 
from django.db.models import Q
from django.utils import timezone
from user.decorators import user_only
from django.utils.timezone import now




@login_required
@user_only
def search_items(request):
    now = timezone.now().date()  # Get the current date
    form = SearchForm(request.GET or None)  # Initialize the form with GET data
    query = request.GET.get('query', '')  # Get the search query from GET parameters

    # Get items that are currently borrowed
    borrowed_item_ids = BorrowRequest.objects.filter(status='approved').values_list('item_id', flat=True)

    # Base queryset: Exclude the user's own items & filter by availability
    queryset = Item.objects.exclude(owner=request.user).exclude(id__in=borrowed_item_ids).filter(
        availability_start__lte=now,
        availability_end__gte=now
    ).order_by('-created_at').distinct()  # Ensure stable ordering and avoid duplicates

    # Apply search filter
    if query:
        queryset = queryset.filter(name__icontains=query)

    # Paginate the results
    paginator = Paginator(queryset, 6)  # Show 6 items per page
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    return render(request, 'search_items.html', {'form': form, 'items': items, 'query': query})



@login_required
@user_only
def request_borrow(request, item_id):
    """Allows a user to request to borrow an item with a return date, even after returning it."""
    item = get_object_or_404(Item, id=item_id)

    if item.owner == request.user:
        messages.error(request, "You cannot borrow your own item.")
        return redirect('item_detail', item.id)

    # Check if there is an active borrow request (pending or approved)
    active_request = BorrowRequest.objects.filter(
        borrower=request.user, item=item, status__in=['pending', 'approved']
    ).exists()

    if active_request:
        messages.error(request, "You already have an active request for this item.")
        return redirect('item_detail', item.id)

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            return_date = form.cleaned_data['return_date']

            BorrowRequest.objects.create(
                borrower=request.user,
                lender=item.owner,
                item=item,
                status='pending',
                return_date=return_date  # Save return date
            )

            Notification.objects.create(
                user=item.owner,
                message=f"{request.user.username} has requested to borrow {item.name} until {return_date}."
            )

            messages.success(request, "Your borrow request has been sent.")
            return redirect('search_items')  # Redirect to manage requests page
    else:
        form = BorrowRequestForm()

    return render(request, 'request_borrow.html', {'form': form, 'item': item})


@login_required
@user_only
def manage_requests(request):
    today = now().date()

    # Get all overdue requests
    overdue_requests = BorrowRequest.objects.filter(
        status='approved', 
        return_date__lt=today
    )

    count = overdue_requests.count()

    # Process each overdue request
    for req in overdue_requests:
        req.status = 'overdue'
        req.save()

        # Send notification to the borrower
        Notification.objects.create(
            user=req.borrower,
            message=f"Your borrow request for '{req.item.name}' is now overdue. Please return it as soon as possible.",
        )

        Notification.objects.create(
            user=req.lender,
            message=f"The item '{req.item.name}' you lended is now overdue.",
        )

        # Auto-decline pending requests if the return date is overdue
    timed_out_requests = BorrowRequest.objects.filter(
        return_date__lt=today,  
        status='pending'
    )

    for borrow_request in timed_out_requests:
        borrow_request.status = 'timed_out'  # Auto-decline
        borrow_request.save()
        messages.info(request, f"Your borrow request for '{borrow_request.item.name}' has timed out.")

        # Notify borrower
        Notification.objects.create(
            user=borrow_request.borrower,
            message=f"Your borrow request for '{borrow_request.item.name}' has timed out."
        )

        Notification.objects.create(
            user=borrow_request.lender,
            message=f"The borrow request for '{borrow_request.item.name}' from '{borrow_request.borrower}' has timed out."
        )

    # Show message if any were marked overdue
    if count > 0:
        messages.warning(request, f"{count} request(s) marked as overdue.")
    """Display both sent and received borrow requests."""
    sent_requests = BorrowRequest.objects.filter(borrower=request.user).order_by('-requested_at')
    received_requests = BorrowRequest.objects.filter(item__owner=request.user).order_by('-requested_at')

    return render(request, 'manage_requests.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })


def approve_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    borrow_request.status = 'approved'
    borrow_request.save()
    borrow_request.mark_as_approved()
    Notification.objects.create(
        user=borrow_request.borrower,
        message=f"Your borrow request for '{borrow_request.item.name}' has been approved."
    )
    messages.success(request, "Request approved successfully.")
    return redirect('manage_requests')

def reject_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    borrow_request.status = 'rejected'
    borrow_request.save()
    Notification.objects.create(
        user=borrow_request.borrower,
        message=f"Your borrow request for '{borrow_request.item.name}' has been rejected."
    )
    messages.warning(request, "Request rejected.")
    return redirect('manage_requests')

def mark_as_returned(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    borrow_request.mark_as_returned()
    messages.info(request, "Item marked as returned.")
    return redirect('manage_requests')


@login_required
@user_only
def borrowed_items(request):
    """
    Displays BorrowRequests accepted by the current user (borrowed items).
    """
    borrowed_items = BorrowRequest.objects.filter(
        borrower=request.user, status__in=['approved', 'returned']
    ).select_related('item', 'item__owner').order_by('-approved_at')

    return render(request, 'borrowed_items.html', {
        'borrowed_items': borrowed_items, 
    })



@login_required
@user_only
def lended_items(request):
    """
    Displays BorrowRequests for items owned by the current user (lended items).
    Shows requests that are either approved or returned.
    """
    lended_items = BorrowRequest.objects.filter(
        item__owner=request.user,  
        status__in=['approved', 'returned']
    ).select_related('item', 'borrower').order_by('-approved_at')


    return render(request, 'lended_items.html', {
        'lended_items': lended_items,
        # 'reviewed_requests': reviewed_requests,  # Pass dictionary to template
    })

