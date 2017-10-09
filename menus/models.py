# -*- coding: UTF-8 -*-
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _


from Test.models import Article

class Item(models.Model):
    # associations
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    article     = models.ForeignKey(Article)
    # item stuff
    name        = models.CharField(max_length=120)
    contents    = models.TextField(help_text=_('Separate by comma'))
    excludes    = models.TextField(blank=True,null=True,help_text=_('Separate by comma'))
    public      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name

    def get_absolute_url(self): #get_absolute_url
        # return f"/article/{self.slug}"
        return reverse('menus:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-updated','-timestamp'] #Item.objects.all()

    def get_contents(self):
        return self.contents.split(',')

    def get_excludes(self):
        return self.excludes.split(',')

