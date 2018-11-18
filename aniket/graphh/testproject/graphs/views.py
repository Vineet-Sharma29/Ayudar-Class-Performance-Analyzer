from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, QuizResult, Quiz
from django.http import JsonResponse

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
		'quizzes' : quizzes
	}
	return render(request, 'graph/graph-view.html', context)