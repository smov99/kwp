from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from celery.services import (
    create_sections_and_articles,
    get_articles,
    get_sections
)
from celery.models import Section, Article
import proposal.services as services


class ConfirmationView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        proposal = services.get_proposal(proposal_id)
        if proposal:
            return render(request, 'confirmation.html', {'proposal_id': proposal_id})
        else:
            return redirect('error-404')

    def post(self, request: HttpRequest, proposal_id) -> HttpResponse:
        email = request.POST['email']
        proposal = services.get_proposal(proposal_id)
        if services.user_email_validation(proposal['Account__c'], 'juan.torres@logrand.com'):
            return redirect('proposal', proposal_id)
        else:
            pass


class ProposalView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        # section_response = get_sections()
        # article_response = get_articles()
        # create_sections_and_articles(section_response, article_response)
        sections = Section.objects.all()
        proposal = services.get_proposal(proposal_id)
        if proposal:
            welcome_message = proposal['Welcome_message__c']
            creator = services.get_proposals_creator(proposal['CreatedById'])
            user_name = creator['Name']
            return render(request, 'proposal.html', {'proposal_id': proposal_id,
                                                     'sections': sections,
                                                     'message': welcome_message,
                                                     'user_name': user_name})
        else:
            return redirect('error-404')


class ProposalPDFView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        return render(request, 'pdf.html', {'proposal_id': proposal_id})


class EventsView(View):
    def post(self, request, proposal_id):
        print(request.POST['event_type'])
        print(request.POST['event_name'])
        print(proposal_id)
        return HttpResponse('ok')
