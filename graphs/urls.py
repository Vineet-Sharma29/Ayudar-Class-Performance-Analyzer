from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
	path('graph', selectstudent, name="student-select"),
	path('graph/<int:rollno>', studentgraph, name="graph-view"),
	path('quiz', selectquiz, name="quiz-select"),
	path('quiz/<int:quizid>', quizgraph, name="quiz-results"),
	path('feeddata', feeddata, name="feeddata"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)