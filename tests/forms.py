# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Test, Category, QuestionOfTest, LevelOfTest,ClosedQuestion, ClosedQuestionOption
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


# Формы для вопросов
class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionOfTest
        fields = ('test', 'question_index_number', 'type_of_question', 'level_of_question')

class ClosedQuestionForm(forms.ModelForm):
    question_index_number = forms.IntegerField(
        label=(u'Можете указать другой порядковый номер вопроса'),
        required=False,
        help_text=(
        u'Порядковый номер другого вопроса изменится соответственно. Если введенный номер больше номера последнего вопроса, то будет считаться, что введен номер последнего.'),
        widget=NumberInput(attrs={'class': 'form-control', 'min': 1}),
    )

    add_options = forms.BooleanField(
        label=(u'Добавить вместе с вариантами ответа'),
        required=False,
        help_text=(
        u'Введите после содержимого самого вопроса (с новой строки, используя enter) слово "ВАРИАНТЫ", затем вновь перенос строки, а затем один или более вариантов ответа, разделяя их переносами строк (используйте enter, кнопка «Источник» должна быть неактивной. Минимум 2 варианта/элемента.')
    )

    class Meta:
        model = ClosedQuestion
        fields = ('question_of_test','question_content',
                  'correct_option_numbers')

        widgets = {
            'correct_option_numbers': TextInput(attrs={'maxlength': 55, 'class': 'form-control',
                                                       'placeholder': 'Допустимы цифры, запятые и пробел в формате 1, 2, 3',
                                                       'pattern': '(?:\d+(?:,\s)?)+'}),
        }

class ClosedQuestionOptionForm(forms.ModelForm):
    add_several = forms.BooleanField(
        label=(u'Добавить несколько'),
        required=False,
        help_text=(u'Для разделения вариантов ответа используйте переносы строк (enter, каждый параграф станет отдельным вариантом). Кнопка «Источник» должна быть при этом неактивной.')
    )

    class Meta:
        model = ClosedQuestionOption
        fields = ('content',
                  'option_number')

        widgets = {
            'option_number': NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

# Форма для уровня тесте
class LevelForm(forms.ModelForm):
    class Meta:
        model = LevelOfTest
        fields = ('test', 'level_index_number', 'name_level', 'solution')
