from django.utils.deprecation import MiddlewareMixin
import logging
from django.shortcuts import redirect


logger = logging.getLogger(__name__)

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"User {request.user} accessed {request.path}")

class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware to prevent caching of sensitive pages.
    """
    def process_response(self, request, response):
        # Prevent caching for all responses
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response