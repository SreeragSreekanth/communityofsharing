from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement, Event
from .forms import AnnouncementForm, EventForm
from django.core.paginator import Paginator
from django.utils.timezone import now


@login_required
def announcements_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')


    paginator = Paginator(announcements, 5)  # Show 5 announcements per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'announcements_list.html', {'page_obj': page_obj})


@login_required
def events_list(request):
    events = Event.objects.all().order_by('-event_date')


    paginator = Paginator(events, 5)  # Show 5 events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'events_list.html', {'page_obj': page_obj})

# Create Announcement
@login_required
def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcement_form.html', {'form': form, 'title': 'Create Announcement'})

# Edit Announcement
@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcement_form.html', {'form': form, 'title': 'Edit Announcement'})

# Delete Announcement
@login_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, created_by=request.user)
    announcement.delete()
    return redirect('announcements_list')

# Create Event
@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('events_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form, 'title': 'Create Event'})

# Edit Event
@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form, 'title': 'Edit Event'})

# Delete Event
@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    event.delete()
    return redirect('events_list')
