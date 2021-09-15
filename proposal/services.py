import base64
import os
import requests
from datetime import datetime, timedelta
import functools
import time

from user_agents import parse
from ipdata import ipdata

from django.http import Http404
from django.shortcuts import redirect

from kwp import settings
from .models import SessionEvent, Session, ErrorLog


def clock(func):
    def clocked(*args, **kwargs):
        t0 = time.time()

        result = func(*args, **kwargs)

        elapsed = time.time() - t0
        print(elapsed)
        return result

    return clocked


def timed_cache(**timedelta_kwargs):
    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() + update_delta
        # Apply @lru_cache to f with no cache size limit
        f = functools.lru_cache(None)(f)

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)

        return _wrapped

    return _wrapper


def salesforce_login():
    params = {
        'grant_type': 'password',
        'client_id': settings.SF_CONSUMER_KEY,
        'client_secret': settings.SF_CONSUMER_SECRET,
        'username': settings.SF_USER_NAME,
        'password': settings.SF_PASSWORD,
    }
    response = requests.post(settings.SF_LOGIN_URL, params=params)
    return response


def sf_api_call(action, parameters={}, method='get', data={}, request=None):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH, client.
    """
    sf_login = salesforce_login()
    access_token = sf_login.json().get('access_token')
    instance_url = sf_login.json().get('instance_url')
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    doc_headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        if 'profilephoto' in action:
            r = requests.request(method, action, headers=doc_headers, timeout=30)
            if r.status_code < 300:
                return r.content
        elif 'VersionData' in action:
            r = requests.request(method, instance_url + action, headers=doc_headers, timeout=30)
            if r.status_code < 300:
                return r.content
        else:
            r = requests.request(method, instance_url + action, headers=headers, params=parameters, timeout=30)
            return r.json()
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url + action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        raise ValueError('Method should be get or post or patch.')
    if r.status_code < 300:
        if method == 'patch':
            return None
        else:
            return r.json()

    else:
        error_message = 'API error when calling %s : %s' % (r.url, r.content)
        session_id = None
        if request is not None:
            session_id = request.session.get('session_id')
        ErrorLog.objects.create(
            session_id_id=session_id,
            api_call_type=method,
            sf_object=r.url.split('/')[-1],
            sf_error=error_message
        )
        raise Exception(error_message)


def get_geolocation(client_ip):
    """Getting user geolocation.

    :param client_ip: User ip address.
    :return: User geolocation.
    """
    try:
        ipdata_ = ipdata.IPData(settings.IPDATA_TOKEN)
        geolocation = ipdata_.lookup(client_ip, fields=['continent_name', 'country_name', 'city', 'region'])
    except:
        response = None
    else:
        response = ', '.join([v for k, v in geolocation.items() if type(v) == str])
    return response


def get_user_device(request):
    device = parse(request.META['HTTP_USER_AGENT'])
    response = device.os.family + ' ' + '.'.join(map(str, device.os.version))
    if device.device.family != 'Other':
        response += ', ' + device.device.brand + ' ' + device.device.family
    return response


def get_proposal(proposal_id):
    """Getting proposal info.

    :param proposal_id: Proposal Id from url.

    :return: Proposal info
    """
    query = f"SELECT Id,Account__c,Welcome_message__c,Description__c,Published__c,Expired_proposal__c,Show_Case_Study__c,Show_Quick_Start_Guide__c,Show_Brochure__c,Show_Kiwapower_at_a_Glance_video__c,Name FROM Web_Proposals__c where IsDeleted = false and Id = '{proposal_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})
    try:
        error = response[0]['errorCode']
    except KeyError:
        try:
            response = response['records'][0]
        except IndexError:
            response = False
    else:
        response = False
    return response


@timed_cache(seconds=600)
def get_user_email_information(proposal_account_id, request=None):
    """Getting information corresponding to the provided proposal.

    :param request: Request.
    :param proposal_account_id: Account__c value from 'get_proposal' requests response.

    :return: Info relevant to email address.
    """
    query = f"SELECT Authorized_contact__c, Authorized_domain__c, Authorized_email__c FROM Authorized_emails__c where Account__c='{proposal_account_id}' and  isDeleted=false"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query}, request=request)['records']
    return response


def user_email_validation(proposal_account_id, email, request=None):
    """User email validation

    :param request: Request.
    :param proposal_account_id: Account__c value from 'get_proposal' requests response.
    :param email: Provided email address of the user.

    :return: contact_id and contact_account_id contained in dict.
    """
    validated_info = {}
    email_domain = email.split('@')[1]
    email_responses = get_user_email_information(proposal_account_id, request=request)
    for email_response in email_responses:
        if email == email_response['Authorized_email__c']:
            validated_info['contact_id'] = email_response['Authorized_contact__c']
            validated_info['contact_account_id'] = proposal_account_id
            validated_info['is_contactcreated'] = False
            return validated_info
        if email_domain in email_response['Authorized_domain__c'] or \
                email_responses['Authorized_domain__c'] in email_domain:
            domain_response = email_domain_validation(email)
            try:
                valid_email = domain_response[0]['Email']
            except:
                valid_email = False
            if valid_email:
                if valid_email == email:
                    validated_info['contact_id'] = domain_response[0]['Id']
                    validated_info['contact_account_id'] = domain_response[0]['AccountId']
                    validated_info['is_contactcreated'] = False
                    return validated_info
            else:
                validated_info['contact_account_id'] = proposal_account_id
                created_contact_response = create_contact(email, validated_info['contact_account_id'])
                validated_info['contact_id'] = created_contact_response['id']
                validated_info['is_contactcreated'] = True
                return validated_info
    return False


def email_domain_validation(email):
    """Validation of provided email address domain of user.

    :param email: Provided email address of user.

    :return: Response containing info of verified email addresses.
    """
    query = f"SELECT Id,AccountId,Email FROM Contact where Email='{email}' and isDeleted=false"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records']
    return response


@timed_cache(seconds=600)
def get_client_info(proposal_account_id, request=None):
    query = f"Select name, OwnerId from Account where id = '{proposal_account_id}'"
    response = \
        sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query}, request=request)['records'][0]
    return response


@timed_cache(seconds=600)
def get_owner_id(contact_account_id):
    """Getting owner info of new Contact object.

    :param contact_account_id: AccountId from 'email_domain_validation' response.

    :return: Response containing owner info.
    """
    query = f"SELECT OwnerID from Account where Id = '{contact_account_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records'][0]['OwnerId']
    return response


def create_contact(email, contact_account_id):
    """Creating new Contact object.

    :param email: Provided email address of the user.
    :param contact_account_id: AccountId from 'email_domain_validation' response.

    :return: Response containing new users info.
    """
    owner_id = get_owner_id(contact_account_id)
    data = {
        'Email': email,
        'LastName': email.split('@')[0],
        'AccountId': contact_account_id,
        'From_django__c': True,
        'OwnerId': owner_id
    }
    response = sf_api_call(f"/services/data/{settings.SF_API_VERSION}/sobjects/Contact", method='post', data=data)
    return response


@timed_cache(seconds=600)
def get_proposals_creator(proposal_account_id, request=None):
    """Getting proposal author info.

    :param request: Request.
    :param proposal_account_id: Account__c from 'get_proposal's response.

    :return: Author info.
    """
    client = get_client_info(proposal_account_id, request)
    user_id = client['OwnerId']
    query = f"SELECT Name,MediumPhotoUrl,SmallPhotoUrl FROM User where id='{user_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query}, request=request)['records'][0]
    response['client_name'] = client['Name']
    return response


def get_documents_list(proposal_id, request=None):
    """Getting documents list.

    :param request: Request.
    :param proposal_id: Proposal Id from url.

    :return: List of documents
    """
    query = f"SELECT ContentDocumentId FROM ContentDocumentLink where IsDeleted = false and LinkedEntityId = '{proposal_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query}, request=request)['records']
    return response


def get_single_document(content_document_id, request=None):
    """Getting single document.

    :param request: Request.
    :param content_document_id: First match in list of documents from 'get_documents_list's response.

    :return: Document.
    """
    query = f"SELECT Id, ContentSize, CreatedDate, Description, FileExtension, FileType, OwnerId, ParentId, PublishStatus, SharingOption, SharingPrivacy, Title FROM ContentDocument where Id='{content_document_id}' and FileType='PDF' order by CreatedDate DESC"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query}, request=request)
    try:
        response = response['records'][0]
    except:
        response = None
    return response


def get_document_link(content_document_id, request=None):
    """Getting url to file

    :param request: Request.
    :param content_document_id: Id of document.

    :return: Document link.
    """
    query = f"SELECT VersionData FROM ContentVersion WHERE ContentDocumentId='{content_document_id}' and isLatest = true"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query}, request=request)['records'][0][
            'VersionData']
    return response


@timed_cache(seconds=600)
def get_document(url, request=None):
    """Getting needed document.

    :param request: Request.
    :param url: Document link.

    :return: Binary document.
    """
    response = sf_api_call(url, request=request)
    return response


@timed_cache(seconds=600)
def get_creator_img(url, request):
    """Getting creator image.

    :param request: Request.
    :param url: Image link.

    :return: Image in base64 format.
    """
    response = get_document(url, request)
    img64 = base64.b64encode(response).decode()
    return img64


def get_pdf_for_review(proposal_id, request):
    """Getting PDF for review.

    :param request: Request.
    :param proposal_id: Proposal Id from url.

    :return: Document body and title.
    """
    response = {}
    document_list = get_documents_list(proposal_id, request)[0]
    document_id = document_list['ContentDocumentId']
    single_document = get_single_document(document_id, request)
    if single_document:
        response['title'] = ' '.join(single_document['Title'].split('_'))
        document_link = get_document_link(document_id, request)
        bytes_document = get_document(document_link, request)
        file_name = single_document['Title'] + '.pdf'
        document_path = os.path.join(settings.MEDIA_ROOT, file_name)
        try:
            with open(document_path, 'wb') as doc:
                doc.write(bytes_document)
        except FileExistsError:
            pass
        response['document_base64'] = base64.b64encode(bytes_document).decode()
        response['file_name'] = file_name
        response['document_link'] = os.path.join(settings.MEDIA_URL, single_document['Title'] + '.pdf')
    else:
        response = None
    return response


def create_sf_session_record(
        proposal_id,
        proposal_account_id,
        contact_id,
        device,
        ip_address,
        ip_geolocation
):
    """Creating an session record in Salesforce.

    :param ip_geolocation: User geolocation.
    :param ip_address: User ip address.
    :param device: User device.
    :param proposal_id: Proposal Id from url.
    :param proposal_account_id: Account__c value from 'get_proposal' requests response.
    :param contact_id: 'contact_id' from 'user_email_validation' response.

    :return: Created record id.
    """
    data = {
        'Web_Proposal__c': proposal_id,
        'Account__c': proposal_account_id,
        'Contact__c': contact_id,
        'IP_Address__c': ip_address,
        'IP_geolocation__c': ip_geolocation,
        'Device_OS__c': device,
        'Login_date__c': datetime.utcnow().__format__('%Y-%m-%dT%H:%M:%S.%UZ'),
        'OwnerId': settings.SF_USER_ID
    }
    response = sf_api_call(f"/services/data/{settings.SF_API_VERSION}/sobjects/Proposal_engagement_header__c",
                           method='post',
                           data=data)
    return response['id']


def create_sf_event_record(
        sf_session_id,
        event_name,
        event_type,
        message,
        request=None,
        time_spent=None,
        case_id=None
):
    """Creating an session record in Salesforce.

    :param request: Request.
    :param message: Message.
    :param event_type: Event type.
    :param case_id: Case Salesforce record Id.
    :param time_spent: Time spent.
    :param event_name: Event name.
    :param sf_session_id: Session id of Salesforce record.

    """
    if message is not None:
        if len(message) > 150:
            message = message[0:147] + '...'
        event_name = message
    data = {
        'Proposal_engagement_header__c': sf_session_id,
        'Event_date__c': datetime.utcnow().__format__('%Y-%m-%dT%H:%M:%S.%UZ'),
        'Event_type__c': event_type,
        'Time_spent__c': time_spent,
        'Case__c': case_id,
        'Event_description__c': event_name,
    }
    sf_api_call(f"/services/data/{settings.SF_API_VERSION}/sobjects/Proposal_engagement__c",
                method='post',
                data=data,
                request=request
                )


def create_event_record(
        session_id,
        sf_session_id,
        event_type,
        proposal_name,
        contact_account_id,
        event_name,
        email,
        request=None,
        contact_id=None,
        time_spent=None,
        message=None
):
    """Creating an event record in both systems, Salesforce and Django.

    :param request: Request.
    :param sf_session_id: Session id of Salesforce record.
    :param contact_account_id: AccountId from 'email_domain_validation' response.
    :param proposal_name: 'Name' from 'get_proposal' requests response.
    :param email: Provided email address of user.
    :param session_id: Session Id.
    :param event_type: Event type.
    :param contact_id: 'contact_id' from 'user_email_validation' response.
    :param event_name: Event name.
    :param time_spent: Time spent on page(if available).
    :param message: Message(if available).
    """
    if time_spent is not None:
        if 'section' in event_type:
            event_name_ = event_name + ', spent {} seconds'.format(time_spent)
        else:
            event_name_ = event_name.replace('seconds', str(time_spent) + ' seconds')
    elif message is not None:
        if 'Feedback-Form' in event_name:
            event_name_ = 'Question or Feedback, WebProposal {}'.format(
                proposal_name
            )
        else:
            event_name_ = 'Meeting request, WebProposal {}'.format(
                proposal_name
            )
    else:
        event_name_ = event_name
    SessionEvent.objects.create(
        session_id_id=session_id,
        event_type=event_type,
        event_name=event_name_,
        message=message
    )
    if email != settings.TRUSTED_EMAIL:
        case_id = None
        if message is not None:
            if 'Feedback-Form' in event_name:
                subject = 'Question or Feedback, WebProposal {}'.format(
                    proposal_name
                )
            else:
                subject = 'Meeting request, WebProposal {}'.format(
                    proposal_name
                )
            case_id = create_case_record(
                message=message,
                subject=subject,
                contact_account_id=contact_account_id,
                contact_id=contact_id,
                request=request
            )['id']
            event_name = 'Question submitted'
            message = subject + ': ' + message
        create_sf_event_record(
            sf_session_id=sf_session_id,
            event_name=event_name,
            event_type=event_type,
            time_spent=time_spent,
            case_id=case_id,
            message=message,
            request=request
        )


def create_case_record(
        message,
        subject,
        contact_account_id,
        contact_id,
        request=None
):
    """Creating a Case record.

    :param request: Request.
    :param subject: Form name.
    :param message: Message(if available).
    :param contact_account_id: AccountId from 'email_domain_validation' response.
    :param contact_id: 'contact_id' from 'user_email_validation' response.
    """
    owner_id = get_owner_id(contact_account_id)
    data = {
        'Description': message,
        'From_django__c': True,
        'OwnerId': owner_id,
        'ContactId': contact_id,
        'Subject': subject
    }
    response = sf_api_call(f"/services/data/{settings.SF_API_VERSION}/sobjects/Case",
                           method='post',
                           data=data,
                           request=request)
    return response


def additional_email_verification(request, proposal_id):
    client_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    # client_ip = request.META['HTTP_X_REAL_IP']
    # client_ip = request.META['REMOTE_ADDR']
    try:
        email = request.session['email']
        if email == settings.TRUSTED_EMAIL:
            email_validation = True
        else:
            email_validation = user_email_validation(request.session['proposal_account_id'], email, request=request)
    except KeyError:
        email_validation = False
    if not email_validation:
        if request.session['email']:
            Session.objects.create(
                proposal_id=proposal_id,
                email=request.session['email'],
                email_valid=request.session['is_emailvalid'],
                message='Trying to access a Proposal without authorization.',
                client_ip=client_ip,
                client_geolocation=get_geolocation(client_ip),
                device=get_user_device(request)
            )
        else:
            Session.objects.create(
                proposal_id=proposal_id,
                message='Trying to access a Proposal without authorization.',
                client_ip=client_ip,
                client_geolocation=get_geolocation(client_ip),
                device=get_user_device(request)
            )
        return redirect('confirmation', proposal_id)


def additional_confirmation(request, is_contactcreated, proposal, proposal_id):
    # client_ip = request.META['HTTP_X_REAL_IP']
    # client_ip = request.META['REMOTE_ADDR']
    client_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    if client_ip != '127.0.0.1':
        request.session['sf_session_id'] = create_sf_session_record(
            proposal_id,
            request.session['proposal_account_id'],
            request.session['contact_id'],
            get_user_device(request),
            client_ip,
            get_geolocation(client_ip),
        )
        if not proposal['Published__c']:
            Session.objects.create(
                proposal_id=proposal_id,
                email=request.session['email'],
                email_valid=True,
                account_id=proposal['Account__c'],
                client_ip=client_ip,
                client_geolocation=get_geolocation(client_ip),
                proposal_exists=True,
                contact_id=request.session['contact_id'],
                contact_created=is_contactcreated,
                message='Proposal not published',
                device=get_user_device(request)
            )
            raise Http404('published')
        session = Session.objects.create(
            proposal_id=proposal_id,
            email=request.session['email'],
            email_valid=True,
            account_id=proposal['Account__c'],
            client_ip=client_ip,
            client_geolocation=get_geolocation(client_ip),
            proposal_exists=True,
            contact_id=request.session['contact_id'],
            contact_created=is_contactcreated,
            device=get_user_device(request)
        )
        request.session['session_id'] = session.pk


def additional_trusted_email_confirmation(request, proposal_id):
    # client_ip = request.META['HTTP_X_REAL_IP']
    # client_ip = request.META['REMOTE_ADDR']
    client_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    session = Session.objects.create(
        proposal_id=proposal_id,
        email=request.session['email'],
        client_ip=client_ip,
        client_geolocation=get_geolocation(client_ip),
        email_valid=True,
        proposal_exists=True,
        message='Backdoor email access.',
        device=get_user_device(request)
    )
    request.session['session_id'] = session.pk


def create_failed_session_record(request, proposal_id, email):
    # client_ip = request.META['HTTP_X_REAL_IP']
    # client_ip = request.META['REMOTE_ADDR']
    client_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    if client_ip != '127.0.0.1':
        try:
            is_email_valid = request.session['is_emailvalid']
        except KeyError:
            is_email_valid = False
        if email:
            Session.objects.create(
                proposal_id=proposal_id,
                email=email,
                email_valid=is_email_valid,
                message='Trying to access a non-existent Proposal.',
                client_ip=client_ip,
                client_geolocation=get_geolocation(client_ip),
                device=get_user_device(request)
            )
        else:
            Session.objects.create(
                proposal_id=proposal_id,
                message='Trying to access a non-existent Proposal.',
                client_ip=client_ip,
                client_geolocation=get_geolocation(client_ip),
                device=get_user_device(request)
            )
        raise Http404()
