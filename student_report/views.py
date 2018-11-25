from django.shortcuts import render


def student_report(request):
    return render(request, "student_report/student_report.html")


def charts(request):
    return render(request, "student_report/charts.html")


def tables(request):
    return render(request, "student_report/tables.html")