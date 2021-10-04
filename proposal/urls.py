from django.urls import path
from proposal import views

urlpatterns = [
    path('<slug:proposal_id>/', views.ConfirmationView.as_view(), name='confirmation'),
    path('<slug:proposal_id>/proposal/', views.ProposalView.as_view(), name='proposal'),
    path('<slug:proposal_id>/proposal/pdf/<slug:document_id>', views.ProposalPDFView.as_view(), name='pdf'),
]
