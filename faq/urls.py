from django.urls import path
from .views import UpdateSectionsView

urlpatterns = [
    path('', UpdateSectionsView.as_view(), name='update_sections'),
]
