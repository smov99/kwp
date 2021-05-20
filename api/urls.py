from django.urls import path

import api.views as views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('session-list/', views.SessionList.as_view(), name=views.SessionList.name),
    path('session-event-list', views.SessionEventList.as_view(), name=views.SessionEventList.name),
    path('session-detail/<int:pk>', views.SessionDetail.as_view(), name=views.SessionDetail.name),
    path('session-event-detail/<int:pk>', views.SessionEventDetail.as_view(), name=views.SessionEventDetail.name),
]
