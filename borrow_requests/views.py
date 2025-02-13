from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from resources.models import Item
from .models import BorrowRequest
from .forms import BorrowRequestForm, SearchForm
from django.utils import timezone
from django.core.paginator import Paginator
# from notifications.models import Notification  # Import Notification from the other app



@login_required
def search_items(request):
    now = timezone.now().date()  # Get the current date
    form = SearchForm(request.GET or None)  # Initialize the form with GET data
    query = request.GET.get('query', '')  # Get the search query from GET parameters

    # Base queryset: Exclude the user's own items and filter by availability
    queryset = Item.objects.exclude(owner=request.user).filter(
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
def send_borrow_request(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.borrower = request.user
            borrow_request.item = item
            borrow_request.save()

            # Notify the lender
            # Notification.objects.create(
            #     user=item.owner,
            #     message=f"{request.user.username} has requested to borrow your item: {item.name}."
            # )
            # messages.success(request, "Your borrowing request has been sent.")
            # return redirect('search_items')
    else:
        form = BorrowRequestForm(initial={'item': item})
    return render(request, 'send_request.html', {'form': form, 'item': item})

@login_required
def manage_requests(request):
    # Fetch requests sent by the current user (borrower)
    sent_requests = BorrowRequest.objects.filter(borrower=request.user).order_by('-created_at')

    # Fetch requests received by the current user (lender)
    received_requests = BorrowRequest.objects.filter(item__owner=request.user).order_by('-created_at')

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'manage_requests.html', context)

@login_required
def update_request_status(request, request_id):
    # Get the borrowing request object
    borrow_request = get_object_or_404(BorrowRequest, id=request_id, item__owner=request.user)
    
    # Get the new status from the query parameters
    status = request.GET.get('status')

    # Validate the status and update the request
    if status in ['approved', 'rejected']:
        borrow_request.status = status
        borrow_request.save()

        # Notify the borrower about the status change
        # Notification.objects.create(
        #     user=borrow_request.borrower,
        #     message=f"Your request to borrow {borrow_request.item.name} has been {status}."
        # )
        messages.success(request, f"The request has been marked as {status}.")
    else:
        messages.error(request, "Invalid status provided.")

    # Redirect back to the manage requests page
    return redirect('manage_requests')