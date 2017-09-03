# -*- coding: UTF-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import  CreateView,DeleteView,View

from .forms import RegisterForm
from Test.models import Article
from menus.models import Item
from .models import Profile

User = get_user_model()


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = True
                profile.save()
                return redirect("/login")
    return redirect("/login")


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'
    success_message = "Ваш аккаунт создан. Проверьте почту для подтверждения."

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated():
        #     return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/u/{profile_.user.username}/")




class ProfileDetailView(LoginRequiredMixin ,DeleteView):
    template_name = 'profiles/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username,is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user =  context['user'] # self.request.user
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get("q")
        items_exists = Item.objects.filter(user=user).exists()
        qs = Article.objects.filter(owner=user).search(query)
            #qs = Article.objects.search(query)
        if items_exists and qs.exists():
            context['title'] = qs
        return context

