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
    @services.clock
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        proposal = services.get_proposal(proposal_id)
        if proposal:
            return render(request, 'confirmation.html', {'proposal_id': proposal_id})
        else:
            pass

    def post(self, request, proposal_id) -> HttpResponse:
        email = request.POST['email']
        request.session['email'] = email
        proposal = services.get_proposal(proposal_id)
        if services.user_email_validation(proposal['Account__c'], email):
            return redirect('proposal', proposal_id)
        else:
            pass


class ProposalView(View):
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        # section_response = get_sections()
        # article_response = get_articles()
        # create_sections_and_articles(section_response, article_response)
        sections = Section.objects.all()
        proposal = services.get_proposal(proposal_id)
        if proposal:
            request.session['is_proposalexist'] = proposal['Published__c']
            welcome_message = proposal['Welcome_message__c']
            creator = services.get_proposals_creator(proposal['CreatedById'])
            client_name = services.get_client_name(proposal['Account__c'])
            img = services.get_document(creator['MediumPhotoUrl'])
            creator_name = creator['Name']
            return render(request, 'proposal.html', {'proposal_id': proposal_id,
                                                     'sections': sections,
                                                     'message': welcome_message,
                                                     'creator_name': creator_name,
                                                     'img': img,
                                                     'client_name': client_name
                                                     })
        else:
            return redirect('error-404')


class ProposalPDFView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        return render(request, 'pdf.html', {'proposal_id': proposal_id})


class EventsView(View):
    def post(self, request, proposal_id):
        print(request.POST['event_type'])
        print(request.POST['event_name'])
        try:
            print(request.POST['time_spent'])
        except:
            pass
        try:
            print(request.POST['message'])
        except:
            pass
        print(proposal_id)
        return HttpResponse('ok')
