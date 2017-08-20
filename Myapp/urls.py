# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import  LoginView

from profiles.views import  ProfileFollowToggle



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^u/', include('profiles.urls', namespace='profiles')),
    url(r'^profile-follow/$',ProfileFollowToggle.as_view(), name='follow'),
    url(r'^$',  TemplateView.as_view(template_name='Test/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='Test/about.html'), name='about'),
    url(r'^contacts/$', TemplateView.as_view(template_name='Test/contacts.html'), name='contacts'),
    url(r'^article/',include('Test.urls', namespace='article')),
    url(r'^items/', include('menus.urls', namespace='menus')),
]
