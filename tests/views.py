# -*- coding: UTF-8 -*-
import json
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, render_to_response, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView , UpdateView
from django.views.generic.base import ContextMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse,reverse_lazy
from .forms import TestForm,ClosedQuestionForm,ClosedQuestionOptionForm,LevelForm,QuestionForm
from .models import Test, QuestionOfTest,LevelOfTest,ClosedQuestion, ClosedQuestionOption
# Create your views here.

class TestListAllView(ListView):
    template_name = 'tests/tests.html'
    def get_queryset(self):
        return Test.objects.all().order_by('id')

class TestDetailAllView(DetailView):
    template_name = 'tests/test_form.html'
    def get_queryset(self):
        return Test.objects.filter(user__is_active=True)

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
        #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        return kwargs

    def get_success_url(self):
        return reverse('tests:mylist')

#изменение
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
        #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        return kwargs

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
        #obj.question_of_test = self.request.question_of_test
        return super(QOTCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QOTCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание вопроса'
        return context

        # def get_form_kwargs(self):
        #     kwargs = super(QOTCreateView, self).get_form_kwargs()
        #     print(kwargs)
        #     kwargs['question_of_test_id'] = self.request.question_of_test_id
        #     #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        #     return 0

# вопросы закрытого типа
class CQCreateView(LoginRequiredMixin, CreateView):
    model = ClosedQuestion
    template_name = 'tests/form.html'
    form_class = ClosedQuestionForm

    def get_queryset(self):
        return ClosedQuestion.objects.filter(user=self.request.user)

    def form_valid(self, form):
        obj = form.save(commit=False)
        #obj.question_of_test = self.request.question_of_test
        return super(CQCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CQCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание вопроса закрытого типа'
        return context

        # def get_form_kwargs(self):
        #     kwargs = super(QOTCreateView, self).get_form_kwargs()
        #     print(kwargs)
        #     kwargs['question_of_test_id'] = self.request.question_of_test_id
        #     #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        #     return 0
    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs = {'pk': test_pk})

#Уровень
# Создание нового уровня в тесте
class LOTCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tests/form.html'
    model = LevelOfTest
    form_class = LevelForm
    #fields = '__all__'

    #initial = {'test': testid , }
    def get_initial(self):
        test_id = self.kwargs.get('pk')
        level_index_number = LevelOfTest.objects.filter(test_id=test_id).count()+1
        initial = {'test': test_id, 'level_index_number': level_index_number, }
        return initial

    def get_queryset(self):
        return LevelOfTest.objects.all()

    # def get(self,request, *args, **kwargs):
    #     fields = ['test','level_index_number','name_level','solution']
    #     self.fields['test'] = self.kwargs.get('pk')

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        return super(LOTCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LOTCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание уровня'
        return context

    # редирект обратно к списку уровням
    def get_success_url(self):
        test_pk = self.kwargs.get('test_id')
        return reverse('tests:detail', kwargs = {'pk': test_pk})

    # def get_form_kwargs(self):
    #     kwargs = super(LOTCreateView, self).get_form_kwargs()
    #     kwargs['request'] = self.request
    #     #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
    #     return kwargs

    # def get_success_url(self):
    #     print("successfully posted")
    #     return reverse('arenas:detail', kwargs={'pk': self.object.pk})

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

    # редирект обратно к списку уровням
    def get_success_url(self):
        test_pk = self.kwargs.get('pk')
        return reverse('tests:detail', kwargs={'pk': test_pk})

    # def get_form_kwargs(self):
    #     kwargs = super(LOTUpdateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
    #     return kwargs

# Проверка
# class Testing(DetailView):
#     template_name = 'tests/test_testing.html'
#     def get_queryset(self):
#         return LevelOfTest.objects.all()
    # def post(self, request, *args, **kwargs):
    #     data = serializers.serialize('json',Test.objects.all().filter())
    #     return HttpResponse(json.loads(data))

@login_required
def Testing(request,pk):
    LOT = LevelOfTest.objects.all().filter(test_id=pk).first() #Первый уровнь
    QOF = QuestionOfTest.objects.all().filter(test_id=pk).first() #Первый вопрос
    CQ = ClosedQuestion.objects.all().filter(question_of_test__test_id=pk).first()
    CQO = ClosedQuestionOption.objects.all().filter(question__question_of_test__test_id=pk)
    context = {
        'LOT':LOT,
        'QOF':QOF,
        'CQ': CQ,
        'CQO': CQO,
    }
    return render(request,'tests/test_testing.html',context)