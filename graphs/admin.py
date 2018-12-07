from django.contrib import admin
from .models import Student, Quiz, QuizResult

admin.site.register(Student)
admin.site.register(Quiz)
admin.site.register(QuizResult)