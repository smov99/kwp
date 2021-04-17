from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from kwp import settings


class ConfirmationView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        return render(request, 'confirmation.html', {'proposal_id': proposal_id})

    def post(self, request: HttpRequest, proposal_id) -> HttpResponse:
        return redirect('proposal', proposal_id)


class ProposalView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        return render(request, 'proposal.html', {'proposal_id': proposal_id})


class ProposalPDFView(View):
    def get(self, request: HttpRequest, proposal_id) -> HttpResponse:
        return render(request, 'pdf.html', {'proposal_id': proposal_id})


class EventsView(View):
    def post(self, request, proposal_id):
        print(request.POST['event_type'])
        print(request.POST['event_name'])
        print(proposal_id)
        pass
