from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
import datetime
from django.views import View
from celery.services import (
    create_sections_and_articles,
    get_articles,
    get_sections
)
from celery.models import Section, Article
from .models import Session, SessionEvent
import proposal.services as services


class ConfirmationView(View):
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        proposal = services.get_proposal(proposal_id)
        request.session['client_ip'] = request.META.get("REMOTE_ADDR")
        if proposal:
            return render(request, 'confirmation.html', {'proposal_id': proposal_id})
        else:
            if request.session['email']:
                Session.objects.get_or_create(
                    proposal_id=proposal_id,
                    email=request.session['email'],
                    is_emailvalid=request.session['is_emailvalid'],
                    message='Trying to access a non-existent Proposal.',
                    client_ip=request.session['client_ip']
                )
            else:
                Session.objects.get_or_create(
                    proposal_id=proposal_id,
                    message='Trying to access a non-existent Proposal.',
                    client_ip=request.session['client_ip']
                )

    @services.clock
    def post(self, request, proposal_id) -> HttpResponse:
        email = request.POST['email']
        proposal = services.get_proposal(proposal_id)
        request.session['email'] = email
        request.session['proposal_account_id'] = proposal['Account__c']
        email_validation = services.user_email_validation(proposal['Account__c'], email)
        if email_validation:
            request.session['contact_id'] = email_validation['contact_id']
            request.session['is_emailvalid'] = True
            is_contactcreated = email_validation['is_contactcreated']
            if not proposal['Published__c']:
                Session.objects.get_or_create(
                    proposal_id=proposal_id,
                    email=email,
                    is_emailvalid=True,
                    account_id=proposal['Account__c'],
                    client_ip=request.session['client_ip'],
                    is_proposalexists=True,
                    contact_id=request.session['contact_id'],
                    is_contactcreated=is_contactcreated,
                    message='Proposal not published'
                )
                pass
            session = Session.objects.get_or_create(
                proposal_id=proposal_id,
                email=email,
                is_emailvalid=True,
                account_id=proposal['Account__c'],
                client_ip=request.session['client_ip'],
                is_proposalexists=True,
                contact_id=request.session['contact_id'],
                is_contactcreated=is_contactcreated
            )
            request.session['session_id'] = session[0].pk
            return redirect('proposal', proposal_id)
        else:
            Session.objects.get_or_create(
                proposal_id=proposal_id,
                email=email,
                message='Trying to access Proposal with a non-valid Email.',
                client_ip=request.session['client_ip']
            )
            pass


class ProposalView(View):
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        section_response = get_sections()
        article_response = get_articles()
        create_sections_and_articles(section_response, article_response)
        try:
            email = request.session['email']
            email_validation = services.user_email_validation(request.session['proposal_account_id'], email)
        except KeyError:
            email_validation = False
        if not email_validation:
            return redirect('confirmation', proposal_id)
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
        try:
            time_spent = request.POST['time_spent']
        except KeyError:
            time_spent = None
        try:
            message = request.POST['message']
        except KeyError:
            message = None
        services.create_event_record(
            session_id=request.session['session_id'],
            event_type=request.POST['event_type'],
            event_name=request.POST['event_name'],
            time_spent=time_spent,
            message=message,
            proposal_id=proposal_id,
            proposal_account_id=request.session['proposal_account_id'],
            contact_id=request.session['contact_id']
        )
        return HttpResponse('ok')
