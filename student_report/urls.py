from django.urls import path
from . import views

urlpatterns = [
    path('student_report/', views.student_report, name="student_report"),
]
