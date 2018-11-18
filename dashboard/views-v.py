from django.shortcuts import render
# import algo as ag


def dashboard(request):
    return render(request, "dashboard/dashboard.html")



# for student in students:
#     marks = tuple(row)
#     v = ag.initialize(marks, header)
#     CourseStat = CourseStats(marks)
#     ExamStat = ExamStats(marks)
#     Labels = PersistenLabels(v)
#
#

def needy_list(request):
    return render(request, "dashboard/needy_list.html")






