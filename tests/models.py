# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.utils.timezone import now,pytz
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Test(models.Model):
    user = models.ForeignKey(User, related_name='tests', on_delete=models.CASCADE, verbose_name='Пользователь, загрузивший тест', null=True, blank=True)
    category = models.ForeignKey('tests.Category', related_name='tests', on_delete=models.CASCADE, verbose_name='Категория теста', null=True, blank=True)
    result_scale = models.ForeignKey('tests.ResultScale', related_name='tests', on_delete=models.CASCADE, verbose_name='Оценочная шкала теста')
    # Т.е. тесту может быть назначено много тегов, а теги
    # могут быть назначены для  разных тестов
    # По документации Django, предпочтительно использовать имя поля во множ. числе
    tags = models.ManyToManyField('tests.Tag', related_name='tests', verbose_name='Тег или теги теста', blank=True)
    anonymous_loader = models.BooleanField('Анонимный тест. На странице теста не будет указан пользователь, который загрузил тест.', default=False, blank=True)
    name = models.CharField('Наименование теста', max_length=200, null=False, blank=False, unique=True)
    description = models.TextField('Описание теста', default='Описание теста отсутствует...')
    controlling = models.BooleanField('Использование контроля прохождения теста', default=False)
    time_restricting = models.IntegerField('Ограничение времени прохождения теста в минутах', null=True, blank=True)
    rating = models.IntegerField('Рейтинг теста', default=0, editable=False)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    published_date = models.DateTimeField('Дата публикации', auto_now=True)
    ready_for_passing = models.BooleanField('Готовность теста для прохождения другими пользователями', default=False, blank=True, editable=False)
    show_answers = models.BooleanField('Показывать ответы после прохождения', default=True, blank=True)
    single_passing = models.BooleanField('Допускается пройти тест только один раз', default=False, blank=True)
    only_registered_can_pass = models.BooleanField('Только зарегистрированные и авторизованные пользователи могут проходить тест', default=False, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tests:edit', kwargs={'pk': self.pk})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.published_date = None
        self.save()

    def make_ready_for_passing(self):
        self.ready_for_passing = True
        self.save()

    def review_positively(self):
        self.rating = f"{rating + 1}"
        self.save()

    def review_negatively(self):
        self.rating = f"{rating- 1}"
        self.save()

    class Meta:
        ordering = ['name']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

class Category(models.Model):
    name = models.CharField('Наименование категории', max_length=80, blank=False, unique=True)
    confirmed = models.BooleanField('Категория подтверждена', default=False)

    def confirm(self):
        self.confirmed = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        permissions = (
            ('confirm_category', 'Can confirm_category'),
        )

class ResultScale(models.Model):
    name = models.CharField('Наименование шкалы', max_length=70, blank=False, unique=True)
    scale_divisions_amount = models.IntegerField('Количество возможных оценок', default=0)

    divisions_layout = models.CharField(
        'Разметка делений шкалы -- процентные доли каждого деления через запятую',
        max_length=80, blank=False,
        help_text='Следует указать [количество возможных баллов/оценок - 1] элементов. Например, для 2-бальной шкалы (зачтено, незачтено) разметка делений может быть <q>50</q>')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Оценочная шкала'
        verbose_name_plural = 'Оценочные шкалы'

class Tag(models.Model):
    name = models.CharField('Наименование тега', max_length=40, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class TestRate(models.Model):
    test = models.ForeignKey('tests.Test',
                             related_name='rates',
                             on_delete=models.CASCADE,
                             verbose_name='Тест, к которому относится данная пользовательская оценка (рейтинг)',
                             null=False, blank=False)
    reviewer = models.ForeignKey(User, related_name='rates',
                                 verbose_name='Пользователь, к которому относится данная пользовательская оценка (рейтинг)',
                                 null=False, blank=False)
    like = models.BooleanField('Тест понравился? Если True — +1 к рейтингу, иначе — -1 к рейтингу',
                               null=False, blank=False)

    def __str__(self):
        if self.like:
            rate = '+1'
        else:
            rate = '-1'
        return rate + ' от пользователя ' + self.reviewer.username

    class Meta:
        verbose_name = 'Оценка тестов'
        verbose_name_plural = 'Оценки тестов'

class Result(models.Model):
    owner = models.ForeignKey(User, related_name='results', on_delete=models.CASCADE,
        verbose_name='Пользователь, к которому относится результат прохождения', null=False, blank=False)
    test = models.ForeignKey('tests.Test', related_name='results',
            blank=False, on_delete=models.CASCADE, verbose_name='Тест, к которому относится вопрос')
    grade_based_on_scale = models.IntegerField('Оценка по шкале', null=False, blank=False)
    passing_date = models.DateTimeField('Дата прохождения теста', default=timezone.now, editable=False)
    # Процент неправильных можно посчитать — [100-correct_answers_percentage], поэтому его можно не хранить
    correct_answers_percentage = models.IntegerField('Процент правильных ответов в целочисленном формате', null=False, blank=False)

    def __str__(self):
        return self.owner.username + ' прошел тест ' + self.test.name + ' с оценкой ' + str(self.grade_based_on_scale)

    class Meta:
        ordering = ['owner', 'test']
        verbose_name = 'Результат прохождения теста'
        verbose_name_plural = 'Результаты прохождения тестов'