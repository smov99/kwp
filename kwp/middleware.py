from proposal.services import create_error_message
from django.template import loader
from django.http import HttpResponse


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        create_error_message(
            request=request,
            error_message=exception,
            error_type='Exception'
        )
        return HttpResponse(loader.render_to_string('503.html'), status=503)
