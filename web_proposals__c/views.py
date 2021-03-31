from django.shortcuts import render
from django.views.generic import TemplateView


class ConfirmationView(TemplateView):
    template_name = 'confirmation.html'


class ProposalView(TemplateView):
    template_name = 'proposal.html'
