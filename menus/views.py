from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.utils.translation import ugettext_lazy as _
from .forms import ItemForm
from .models import Item

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            object_list = Item.objects.filter(public=True).order_by('-timestamp')
            return render(request, "Test/home.html", {"object_list": object_list})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Item.objects.filter(user_id__in=is_following_user_ids, public=True).order_by("-updated")
        return render(request, "menus/home-feed.html", {'object_list': qs})

class ItemListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'menus/form.html'
    form_class = ItemForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView,self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView,self).get_context_data(**kwargs)
        context['title'] = _('Create Item')
        return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'menus/detail-update.html'
    form_class = ItemForm
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView,self).get_context_data(**kwargs)
        context['title'] = _('Update Item')
        return context

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        return kwargs