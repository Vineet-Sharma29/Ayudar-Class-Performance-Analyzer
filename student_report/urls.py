from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_report, name="student_report"),
]
