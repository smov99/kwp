from kwp import settings
from proposal.services import sf_api_call
import re


def get_sections():
    """Request for getting sections info from Salesforce API.

    :return: Sections info normalized via 'normalize_sections' func.
    """
    query = "SELECT Category_order__c, English_label__c, Spanish_label__c, FAQ_Category__c FROM Django_FAQ_Setting__c WHERE IsDeleted = false"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records']
    sections = normalize_sections(response)
    return sections


def normalize_sections(sections_response):
    """Normalizing sections response.

    :param sections_response:  Response from 'get_sections' request.

    :return: Normalized sections response.
    """
    sections = {}
    for section in sections_response:
        sections[section['FAQ_Category__c']] = {
            'order': section['Category_order__c'],
            'spanish_label': section['Spanish_label__c'],
            'english_label': section['English_label__c'],
        }
    return sections


def get_articles():
    """Request for getting articles info from Salesforce API.

    :return: Articles info normalized via 'normalize_articles' func.
    """
    query = "SELECT KnowledgeArticleId, Django_Order__c, Django_Category__c, Language, Question__c, Answer__c FROM Knowledge__kav where IsDeleted = false ORDER BY  Django_Order__c, Language ASC"
    response = sf_api_call(f'/services/data/{settings.SF_API_VERSION}/query/', {'q': query})['records']
    articles = normalize_articles(response)
    return articles


def normalize_articles(articles_response):
    """Normalize articles response.

    :param articles_response: Response from 'get_articles' request.

    :return: Normalized articles response.
    """
    articles = {}
    for article in articles_response:
        if article['Django_Category__c']:
            question = re.sub('<[^>]*>', '', article['Question__c'])
            answer = re.sub('<[^>]*>', '', article['Answer__c'])
            guid = article['KnowledgeArticleId']
            category = article['Django_Category__c']
            order = article['Django_Order__c']
            language = article['Language']
            try:
                article_category = articles[category]
            except KeyError:
                article_category = articles[category] = {}
            try:
                article_order = article_category[order]
            except KeyError:
                article_order = articles[category][order] = {}
            article_order[language] = {
                'guid': guid,
                'question': question,
                'answer': answer
            }
    return articles
