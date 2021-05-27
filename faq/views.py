from django.shortcuts import redirect
from django.views import View

import faq.services as services


class UpdateSectionsView(View):
    def post(self, request):
        sections = services.get_sections()
        articles = services.get_articles()
        services.create_sections_and_articles(sections, articles)
        return redirect(request.META.get('HTTP_REFERER'))

