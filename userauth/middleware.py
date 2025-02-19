from django.utils.deprecation import MiddlewareMixin
import logging
from django.shortcuts import redirect


logger = logging.getLogger(__name__)

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"User {request.user} accessed {request.path}")

class DisableBackAfterLogoutMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path in ["/login/", "/logout/"]:  # Add other auth-related paths if needed
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response