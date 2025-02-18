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
# from reviews.models import Review




@login_required
def search_items(request):
    now = timezone.now().date()  # Get the current date
    form = SearchForm(request.GET or None)  # Initialize the form with GET data
    query = request.GET.get('query', '')  # Get the search query from GET parameters

    # Base queryset: Exclude the user's own items and filter by availability
    borrowed_item_ids = BorrowRequest.objects.filter(status='approved').values_list('item_id', flat=True)
    # Base queryset: Exclude the user's own items and items that are currently borrowed or not returned
    queryset = Item.objects.exclude(owner=request.user).exclude(id__in=borrowed_item_ids).filter(
        availability_start__lte=now,
        availability_end__gte=now
    )

    # Apply search query if provided
    if query:
        queryset = queryset.filter(name__icontains=query)

    # Paginate the results
    paginator = Paginator(queryset, 6)  # Show 6 items per page
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    return render(request, 'search_items.html', {'form': form, 'items': items, 'query': query})


@login_required
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
            return redirect('manage_requests')  # Redirect to manage requests page
    else:
        form = BorrowRequestForm()

    return render(request, 'request_borrow.html', {'form': form, 'item': item})


@login_required
def manage_requests(request):
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
def borrowed_items(request):
    """
    Displays BorrowRequests accepted by the current user (borrowed items).
    """
    borrowed_items = BorrowRequest.objects.filter(
        borrower=request.user, status__in=['approved', 'returned']
    ).select_related('item', 'item__owner')

    return render(request, 'borrowed_items.html', {
        'borrowed_items': borrowed_items, 
    })



@login_required
def lended_items(request):
    """
    Displays BorrowRequests for items owned by the current user (lended items).
    Shows requests that are either approved or returned.
    """
    lended_items = BorrowRequest.objects.filter(
        item__owner=request.user,  
        status__in=['approved', 'returned']
    ).select_related('item', 'borrower').order_by('-approved_at')

    # ✅ Create a dictionary to track if the owner has reviewed each request
    # reviewed_requests = {
    #     lend.id: Review.objects.filter(
    #         reviewer=request.user, borrow_request=lend
    #     ).exists()
    #     for lend in lended_items
    # }

    return render(request, 'lended_items.html', {
        'lended_items': lended_items,
        # 'reviewed_requests': reviewed_requests,  # Pass dictionary to template
    })

