from django.db import transaction
import re

from kwp import settings
from proposal.services import sf_api_call
from .models import Section, Article


def update_attr(queryset, value):
    """ Updates model instance attributes and saves the instance.

    :param queryset: Any Model instance.
    :param value: Attributes value.
    """
    with transaction.atomic():
        for obj in queryset:
            obj.is_active = value
            obj.save()


def get_sections():
    """Request for getting sections info from Salesforce API.

    :return: Sections info normalized via 'normalize_sections' func.
    """
    query = "SELECT Id, Category_order__c, English_label__c, Spanish_label__c, FAQ_Category__c FROM Django_FAQ_Setting__c WHERE IsDeleted = false"
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
            'guid': section['Id']
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
                article_order = article_category[order] = {}
            article_order[language] = {
                'guid': guid,
                'question': question,
                'answer': answer
            }
    return articles


def create_sections_and_articles(section_return, article_return):
    """Creating section and article objects in db.

    :param section_return: Response from 'get_sections' func.
    :param article_return: Response from 'get_articles' func.
    """
    for section in section_return:
        try:
            section_articles = article_return[section]
        except KeyError:
            section_articles = {}
        order = section_return[section]['order']
        label = section
        guid = section_return[section]['guid']
        label_es = section_return[section]['spanish_label']
        label_en = section_return[section]['english_label']
        if Section.objects.filter(guid=guid, is_active=False).exists():
            Section.objects.filter(is_active=False).get(guid=guid).delete()
        Section.objects.get_or_create(
            order=order,
            guid=guid,
            is_active=True,
            label=label,
            label_en=label_en,
            label_es=label_es
        )
        if section_articles:
            for article in section_articles:
                this_article = section_articles[article]
                order = article
                guid = this_article['en_US']['guid']
                question = this_article['en_US']['question']
                answer = this_article['en_US']['answer']
                question_es = this_article['es']['question']
                question_en = this_article['en_US']['question']
                answer_es = this_article['es']['answer']
                answer_en = this_article['en_US']['answer']
                section_ = Section.objects.filter(is_active=True).get(label_en=label)
                if Article.objects.filter(guid=guid, is_active=False).exists():
                    Article.objects.filter(is_active=False).get(guid=guid).delete()
                Article.objects.get_or_create(
                    order=order,
                    guid=guid,
                    is_active=True,
                    section=section_,
                    question=question,
                    answer=answer,
                    question_en=question_en,
                    question_es=question_es,
                    answer_en=answer_en,
                    answer_es=answer_es
                )
    return True
