import base64
import requests
from datetime import datetime, timedelta
import functools
from PIL import Image

from kwp import settings


params = {
    'grant_type': 'password',
    'client_id': settings.SF_CONSUMER_KEY,
    'client_secret': settings.SF_CONSUMER_SECRET,
    'username': settings.SF_USER_NAME,
    'password': settings.SF_PASSWORD,
}

r = requests.post(settings.SF_LOGIN_URL, params=params)
access_token = r.json().get('access_token')
instance_url = r.json().get('instance_url')


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


def sf_api_call(action, parameters={}, method='get', data={}):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    """
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
        raise Exception('API error when calling %s : %s' % (r.url, r.content))


@timed_cache(seconds=3600)
def get_proposal(proposal_id):
    """Getting proposal info.

    :param proposal_id: Proposal Id from url.

    :return: Proposal info
    """
    query = f"SELECT Id,Account__c,Welcome_message__c,Description__c,CreatedById,Published__c FROM Web_Proposals__c where IsDeleted = false and Id = '{proposal_id}'"
    try:
        response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records'][0]
    except:
        response = False
    return response


def get_user_email_information(proposal_account_id):
    """Getting information corresponding to the provided proposal.

    :param proposal_account_id: Account__c value from 'get_proposal' requests response.

    :return: Info relevant to email address.
    """
    query = f"SELECT Authorized_contact__c, Authorized_domain__c, Authorized_email__c FROM Authorized_emails__c where Account__c='{proposal_account_id}' and  isDeleted=false"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records'][0]
    return response


def user_email_validation(proposal_account_id, email):
    """User email validation

    :param proposal_account_id: Account__c value from 'get_proposal' requests response.
    :param email: Provided email address of the user.

    :return: contact_id and contact_account_id contained in dict.
    """
    validated_info = {}
    email_domain = email.split('@')[1]
    email_response = get_user_email_information(proposal_account_id)
    if email == email_response['Authorized_email__c']:
        validated_info['contact_id'] = email_response['Authorized_contact__c']
        validated_info['contact_account_id'] = proposal_account_id
    elif email_domain == email_response['Authorized_domain__c']:
        domain_response = email_domain_validation(email)
        if domain_response['Email'] == email:
            validated_info['contact_id'] = domain_response['Id']
            validated_info['contact_account_id'] = domain_response['AccountId']
            return validated_info
        else:
            validated_info['contact_account_id'] = proposal_account_id
            created_contact_response = create_contact(email, validated_info['contact_account_id'])
            validated_info['contact_id'] = created_contact_response['Id']
    return validated_info


def email_domain_validation(email):
    """Validation of provided email address domain of user.

    :param email: Provided email address of user.

    :return: Response containing info of verified email addresses.
    """
    query = f"SELECT Id,AccountId,Email FROM Contact where Email='{email}' and isDeleted=false"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records']
    return response


def get_owner_id(contact_account_id):
    """Getting owner info of new Contact object.

    :param contact_account_id: AccountId from 'email_domain_validation' response.

    :return: Response containing owner info.
    """
    query = f"SELECT OwnerID from Account where Id = '{contact_account_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})
    return response


def create_contact(email, contact_account_id):
    """Creating new Contact object.

    :param email: Provided email address of the user.
    :param contact_account_id: AccountId from 'email_domain_validation' response.

    :return: Response containing new users info.
    """
    data = {
        'Email': email,
        'LastName': email.split('@')[0],
        'AccountId': contact_account_id,
        'From_django__c': True,
        'OwnerId': get_owner_id(contact_account_id)
    }
    response = sf_api_call(f"/services/data/{settings.SF_API_VERSION}/sobjects/Contact", method='post', data=data)['records'][0]
    return response


@timed_cache(seconds=3600)
def get_proposals_creator(user_id):
    """Getting proposal author info.

    :param user_id: CreatedById from 'get_proposal's response.

    :return: Author info.
    """
    query = f"SELECT Name,MediumPhotoUrl,SmallPhotoUrl FROM User where id='{user_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records'][0]
    return response


def get_documents_list(proposal_id):
    """Getting documents list.

    :param proposal_id: Proposal Id from url.

    :return: List of documents
    """
    query = f"SELECT ContentDocumentId FROM ContentDocumentLink where IsDeleted = false and LinkedEntityId = '{proposal_id}'"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records']
    return response


def get_single_document(content_document_id):
    """Getting single document.

    :param content_document_id: First match in list of documents from 'get_documents_list's response.

    :return: Document.
    """
    query = f"SELECT Id, ContentSize, CreatedDate, Description, FileExtension, FileType, OwnerId, ParentId, PublishStatus, SharingOption, SharingPrivacy, Title FROM ContentDocument where Id='{content_document_id}' and FileType='PDF' order by CreatedDate DESC"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})
    return response


def get_document_link(content_document_id):
    """Getting url to file

    :param content_document_id: Id of document.

    :return: Document link.
    """
    query = f"SELECT VersionData FROM ContentVersion WHERE ContentDocumentId='{content_document_id}' and isLatest = true"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records'][0]['VersionData']
    return response


def get_document(url):
    """Getting needed document.

    :param url: Document link.

    :return: Document in base64 format.
    """
    response = sf_api_call(url)
    doc64 = base64.b64encode(response).decode()
    return doc64
