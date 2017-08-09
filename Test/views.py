# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import  HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import  View
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView,DetailView,CreateView,UpdateView
from .forms import ArticleCreateForm,ArticleMetaCreateForm
from .models import Article
from django.contrib.auth.models import User

#Important
class ArticleListView(LoginRequiredMixin, ListView):

    model = Article
    # def get_queryset(self):
    #
    #     return Article.objects.filter(owner=self.request.user)
    #     return Article.objects.all()

    def get_queryset(self):
    # Fetch the queryset from the parent's get_queryset
        queryset = super(ArticleListView, self).get_queryset()
    # Get the q GET parameter
        q = self.request.GET.get('q')
        if q:
    # return a filtered queryset
            return queryset.filter(title__icontains=q)
    # No q is specified so we return queryset
        return  Article.objects.filter(owner=self.request.user)


# замена pk на id для ссылки
class ArticleDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Article.objects.filter(owner=self.request.user)

    # def get_object(self, queryset=None):
    #     article_id =  self.kwargs.get('article_id')
    #     obj = get_object_or_404(Article,id=article_id) #pk=article_id
    #     return obj

class ArticleCreateView(LoginRequiredMixin, CreateView):
    form_class = ArticleMetaCreateForm
    login_url = '/login/'
    template_name = 'Test/form.html' # may use without 'Test/'          (templates)
    #success_url = '/article/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(ArticleCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView,self).get_context_data(**kwargs)
        context['title'] = _('Add news')
        return context

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ArticleMetaCreateForm
    login_url = '/login/'
    template_name = 'Test/detail_update.html' # may use without 'Test/'          (templates)
    #success_url = '/article/'

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView,self).get_context_data(**kwargs)
        name = self.get_object().title
        context['title'] = _('Update new')+f' {name}'
        return context

    def get_queryset(self):
        return Article.objects.filter(owner=self.request.user)