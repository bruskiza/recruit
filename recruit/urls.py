"""recruit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from interviews import views as interviewsViews
from jobs import views as jobsViews
from candidates import views as candidatesViews
from recruiters import views as recruitersViews
from dashboards import views as dashboardViews
from django.contrib.auth.models import User

urlpatterns = [
    re_path(r'^$', dashboardViews.dashboards, name='dashboards'),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^jobs/$', jobsViews.view_jobs, name='jobs'),
    re_path(r'^jobs/(?P<job_id>\d+)/$', jobsViews.view_job_details, name='job_details'),
    re_path(r'^candidates/apply/$', candidatesViews.apply, name='candidate_apply'),
    re_path(r'^candidates/apply/success/$', candidatesViews.apply_success, name='candidate_apply_success'),    
    re_path(r'^recruiters/', recruitersViews.view_recruiters, name='recruiters'),
    # re_path(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}), 
    re_path(r'^available/(?P<bu_id>\d+)/$', interviewsViews.available, name='available'),
    re_path(r'^availability/(?P<bu_id>\d+)/$', interviewsViews.availability, name='availability'),
    re_path(r'^interviews/', interviewsViews.interview_requests, name='interviews')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)