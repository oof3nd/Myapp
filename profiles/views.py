# -*- coding: UTF-8 -*-
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin

from Test.models import Article
from menus.models import Item

User = get_user_model()

class ProfileFollowToggle(View):
    def post(self,request,*args,**kwargs):
        print(request.data)
        return redirect("/")


class ProfileDetailView(LoginRequiredMixin, DeleteView):
    template_name = 'profiles/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username,is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user =  context['user'] # self.request.user
        query = self.request.GET.get("q")
        items_exists = Item.objects.filter(user=user).exists()
        qs = Article.objects.filter(owner=user).search(query)
            #qs = Article.objects.search(query)
        if items_exists and qs.exists():
            context['title'] = qs
        return context

