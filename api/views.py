from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from proposal.models import Session, SessionEvent
from .serializers import *


class SessionList(generics.ListAPIView):
    serializer_class = SessionSerializer
    name = 'session-list'
    ordering_fields = ('created',)

    def get_queryset(self):
        queryset = Session.objects.all()
        proposal_id = self.request.query_params.get('proposalid')
        if proposal_id is not None:
            queryset = queryset.filter(proposal_id=proposal_id)
        return queryset


class SessionDetail(generics.RetrieveAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    name = 'session-detail'


class SessionEventList(generics.ListAPIView):
    serializer_class = SessionEventSerializer
    name = 'sessionevent-list'
    ordering_fields = ('created',)

    def get_queryset(self):
        queryset = SessionEvent.objects.all()
        session_id = self.request.query_params.get('sessionid')
        if session_id is not None:
            queryset = queryset.filter(session_id_id=session_id)
        return queryset


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
