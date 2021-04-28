from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView

from kwp import settings
from faq.models import Section
from .models import Session
import proposal.services as services
from .forms import VerificationForm


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
                    email_valid=request.session['is_emailvalid'],
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
        form = VerificationForm(request.POST)
        if not form.is_valid():
            request.method = 'GET'
            return HttpResponse({'error': True})
        email = request.POST['email']
        request.session['email'] = email
        proposal = services.get_proposal(proposal_id)
        if email == settings.TRUSTED_EMAIL:
            services.additional_trusted_email_confirmation(request, proposal_id)
            return redirect('proposal', proposal_id)
        request.session['proposal_account_id'] = proposal['Account__c']
        email_validation = services.user_email_validation(proposal['Account__c'], email)
        if email_validation:
            request.session['contact_account_id'] = email_validation['contact_account_id']
            request.session['contact_id'] = email_validation['contact_id']
            request.session['is_emailvalid'] = True
            is_contactcreated = email_validation['is_contactcreated']
            services.additional_confirmation(request, is_contactcreated, proposal, proposal_id)
            return redirect('proposal', proposal_id)
        else:
            Session.objects.get_or_create(
                proposal_id=proposal_id,
                email=request.session['email'],
                message='Trying to access Proposal with a non-valid Email.',
                client_ip=request.session['client_ip']
            )
            pass


class ProposalView(View):
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        try:
            services.additional_email_verification(request, proposal_id)
        except KeyError:
            return redirect('confirmation', proposal_id)
        sections = Section.objects.filter(is_active=True).all()
        proposal = services.get_proposal(proposal_id)
        request.session['proposal_name'] = proposal['Name']
        request.session['proposal_account_id'] = proposal['Account__c']
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
    def get(self, request, proposal_id) -> HttpResponse:
        try:
            services.additional_email_verification(request, proposal_id)
        except KeyError:
            pass
        document = services.get_pdf_for_review(proposal_id)
        document_body = document['document']
        document_title = document['title']
        return render(request, 'pdf.html', {'proposal_id': proposal_id,
                                            'document_body': document_body,
                                            'document_title': document_title
                                            })


class PDFViewerView(TemplateView):
    template_name = 'viewer.html'


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
        if request.session['email'] == settings.TRUSTED_EMAIL:
            request.session['contact_id'] = None
        request.session['event_type'] = request.POST['event_type']
        request.session['event_name'] = request.POST['event_name']
        services.create_event_record(
            session_id=request.session['session_id'],
            event_type=request.POST['event_type'],
            event_name=request.POST['event_name'],
            time_spent=time_spent,
            message=message,
            proposal_id=proposal_id,
            proposal_account_id=request.session['proposal_account_id'],
            contact_id=request.session['contact_id'],
            email=request.session['email'],
            contact_account_id=request.session['contact_account_id'],
            proposal_name=request.session['proposal_name']
        )
        return HttpResponse('ok')
