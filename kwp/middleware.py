import traceback

from django.http import HttpResponse
from django.template import loader

from proposal.models import Session
from proposal.services import create_error_message


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if "admin" in request.get_full_path():
            request.session.set_expiry(3600)
        return self._get_response(request)

    def process_exception(self, request, exception):
        exception_name = exception.__class__.__name__
        accepted_exceptions = ["Http404", "Http403", "Http400"]
        if exception_name not in accepted_exceptions:
            create_error_message(
                request=request, error_message=traceback.format_exc(), error_type=exception.__class__.__name__
            )
            session_id = request.session.get("session_id")
            if session_id:
                session = Session.objects.all().get(pk=session_id)
                session.with_error = "Yes"
                session.save(update_fields=["with_error"])
            return HttpResponse(loader.render_to_string("503.html"), status=503)
