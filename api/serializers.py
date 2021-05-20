from rest_framework import serializers
from django.contrib.auth import get_user_model

from proposal import models as models

User = get_user_model()


class SessionEventSerializer(serializers.HyperlinkedModelSerializer):
    session_id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    class Meta:
        model = models.SessionEvent
        fields = (
            'url',
            'session_id',
            'id',
            'created',
            'event_type',
            'event_name',
            'message'
        )


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    events = SessionEventSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Session
        fields = (
            'url',
            'id',
            'created',
            'proposal_id',
            'proposal_exists',
            'email',
            'email_valid',
            'account_id',
            'contact_id',
            'contact_created',
            'message',
            'client_ip',
            'client_geolocation',
            'device',
            'events'
        )
