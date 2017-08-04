# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.conf.urls import url
from Test.views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
)

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='list'),
    url(r'^create/$', ArticleCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', ArticleUpdateView.as_view(), name='detail'),
    #url(r'^(?P<slug>[\w-]+)/edit/$', ArticleUpdateView.as_view(), name='edit'),
]
