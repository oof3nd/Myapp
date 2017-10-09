# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Test, Category
from django.forms import CheckboxSelectMultiple, NumberInput, TextInput


class TestForm(forms.ModelForm):
    # Фильтрация предложенных для выбора категорий
    def __init__(self,user=None,*args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(confirmed=True)

    new_category = forms.CharField(
        label=(u'Можете указать новую категорию'),
        required=False,
        help_text=(u'Учтите, что новая категория не будет использована, пока не будет подтверждена администратором или модератором'),
        widget=TextInput(attrs={'class': 'form-control', 'maxlength': 80,
            'title': 'Допускается использовать строчные и заглавные буквы, цифры, дефис и /',
            'placeholder': 'Допускается использовать строчные и заглавные буквы, цифры, дефис и /',
            'pattern': '[ a-zA-Zа-яёА-ЯЁ0-9 -/]+'}),
        error_messages={'unique': "Такая категория уже существует, выберите ее из предложенных."}
    )

    new_tags = forms.CharField(
        label=(u'Если требуется, укажите через запятую новые теги'),
        required=False,
        widget=TextInput(attrs={'maxlength': 250, 'class': 'form-control',
                                'title': 'Допускается использовать строчные и заглавные буквы, цифры, запятые, дефис и /',
                                'placeholder': 'Допускается использовать строчные и заглавные буквы, цифры, запятые, дефис и /',
                                'pattern': '[a-zA-Zа-яёА-ЯЁ0-9 -/,]+'}),
        error_messages={'unique': "Такой тег уже существует, выберите его из предложенных."}
    )

    publish_after_adding = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=(u'Опубликовать тест сразу после отправки (загрузки) либо редактирования теста'),
        required=False
    )

    class Meta:
        model = Test
        fields = ('category', 'result_scale', 'tags', 'name',
                  'description', 'controlling', 'time_restricting', 'anonymous_loader', 'show_answers', 'single_passing', 'only_registered_can_pass')
        widgets = {
            'tags': CheckboxSelectMultiple,
            'time_restricting': NumberInput(attrs={'min': 1, 'placeholder': 'Не менее 1 минуты', 'class': 'form-control'}),
            'name': TextInput(attrs={'maxlength': 200, 'class': 'form-control',
                                     'title': 'Первая буква названия будет преобразована в заглавную, остальные — в строчные. Допускается использовать: буквы, цифры, пробелы, запятые, -/«»():;',
                                     'placeholder': 'Допускается использовать: буквы, цифры, пробелы, запятые, -/«»():;',
                                     'pattern': '[a-zA-Zа-яёА-Я0-9 -/,«»();:]*'}),
        }
        error_messages = {
            'name': {
                'unique': "Тест с таким именем уже присутствует в системе. Пожалуйста, придумайте другое название.",
            }
        }


