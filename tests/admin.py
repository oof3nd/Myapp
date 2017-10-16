# -*- coding: UTF-8 -*-
from django.contrib import admin
from tests.models import Test, Category,ResultScale,Tag,TestRate,Result,ClosedQuestion,ClosedQuestionOption,QuestionOfTest
# Register your models here.
admin.site.register(Test)
admin.site.register(Category)
admin.site.register(ResultScale)
admin.site.register(Tag)
admin.site.register(TestRate)
admin.site.register(Result)
admin.site.register(QuestionOfTest)
admin.site.register(ClosedQuestion)
admin.site.register(ClosedQuestionOption)
