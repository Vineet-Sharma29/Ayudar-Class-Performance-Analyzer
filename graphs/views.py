from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, QuizResult, Quiz
import json

def selectstudent(request):
	if request.method == "POST":
		return redirect("graph-view", request.POST['rollno'])
	context = {
		'students' : Student.objects.all(),
	}
	return render(request, 'graph/selectstudent.html', context)

def studentgraph(request, rollno):
	student = get_object_or_404(Student, rollno=rollno)
	quizzes = QuizResult.objects.filter(student=student)
	context = {
		'student' : student,
		'quizzes' : quizzes,
	}
	return render(request, 'graph/graph.html', context)

def selectquiz(request):
	if request.method == "POST":
		return redirect("quiz-results", request.POST['quizid'])
	context = {
		'quizzes' : Quiz.objects.all(),
	}
	return render(request, 'graph/selectquiz.html', context)

def quizgraph(request, quizid):
	quiz = get_object_or_404(Quiz, id=quizid)
	results = QuizResult.objects.filter(quiz=quiz)
	avg = results[1].classaverage
	context = {
		'quiz' : quiz,
		'results' : results,
		'avg' : avg
	}
	return render(request, 'graph/quizgraph.html', context)