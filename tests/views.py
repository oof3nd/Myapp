from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView , UpdateView, View
from django.utils.translation import ugettext_lazy as _
from .forms import TestForm,ClosedQuestionForm,ClosedQuestionOptionForm

from .models import Test, QuestionOfTest,ClosedQuestion, ClosedQuestionOption
# Create your views here.

class TestListAllView(ListView):
    template_name = 'tests/tests.html'
    def get_queryset(self):
        return Test.objects.all()


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
        context['QuestionOfTest_object_list'] = QuestionOfTest.objects.all().filter(test_id=self.object.id)
        context['ClosedQuestion_object_list'] = ClosedQuestion.objects.all().filter(question_of_test__test_id=self.object.id) # выводим только те вопросы, которые входят в этот теста
        context['ClosedQuestionOption_object_list'] = ClosedQuestionOption.objects.all()
        return context
    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)


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

class QOTCreateView(LoginRequiredMixin, CreateView):
    model = ClosedQuestion
    template_name = 'tests/form.html'
    form_class = ClosedQuestionForm

    def get_queryset(self):
        return  ClosedQuestion.objects.all().filter(question_of_test__test_id=self.object.id)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.question_of_test = self.request.question_of_test
        return super(QOTCreateView,self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(QOTCreateView, self).get_context_data(**kwargs)
        print(kwargs)
        context['title'] = 'Создание вопроса'
        return context

    # def get_form_kwargs(self):
    #     kwargs = super(QOTCreateView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['question_of_test_id'] = self.request.question_of_test_id
    #     #kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
    #     return 0


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
