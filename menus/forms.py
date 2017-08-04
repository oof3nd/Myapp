# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from Test.models import Article
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'article',
            'name',
            'contents',
            'excludes',
            'public',
        ]
        labels = {
            'article': _('Article'),
            'name': _('Name'),
            'contents': _('Contents'),
            'excludes': _('Excludes'),
            'public': _('Public'),
        }

    def __init__(self,user=None,*args, **kwargs):
        #print(kwargs.pop('user'))
        # print(user)
        # print(kwargs)
        super(ItemForm,self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Article.objects.filter(owner=user)