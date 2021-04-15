from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from kwp import settings


class ConfirmationView(View):
    def get(self, request: HttpRequest, proposalid) -> HttpResponse:
        return render(request, 'confirmation.html', {'proposalid': proposalid})

    def post(self, request: HttpRequest, proposalid) -> HttpResponse:
        return redirect('proposal', proposalid)


class ProposalView(View):
    def get(self, request: HttpRequest, proposalid) -> HttpResponse:
        return render(request, 'proposal.html', {'proposalid': proposalid})


class ProposalPDFView(View):
    def get(self, request: HttpRequest, proposalid) -> HttpResponse:
        return render(request, 'pdf.html', {'proposalid': proposalid})


class EventsView(View):
    def post(self, request, proposalid):
        print(request.POST['event_type'])
        print(request.POST['event_name'])
        print(proposalid)
        pass
