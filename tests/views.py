# -*- coding: UTF-8 -*-
import json
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, render_to_response, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView , UpdateView, TemplateView
from django.views.generic.base import ContextMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse,reverse_lazy
from .forms import TestForm,ClosedQuestionForm,ClosedQuestionOptionForm,LevelForm,QuestionForm
from .models import Test, QuestionOfTest,LevelOfTest,ClosedQuestion, ClosedQuestionOption

class TestListAllView(ListView):
    template_name = 'tests/tests.html'
    def get_queryset(self):
        return Test.objects.all().order_by('id')

class TestDetailAllView(DetailView):
    template_name = 'tests/test_form.html'

    def get_queryset(self):
        return Test.objects.filter(user__is_active=True)

    def get_context_data(self,*args,**kwargs):
        context = super(TestDetailAllView, self).get_context_data(**kwargs)
        context['LOT'] = LevelOfTest.objects.filter(test_id=self.object.id).order_by('level_index_number').first()
        LOT = LevelOfTest.objects.filter(test_id=self.object.id).order_by('level_index_number').first()
        context['QOF'] = QuestionOfTest.objects.filter(level_of_question_id=LOT).order_by('question_index_number').first()
        QOF = QuestionOfTest.objects.filter(level_of_question_id=LOT).order_by('question_index_number').first()
        context['CQ'] = ClosedQuestion.objects.get(question_of_test_id=QOF) # выводим только те вопросы, которые входят в этот теста
        CQ = ClosedQuestion.objects.get(question_of_test_id=QOF)
        context['CQO'] =  ClosedQuestionOption.objects.filter(question_id=CQ)
        return context

class TestListView(ListView):
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

