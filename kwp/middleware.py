import traceback

from proposal.services import create_error_message
from django.template import loader
from django.http import HttpResponse
from django.core.signals import got_request_exception


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        exception_name = exception.__class__.__name__
        accepted_exceptions = ['Http404', 'Http403', 'Http400']
        if exception_name not in accepted_exceptions:
            create_error_message(
                request=request,
                error_message=traceback.format_exc(),
                error_type=exception.__class__.__name__
            )
            return HttpResponse(loader.render_to_string('503.html'), status=503)
