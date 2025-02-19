from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from community_events.models import Event, Announcement

class EventAnnouncementMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user and not isinstance(request.user, AnonymousUser):
            # Get the latest events and announcements
            new_events = Event.objects.filter(created_at__gt=request.user.profile.last_checked)
            new_announcements = Announcement.objects.filter(created_at__gt=request.user.profile.last_checked)

            # Store counts in request
            request.new_events_count = new_events.count()
            request.new_announcements_count = new_announcements.count()
        else:
            request.new_events_count = 0
            request.new_announcements_count = 0
