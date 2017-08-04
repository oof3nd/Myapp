# -*- coding: UTF-8 -*-
from .models import Article
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

important_CHOICES = [
    (_('New'), _('New')),
    (_('Fast'), _('Fast')),
]

from .validators import validate_email,validate_important

class ArticleCreateForm(forms.Form):
    title           = forms.CharField()
    important       = forms.CharField(required=False)
    text            = forms.CharField(required=False)
   # user            = forms.CharField()


class ArticleMetaCreateForm(forms.ModelForm):
    #email = forms.EmailField()
    #important = forms.CharField(required=False, validators=[validate_important])
    class Meta:
        model = Article
        fields = ['title','important','text','slug',]
        labels = {
            'title': _('Title'),
            'important': _('Important'),
            'text': _('Text'),
            'slug': _('slug'),
        }
        help_texts = {
            #'important': _('New'),
        }
        widgets = {
            'important': forms.Select(
                #attrs={'placeholder': 'Новая или Срочная'},
                choices=important_CHOICES),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title == "Привет":
            raise forms.ValidationError("Некорректное имя")
        return title

    # def clean(self):
    #     email = self.cleaned_data.get("email")
    #     if ".edu" in email:
    #         raise forms.ValidationError("Нельзя использовать edu")
    #     return email