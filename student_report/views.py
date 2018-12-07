from django.shortcuts import render
from dashboard.models import Marks,Enrollments,User,student_ranks
from registration.models import professor_profile
from django.shortcuts import HttpResponse

def student_report(request,id):
    if id == 0:
        return HttpResponse('No  reports to show')
    user = User.objects.get(username=request.user)
    profile = professor_profile.objects.get(professor=user)
    student_quizzes = Marks.objects.filter(prof_id=user,course_id=profile.professor_course,student_id=id)
    quizzes = []
    for i in student_quizzes:
        quiz_name = i.q_name
        marks = i.marks
        quiz_students = Marks.objects.filter(course_id=profile.professor_course,prof_id=user,q_name=quiz_name)
        sum=0
        for j in quiz_students:
            sum=sum+int(j.marks)
        average = sum/len(quiz_students)
        quizzes.append([quiz_name,marks,average])
    name = Enrollments.objects.get(prof_id=user,course_id=profile.professor_course,student_id=id)
    rank = student_ranks.objects.get(student_id=id)
    ranks =[rank.class_rank,rank.exam_rank,rank.lab_rank,rank.asgn_rank,rank.oth_rank]
    student_marks = [rank.best_exam,rank.best_marks,rank.worst_exam,rank.worst_marks,rank.overall]
    return render(request, "student_report/student_report.html",{'quizzes':quizzes,'sid':id,'student':name.student_name,'ranks':ranks,'Marks':student_marks})


def charts(request):
    return render(request, "student_report/charts.html")


def tables(request):
    return render(request, "student_report/tables.html")