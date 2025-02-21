from django.http import HttpResponseForbidden
from functools import wraps

def user_only(view_func):
    """
    Decorator to restrict access to regular users only.
    Admins and staff members will be denied access.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    return _wrapped_view
