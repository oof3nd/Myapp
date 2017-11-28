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
    LOTCreateView,
    LOTUpdateView,
    CQCreateView,
    CQOCreateView,
    Testing,
)

# urls ответов
optionspatterns = [
    url(r'^create_option/$', CQOCreateView.as_view(), name='createQCO'),
]

# urls вопросов
questionspatterns = [
    url(r'^create_question/$', QOTCreateView.as_view(), name='createQ'),
    url(r'^create_question/(?P<question_pk>\d+)/closed$', CQCreateView.as_view(), name='createQC'),
    url(r'^(?P<question_pk>\d+)/option/', include(optionspatterns, namespace='options')),
    url(r'^(?P<question_pk>\d+)/$', Testing.as_view(), name='testing'),
]

# urls уровней
levelspatterns = [
    url(r'^create_level/$', LOTCreateView.as_view(), name='createL'),
    url(r'^edit/(?P<level_pk>\d+)/$', LOTUpdateView.as_view(), name='editL'),
    url(r'^(?P<level_pk>\d+)/question/', include(questionspatterns, namespace='questions')),
    url(r'^(?P<level_pk>\d+)/', include(questionspatterns, namespace='insidequestion')),
]

# urls теста
insidetestpatterns = [
    url(r'^$',TestDetailAllView.as_view(), name='detail'),
    url(r'^testing/',include(levelspatterns,namespace='insidelevel')),
    #url(r'^testing/$', ),
]

urlpatterns = [
    url(r'^$', TestListAllView.as_view(), name='list'),
    url(r'^create/$', TestCreateView.as_view(), name='create'),
    url(r'^mytests/$', TestListView.as_view(), name='mylist'),
    url(r'^mytests/(?P<pk>\d+)/edit/$', TestUpdateView.as_view(), name='edit'),
    url(r'^mytests/(?P<pk>\d+)/$', TestDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/', include(insidetestpatterns, namespace='insidetest')),
    url(r'^mytests/(?P<pk>\d+)/level/', include(levelspatterns,namespace='levels')),
]

