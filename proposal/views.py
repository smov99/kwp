import os

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404

from kwp import settings
from faq.models import Section
from .models import Session, SessionEvent
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
        email = request.POST['email'].lower()
        request.session['email'] = email
        proposal = request.session['proposal']
        if email == settings.TRUSTED_EMAIL:
            services.additional_trusted_email_confirmation(request, proposal_id)
            request.session['is_emailvalid'] = True
            SessionEvent.objects.create(
                session_id_id=request.session.get('session_id'),
                event_type='Login',
                event_name='Auth via backdoor email',
                message=None
            )
            return redirect('proposal', proposal_id)
        request.session['proposal_name'] = proposal['Name']
        request.session['proposal_account_id'] = proposal['Account__c']
        email_validation = services.user_email_validation(proposal['Account__c'], email)
        if email_validation:
            request.session['contact_account_id'] = email_validation['contact_account_id']
            request.session['contact_id'] = email_validation['contact_id']
            request.session['is_emailvalid'] = True
            is_contactcreated = email_validation['is_contactcreated']
            services.additional_confirmation(request, is_contactcreated, proposal, proposal_id)
            if not is_contactcreated:
                event_name = 'Existing contact'
            if is_contactcreated:
                event_name = 'Contact was created'
            services.create_event_record(
                session_id=request.session['session_id'],
                event_type='Login',
                event_name=event_name,
                sf_session_id=request.session.get('sf_session_id'),
                contact_id=request.session['contact_id'],
                email=request.session['email'],
                contact_account_id=request.session['contact_account_id'],
                proposal_name=request.session['proposal_name']
            )
            return redirect('proposal', proposal_id)
        else:
            # client_ip = request.META['HTTP_X_REAL_IP']
            # client_ip = request.META['REMOTE_ADDR']
            client_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
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
            document = services.get_pdf_for_review(proposal_id, request)
            request.session['document'] = document
            welcome_message = proposal['Welcome_message__c']
            creator = services.get_proposals_creator(proposal['Account__c'], request)
            client_name = creator['client_name']
            img = services.get_creator_img(creator['MediumPhotoUrl'], request)
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

    def post(self, request, proposal_id):
        if request.POST['url'] == request.META['HTTP_REFERER']:
            document = request.session['document']
            file_name = document['file_name']
            os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
        return HttpResponse({'ok': True})


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


class Viewer(View):
    @xframe_options_exempt
    def get(self, request):
        try:
            proposal_id = request.session['proposal_id']
        except KeyError:
            raise Http404()
        return render(request, 'viewer.html')


class EventsView(View):
    def post(self, request):
        try:
            time_spent = float(request.POST['time_spent'])
        except:
            time_spent = None
        print(request.POST)
        message = request.POST.get('message')
        if request.session['email'] == settings.TRUSTED_EMAIL:
            request.session['contact_id'] = None
            request.session['contact_account_id'] = None
        request.session['event_type'] = request.POST['event_type']
        request.session['event_name'] = request.POST['event_name']
        sf_session = request.session.get('sf_session_id')
        services.create_event_record(
            session_id=request.session['session_id'],
            event_type=request.POST['event_type'],
            event_name=request.POST['event_name'],
            time_spent=time_spent,
            message=message,
            sf_session_id=sf_session,
            contact_id=request.session['contact_id'],
            email=request.session['email'],
            contact_account_id=request.session['contact_account_id'],
            proposal_name=request.session['proposal_name'],
            request=request
        )
        return HttpResponse({'Success': True})
