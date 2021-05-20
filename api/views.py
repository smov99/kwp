from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from proposal.models import Session, SessionEvent
from .serializers import *


class SessionList(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    name = 'session-list'
    ordering_fields = ('-created',)


class SessionDetail(generics.RetrieveAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    name = 'session-detail'


class SessionEventList(generics.ListAPIView):
    queryset = SessionEvent.objects.all()
    serializer_class = SessionEventSerializer
    name = 'sessionevent-list'
    ordering_fields = ('-created',)


class SessionEventDetail(generics.RetrieveAPIView):
    queryset = SessionEvent.objects.all()
    serializer_class = SessionEventSerializer
    name = 'sessionevent-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'sessions-list': reverse(SessionList.name, request=request),
            'session-events-list': reverse(SessionEventList.name, request=request),
        })
