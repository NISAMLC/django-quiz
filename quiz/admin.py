from django.contrib import admin
from .models import QuizSet, Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_set', 'question_text', 'correct_option')

admin.site.register(QuizSet)
admin.site.register(Question, QuestionAdmin)

