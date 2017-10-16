# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url, include
from tests.views import (
    TestListAllView,
    TestDetailAllView,
    TestListView,
    TestDetailView,
    TestCreateView,
    TestUpdateView,
    QOTCreateView,
)

urlpatterns = [
    url(r'^create/$', TestCreateView.as_view(), name='create'),
    url(r'^mytests/(?P<pk>\d+)/', include([
    url(r'^$', TestDetailView.as_view(), name='detail'),
    url(r'^create/$',  QOTCreateView.as_view(), name='createQ')])),
    #url(r'^mytests/(?P<pk>\d+)/create/$', QOTCreateView.as_view(), name='createQ'),
#r'^(?P<username>[\w-]+)
    url(r'^mytests/$', TestListView.as_view(), name='mylist'),
    url(r'^mytests/(?P<pk>\d+)/edit/$', TestUpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/$', TestDetailAllView.as_view(), name='details'),
    url(r'^$', TestListAllView.as_view(), name='list'),
]
