# -*- coding: UTF-8 -*-
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DeleteView
# Create your views here.

User = get_user_model()

class ProfileDetailView(DeleteView):
    template_name = 'profiles/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username,is_active=True)