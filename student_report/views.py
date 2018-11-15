from django.shortcuts import render

def student_report(request):
    return render(request, "student_report/student_report.html")
