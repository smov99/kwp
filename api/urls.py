from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

import api.views as views
from api.services import schema_view

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('session-list', views.SessionList.as_view(), name=views.SessionList.name),
    path('session-event-list', views.SessionEventList.as_view(), name=views.SessionEventList.name),
    path('session-detail/<int:pk>', views.SessionDetail.as_view(), name=views.SessionDetail.name),
    path('session-event-detail/<int:pk>', views.SessionEventDetail.as_view(), name=views.SessionEventDetail.name),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
]
