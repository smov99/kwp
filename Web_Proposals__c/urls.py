from django.urls import path
import Web_Proposals__c.views as views

urlpatterns = [
    path('', views.ConfirmationView.as_view(), name='confirmation'),
    path('proposal/', views.ProposalView.as_view(), name='proposal'),
]
