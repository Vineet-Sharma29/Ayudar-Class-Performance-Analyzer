from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, QuizResult, Quiz
import json
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from xlrd import open_workbook
import xlrd

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
	avg = quiz.classaverage
	context = {
		'quiz' : quiz,
		'results' : results,
		'avg' : avg
	}
	return render(request, 'graph/quizgraph.html', context)

def feeddata(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		result = "Success"
		if filename.endswith('.xlsx') or filename.endswith('.xls'):
			workbook = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, filename))
			if workbook.nsheets < 1:
				result = "File is empty.Please try again."
			else:
				sheet = workbook.sheet_by_index(0)
				if sheet.cell(0, 0).value == "SID":
					for column in range(1, sheet.ncols):
						testname = sheet.cell(0, column).value
						if Quiz.objects.filter(name=testname).count():
							currquiz = Quiz.objects.get(name=testname)
						else:
							currquiz = Quiz.objects.create(name=testname, prof=request.user.username)
						for rownum in range(1, sheet.nrows):
							SID = sheet.cell(rownum, 0).value
							marks = sheet.cell(rownum, column).value
							if Student.objects.filter(rollno=SID).count():
								Stu = Student.objects.get(rollno=SID)
								if QuizResult.objects.filter(quiz = currquiz, student = Stu).count():
									cur_result = QuizResult.objects.get(quiz= currquiz, student = Stu)
									cur_result.marks = marks
									cur_result.save()
								else:
									QuizResult.objects.create(quiz= currquiz, student=Stu, marks=marks)
							else:
								result = "Some students did not exist please add the record manually."
				else:
					result = "Invalid File"
		else:
			result = "Please check the file extension and try again."
		return render(request, 'graph/feeddata.html', {
			'result' : result,
			'uploaded_file_url': uploaded_file_url
		})
	return render(request, 'graph/feeddata.html')