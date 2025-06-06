from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Item, ItemImage
from .forms import ItemForm, ItemImageForm
from .models import Item
from borrow_requests.models import BorrowRequest
from borrow_requests.forms import BorrowRequestForm
from notifications.models import Notification
from django.contrib import messages
from django.utils import timezone
from user.decorators import user_only


@login_required
@user_only
def create_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        images = request.FILES.getlist('images')  # Get all uploaded images

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.owner = request.user
            item.save()

            for image in images:
                ItemImage.objects.create(item=item, image=image)

            return redirect('item_list')
    else:
        item_form = ItemForm()

    context = {'item_form': item_form}
    return render(request, 'create_item.html', context)


@login_required
@user_only
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, owner=request.user)

    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item)
        images = request.FILES.getlist('images')  # Get all uploaded images
        delete_images = request.POST.getlist('delete_images')  # Get IDs of images to delete

        if item_form.is_valid():
            item_form.save()

            # Save new images
            for image in images:
                ItemImage.objects.create(item=item, image=image)

            # Delete marked images
            for image_id in delete_images:
                image = ItemImage.objects.filter(id=image_id).first()
                if image:
                    image.delete()

            return redirect('item_detail', item_id=item.id)
    else:
        item_form = ItemForm(instance=item)

    context = {'item_form': item_form, 'item': item}
    return render(request, 'edit_item.html', context)


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, owner=request.user)
    item.delete()
    return redirect('item_list')

@login_required
@user_only
def item_list(request):
    items = Item.objects.filter(owner=request.user)
    context = {'items': items}
    return render(request, 'item_list.html', context)

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    now = timezone.now().date()

    # Check if the item is available for borrowing
    is_available = (
        item.availability_start and item.availability_end and
        item.availability_start <= now <= item.availability_end
    )

    context = {
        'item': item,
        'is_available': is_available,
        'now': now,
    }
    return render(request, 'item_detail.html', context)