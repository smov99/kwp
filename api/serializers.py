from rest_framework import serializers
from django.contrib.auth import get_user_model

from faq import models as faq_models
from proposal import models as proposal_models

User = get_user_model()


class FaqInfo():
    pass


class SessionsInfo():
    pass
