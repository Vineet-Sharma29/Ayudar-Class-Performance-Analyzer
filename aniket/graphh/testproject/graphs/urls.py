from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
	path('graph', selectstudent, name="student-select"),
	path('graph/<int:rollno>', studentgraph, name="graph-view"),
]