import os
import re

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404

from kwp import settings
from faq.models import Section
from .models import (
    Session,
    SessionEvent,
    SalesforceCategory
)
import proposal.services as services
from .forms import VerificationForm


class ConfirmationView(View):
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        if re.match('a0P[\w\d]{15}', proposal_id):
            proposal = request.session.get('proposal')
            if proposal:
                if proposal.get('Id') != proposal_id:
                    proposal = services.get_proposal(proposal_id)
            else:
                proposal = services.get_proposal(proposal_id)
            if proposal:
                request.session['proposal'] = proposal
                return render(request, 'confirmation.html', {'proposal_id': proposal_id})
            else:
                email = request.session.get('email')
                services.create_failed_session_record(request, proposal_id, email)
                raise Http404()
        else:
            raise Http404()

    @services.clock
    def post(self, request, proposal_id) -> HttpResponse:
        form = VerificationForm(request.POST)
        if not form.is_valid():
            request.method = 'GET'
            return HttpResponse({'error': True})
        email = request.POST['email'].lower()
        request.session['email'] = email
        proposal = request.session['proposal']
        trusted_emails = services.get_trusted_emails()
        if email in trusted_emails:
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
    @services.clock
    def get(self, request, proposal_id) -> HttpResponse:
        try:
            services.additional_email_verification(request, proposal_id)
        except KeyError:
            return redirect('confirmation', proposal_id)
        sections = Section.objects.filter(is_active=True).all()
        proposal = request.session.get('proposal')
        if proposal:
            request.session['proposal_name'] = proposal['Name']
            request.session['proposal_account_id'] = proposal['Account__c']
            trusted_emails = services.get_trusted_emails()
            if not proposal['Published__c'] and request.session.get('email') not in trusted_emails:
                raise Http404('published')
            dynamic_documents = services.get_dynamic_files_for_review(proposal_id, request)
            proposal_static_resources = services.get_static_resources_to_review(proposal)
            request.session['proposal_id'] = proposal_id
            request.session['is_proposalexist'] = proposal['Published__c']
            request.session['documents'] = dynamic_documents
            welcome_message = proposal['Welcome_message__c']
            proposal_is_expired = proposal['Expired_proposal__c']
            creator = services.get_proposals_creator(proposal['Account__c'], request)
            img = services.get_creator_img(creator['MediumPhotoUrl'], request)
            return render(
                request, 'proposal.html',
                {
                    'proposal_id': proposal_id,
                    'sections': sections,
                    'message': welcome_message,
                    'is_expired': proposal_is_expired,
                    'creator': creator,
                    'img': img,
                    'documents': dynamic_documents,
                    'static_resources': proposal_static_resources,
                    'media_url': settings.MEDIA_URL
                }
            )
        else:
            raise Http404()

    def post(self, request, proposal_id):
        if request.POST['url'] == request.META['HTTP_REFERER']:
            documents = request.session['documents']
            for _, document in documents.items():
                file_name = document['file_name']
                os.remove(os.path.join(settings.MEDIA_ROOT, file_name))
        return HttpResponse({'ok': True})


class ProposalPDFView(View):
    def get(self, request, proposal_id, document_id) -> HttpResponse:
        try:
            services.additional_email_verification(request, proposal_id)
        except KeyError:
            raise Http404('email')
        categories = request.session['categories'] = \
            list(SalesforceCategory.objects.values_list('salesforce_category', flat=True))
        if document_id in categories:
            document = services.get_single_static_document(document_id)
            document_link = os.path.join(
                settings.MEDIA_URL,
                document.document.name
            )
            document_title = document.file_description
        else:
            document = request.session['documents'][document_id]
            services.get_single_dynamic_file(
                document_id,
                document.get('file_name'),
                document.get('document_path'),
                request)
            document_link = document['document_link']
            document_title = document['title']
        return render(request, 'pdf.html', {'proposal_id': proposal_id,
                                            'document': document_link,
                                            'document_title': document_title,
                                            'document_id': document_id
                                            })


class Viewer(View):
    @xframe_options_exempt
    def get(self, request, document_id):
        try:
            proposal_id = request.session['proposal_id']
            if document_id in request.session['categories']:
                document = services.get_single_static_document(document_id)
                document_link = os.path.join(
                    settings.MEDIA_URL,
                    document.document.name
                )
                document_name = document.file_description
            else:
                document = request.session['documents'][document_id]
                services.get_single_dynamic_file(
                    document_id,
                    document.get('file_name'),
                    document.get('document_path'),
                    request
                )
                document_link = document['document_link']
                document_name = document['file_name']
        except KeyError:
            raise Http404()
        return render(request, 'viewer.html', {
            'document_link': document_link,
            'document_name': document_name
        })


class EventsView(View):
    def post(self, request):
        time_spent = request.POST.get('time_spent')
        message = request.POST.get('message')
        document_name = request.POST.get('document_name')
        trusted_emails = services.get_trusted_emails()
        if request.session['email'] in trusted_emails:
            request.session['contact_id'] = None
            request.session['contact_account_id'] = None
        request.session['event_type'] = request.POST['event_type']
        request.session['event_name'] = request.POST['event_name']
        sf_session = request.session.get('sf_session_id')
        if not len(time_spent):
            time_spent = None
        if not len(message):
            message = None
        if not len(document_name):
            document_name = None
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
            request=request,
            document_name=document_name
        )
        return HttpResponse({'Success': True})