class TestDetailView(DetailView):
    def get_context_data(self,*args,**kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        context['QuestionOfTest_object_list'] = QuestionOfTest.objects.all().filter(test_id=self.object.id).order_by('question_index_number')
        context['LevelOfTest_object_list'] = LevelOfTest.objects.all().filter(test_id=self.object.id).order_by('level_index_number')
        context['ClosedQuestion_object_list'] = ClosedQuestion.objects.all().filter(question_of_test__test_id=self.object.id) # выводим только те вопросы, которые входят в этот теста
        context['ClosedQuestionOption_object_list'] = ClosedQuestionOption.objects.all()
        return context
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

#создание
class TestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tests/form.html'
    form_class = TestForm
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(TestCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TestCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание теста'
        return context

    def get_form_kwargs(self):
        kwargs = super(TestCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('tests:mylist')

#изменение теста
class TestUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'tests/form.html'
    form_class = TestForm
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TestUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Обновление теста'
        return context

    def get_form_kwargs(self):
        kwargs = super(TestUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs={'pk': test_pk})

#Ответы
#Создание ответа
class CQOCreateView(LoginRequiredMixin, CreateView):
    model = ClosedQuestionOption
    template_name = 'tests/form.html'
    form_class = ClosedQuestionOptionForm

    def get_initial(self):
        question_id = self.kwargs.get('question_pk')
        closedquestion_id = ClosedQuestion.objects.get(question_of_test_id=question_id)
        option_number = ClosedQuestionOption.objects.filter(question_id=closedquestion_id).count()+1
        initial = {'question': closedquestion_id, 'option_number': option_number, }
        return initial


    def get_queryset(self):
        question_id = self.kwargs.get('question_pk')
        return ClosedQuestion.objects.filter(question_of_test_id=question_id)

    def form_valid(self, form):
        obj = form.save(commit=False)
        return super(CQOCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CQOCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание ответа на вопрос'
        return context

    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs = {'pk': test_pk})

# Редактирование ответа
class CQOUpdateView(LoginRequiredMixin, UpdateView):
    model = ClosedQuestionOption
    pk_url_kwarg = 'level_pk'
    template_name = 'tests/form.html'
    form_class = LevelForm
    def get_queryset(self):
        level_id = self.kwargs.get('level_pk')
        return LevelOfTest.objects.filter(id=level_id)

    def get_context_data(self, **kwargs):
        context = super(CQOUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Обновление уровня'
        return context

    # редирект обратно к тесту
    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs={'pk': test_pk})

#Вопросы
class QOTCreateView(LoginRequiredMixin, CreateView):
    model = QuestionOfTest
    template_name = 'tests/form_next.html'
    form_class = QuestionForm

    def get_initial(self):
        test_id = self.kwargs.get('pk')
        level_id = self.kwargs.get('level_pk')
        question_index_number = QuestionOfTest.objects.filter(level_of_question_id=level_id).count()+1
        initial = {'test': test_id, 'question_index_number':question_index_number, 'level_of_question':level_id }
        return initial

    def get_queryset(self):
        return QuestionOfTest.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        return super(QOTCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QOTCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание вопроса'
        return context

# вопросы закрытого типа
class CQCreateView(LoginRequiredMixin, CreateView):
    model = ClosedQuestion
    template_name = 'tests/form.html'
    pk_url_kwarg = 'question_pk'
    form_class = ClosedQuestionForm

    def get_initial(self):
        question_id = self.kwargs.get('question_pk')
        initial = {'question_of_test':question_id,}
        return initial

    def get_queryset(self):
        return ClosedQuestion.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        return super(CQCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CQCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание вопроса закрытого типа'
        return context

    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs = {'pk': test_pk})

#Уровень
# Создание нового уровня в тесте
class LOTCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tests/form.html'
    model = LevelOfTest
    form_class = LevelForm

    def get_initial(self):
        test_id = self.kwargs.get('pk')
        level_index_number = LevelOfTest.objects.filter(test_id=test_id).count()+1
        initial = {'test': test_id, 'level_index_number': level_index_number, }
        return initial

    def get_queryset(self):
        return LevelOfTest.objects.all()

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        return super(LOTCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LOTCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание уровня'
        return context

    # редирект обратно к тесту
    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs = {'pk': test_pk})

# Редактирование уровня
class LOTUpdateView(LoginRequiredMixin, UpdateView):
    model = LevelOfTest
    pk_url_kwarg = 'level_pk'
    template_name = 'tests/form.html'
    form_class = LevelForm
    def get_queryset(self):
        level_id = self.kwargs.get('level_pk')
        return LevelOfTest.objects.filter(id=level_id)

    def get_context_data(self, **kwargs):
        context = super(LOTUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Обновление уровня'
        return context

    # редирект обратно к тесту
    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs={'pk': test_pk})

# Проверка
class Testing(LoginRequiredMixin, DetailView):
    template_name = 'tests/test_testing.html'

    # def get(self, request, *args, **kwargs):
    #     test_pk = self.kwargs.get('pk')
    #     level_pk = LevelOfTest.objects.filter(test_id=self.kwargs.get('pk')).order_by('level_index_number').first()
    #     question_pk = QuestionOfTest.objects.filter(level_of_question_id=level_pk).order_by('question_index_number').first()
    #     return reverse('tests:insidetest:insidelevel:insidequestion:testing', kwargs={'pk': test_pk,'level_pk':level_pk.id, 'question_pk':question_pk.id })

    def get_queryset(self):
        return LevelOfTest.objects.all()
    def post(self, request, *args, **kwargs):
        data = serializers.serialize('json',Test.objects.filter(id=self.kwargs.get('pk')))
        test_pk = self.kwargs.get('pk')
        level_pk = self.kwargs.get('level_pk')
        question_pk = self.kwargs.get('question_pk')
        last_level = LevelOfTest.objects.filter(test_id=test_pk).order_by('id').last().id
        print(last_level)
        if int(level_pk)<int(last_level):
            level_pk+=1
            print(level_pk)
            return HttpResponseRedirect(reverse('tests:insidetest:insidelevel:insidequestion:testing', kwargs={'level_pk':level_pk, 'pk':test_pk, 'question_pk':question_pk}))
        else:
            return HttpResponse(json.loads(data))

    def get_context_data(self,*args,**kwargs):
        context = super(Testing, self).get_context_data(**kwargs)
        context['LOTS'] = LevelOfTest.objects.filter(test_id=self.kwargs.get('pk')).order_by('level_index_number')
        context['QOFS'] = QuestionOfTest.objects.filter(test_id=self.kwargs.get('pk')).filter(level_of_question_id=self.kwargs.get('level_pk'))
        context['LOT'] = LevelOfTest.objects.filter(test_id=self.kwargs.get('pk'))
        context['QOF'] = QuestionOfTest.objects.filter(level_of_question_id=self.kwargs.get('level_pk'))
        context['CQ'] = ClosedQuestion.objects.get(question_of_test_id=self.kwargs.get('question_pk')) # выводим только те вопросы, которые входят в этот теста
        CQ = ClosedQuestion.objects.get(question_of_test_id=self.kwargs.get('question_pk'))
        context['CQO'] =  ClosedQuestionOption.objects.filter(question_id=CQ)
        return context

    # # редирект
    # def get_success_url(self):
    #     test_pk = self.kwargs.get('pk')
    #     return reverse('tests:detail', kwargs={'pk': test_pk})

# @login_required
# def Testing(request,pk):
#     LOT = LevelOfTest.objects.filter(test_id=pk).order_by('level_index_number').first() #Первый уровнь
#     LOTS = LevelOfTest.objects.filter(test_id=pk)
#     QOF = QuestionOfTest.objects.filter(level_of_question_id=LOT).order_by('question_index_number').first() #Первый вопрос
#     CQ = ClosedQuestion.objects.get(question_of_test_id=QOF)
#     CQO = ClosedQuestionOption.objects.filter(question_id=CQ)
#
#     correct_qu_amount = 0
#     wrong_qu_amount = 0
#     counter = 1
#
#     context = {
#         'LOT':LOT,
#         'QOF':QOF,
#         'CQ': CQ,
#         'CQO': CQO,
#     }
#     return render(request,'tests/test_testing.html',context)