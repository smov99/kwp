import os

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404

from kwp import settings
from faq.models import Section
from .models import Session
import proposal.services as services
from .forms import VerificationForm


class ConfirmationView(View):
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        proposal = services.get_proposal(proposal_id)
        if proposal:
            request.session['proposal'] = proposal
            return render(request, 'confirmation.html', {'proposal_id': proposal_id})
        else:
            email = request.session.get('email')
            services.create_failed_session_record(request, proposal_id, email)

    @services.clock
    def post(self, request, proposal_id) -> HttpResponse:
        form = VerificationForm(request.POST)
        if not form.is_valid():
            request.method = 'GET'
            return HttpResponse({'error': True})
        email = request.POST['email']
        request.session['email'] = email
        proposal = request.session['proposal']
        if email == settings.TRUSTED_EMAIL:
            services.additional_trusted_email_confirmation(request, proposal_id)
            request.session['is_emailvalid'] = True
            request.session['document'] = services.get_pdf_for_review(proposal_id)
            return redirect('proposal', proposal_id)
        request.session['proposal_account_id'] = proposal['Account__c']
        email_validation = services.user_email_validation(proposal['Account__c'], email)
        if email_validation:
            request.session['contact_account_id'] = email_validation['contact_account_id']
            request.session['contact_id'] = email_validation['contact_id']
            request.session['is_emailvalid'] = True
            request.session['document'] = services.get_pdf_for_review(proposal_id)
            is_contactcreated = email_validation['is_contactcreated']
            services.additional_confirmation(request, is_contactcreated, proposal, proposal_id)
            print(request.session['sf_session_id'])
            return redirect('proposal', proposal_id)
        else:
            client_ip = request.META['HTTP_X_REAL_IP']
            # client_ip = request.META['REMOTE_ADDR']
            Session.objects.create(
                proposal_id=proposal_id,
                email=request.session['email'],
                message='Trying to access Proposal with a non-valid Email.',
                client_ip=client_ip,
                client_geolocation=services.get_geolocation(client_ip),
                device=services.get_user_device(request)
            )
            raise Http404('email')


class ProposalView(View):
    def get(self, request, proposal_id) -> HttpResponse:
        try:
            services.additional_email_verification(request, proposal_id)
        except KeyError:
            return redirect('confirmation', proposal_id)
        sections = Section.objects.filter(is_active=True).all()
        proposal = request.session['proposal']
        request.session['proposal_name'] = proposal['Name']
        request.session['proposal_account_id'] = proposal['Account__c']
        if proposal:
            if not proposal['Published__c']:
                raise Http404('published')
            request.session['proposal_id'] = proposal_id
            request.session['is_proposalexist'] = proposal['Published__c']
            document = request.session['document']
            welcome_message = proposal['Welcome_message__c']
            creator = services.get_proposals_creator(proposal['Account__c'])
            client_name = creator['client_name']
            img = services.get_creator_img(creator['MediumPhotoUrl'])
            creator_name = creator['Name']
            return render(request, 'proposal.html', {'proposal_id': proposal_id,
                                                     'sections': sections,
                                                     'message': welcome_message,
                                                     'creator_name': creator_name,
                                                     'img': img,
                                                     'client_name': client_name,
                                                     'document': document
                                                     })
        else:
            raise Http404()


class ProposalPDFView(View):
    def get(self, request, proposal_id) -> HttpResponse:
        try:
            services.additional_email_verification(request, proposal_id)
        except KeyError:
            raise Http404('email')
        document = request.session['document']
        document_link = document['document_link']
        document_title = document['title']
        return render(request, 'pdf.html', {'proposal_id': proposal_id,
                                            'document': document_link,
                                            'document_title': document_title
                                            })

    def post(self, request, proposal_id):
        if request.POST['url'] == request.META['HTTP_REFERER']:
            document = request.session['document']
            file_name = document['file_name']
            os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
        return HttpResponse({'ok': True})


class Viewer(View):
    @xframe_options_exempt
    def get(self, request):
        try:
            proposal_id = request.session['proposal_id']
        except KeyError:
            return HttpResponse('Session time expired. Please reopen this page.')
        document = request.session['document']
        return render(request, 'viewer.html', {'document_body': document['document_base64'],
                                               'document_name': document['file_name']})


class EventsView(View):
    def post(self, request, proposal_id):
        try:
            time_spent = request.POST['time_spent']
        except KeyError:
            time_spent = None
        print(time_spent)
        try:
            message = request.POST['message']
        except KeyError:
            message = None
        if request.session['email'] == settings.TRUSTED_EMAIL:
            request.session['contact_id'] = None
            request.session['contact_account_id'] = None
        request.session['event_type'] = request.POST['event_type']
        request.session['event_name'] = request.POST['event_name']
        services.create_event_record(
            session_id=request.session['session_id'],
            event_type=request.POST['event_type'],
            event_name=request.POST['event_name'],
            time_spent=time_spent,
            message=message,
            sf_session_id=request.session['sf_session_id'],
            proposal_account_id=request.session['proposal_account_id'],
            contact_id=request.session['contact_id'],
            email=request.session['email'],
            contact_account_id=request.session['contact_account_id'],
            proposal_name=request.session['proposal_name']
        )
        return HttpResponse({'Success': True})
