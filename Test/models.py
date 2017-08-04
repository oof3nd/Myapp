# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import django.utils.timezone
from django.utils.timezone import now,pytz
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .untils import unique_slug_generator
from .validators import validate_important

class Article(models.Model):
    title           = models.CharField('Заголовок',max_length=200)
    important       = models.CharField(max_length=200, null=True,blank=True, validators=[validate_important])
    text            = models.TextField()
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)
    #my_date_field  = models.DateField(auto_now=False,auto_now_add=False)
    slug            = models.SlugField(unique=True,null=True,blank=True)
    owner           = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self): #get_absolute_url
        # return f"/article/{self.slug}"
        return  reverse('article:detail', kwargs={'slug': self.slug})



def rl_pre_save_reciiver(sender,instance,*args,**kwargs):
    instance.important = instance.important.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# создает текстовую ссылку
# def rl_post_save_reciiver(sender,instance,created,*args,**kwargs):
#     print('Сохранено')
#     print(instance.timestamp)
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#         instance.save()

pre_save.connect(rl_pre_save_reciiver, sender=Article)

# post_save.connect(rl_post_save_reciiver, sender=Article)