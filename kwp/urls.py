"""simple_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from kwp import settings
from proposal import views

urlpatterns = [
    path('viewer', views.Viewer.as_view(), name='viewer'),
    path('update_sections/', include('faq.urls')),
    path('api/v1/', include('api.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('events/', views.EventsView.as_view(), name='events'),
]

urlpatterns += i18n_patterns(
    path('kwp/', admin.site.urls, name='admin-root'),
    path('', include('proposal.urls')),
    prefix_default_language=False,
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
