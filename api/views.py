from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import *


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'faq-info': reverse(FaqInfo.name, request=request),
            'sessions-info': reverse(SessionsInfo.name, request=request),
        })
