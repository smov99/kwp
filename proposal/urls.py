from django.urls import path
from proposal import views

urlpatterns = [
    path('', views.ConfirmationView.as_view(), name='confirmation'),
    path('proposal/', views.ProposalView.as_view(), name='proposal'),
    path('proposal/pdf/', views.ProposalPDFView.as_view(), name='pdf'),
]
