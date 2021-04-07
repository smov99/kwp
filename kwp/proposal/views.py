from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View

from simple_salesforce import Salesforce
from kwp import settings


class ConfirmationView(View):
    def get(self, request: HttpRequest, proposalid) -> HttpResponse:
        return render(request, 'confirmation.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        pass


class ProposalView(View):
    pass


class ProposalPDFView(View):
    pass
