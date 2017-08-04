# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _



def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            '%(value)s is not an even number',
            params={'value': value},
        )

def validate_email(value):
    email = value
    if ".edu" in email:
        raise ValidationError("Нельзя использовать edu")

IMPORTANT = [_('New'),_('Fast')]

def validate_important(value):
    impo = value.capitalize()
    if not value in IMPORTANT and not impo in IMPORTANT:
        raise ValidationError(F"{value}, данной категории новости нет")

