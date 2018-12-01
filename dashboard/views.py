from django.contrib.auth.models import User
from django.shortcuts import render

from registration.models import professor_profile
from .models import Marks
from .models import csvfile, Enrollments
from django.http import HttpResponse
from .forms import file_class

from django.shortcuts import render
import dashboard.algo as alg
from django.contrib.auth.decorators import login_required

def add_to_database(pat):
    path = 'media/media_/' + pat
    co_id = "ASE"
    pr_id = "SUBU"

    Marks.objects.filter(course_id=co_id).delete()
    Enrollments.objects.filter(course_id=co_id).delete()

    with open(path) as f:
        f1 = f.readline().split(",")
        f1[len(f1) - 1] = f1[len(f1) - 1].rstrip()

        return_firstline_as_tuple(f1)

        f.seek(0, 0)
        f_all = f.readlines()

        tuples = return_tuple(f_all)
        print(list(tuples))
        headers =  ['RollNumber', 'Name', 'exam-mid-35', 'exam-end-50', 'lab-basic01-20','lab-basic02-20','lab-basic03-20','asgn-basic01-15','asgn-basic02-15','asgn-basic03-15','asgn-basic04-15','oth-quiz01-30', 'oth-quiz02-30', 'oth-quiz03-30']
        df = alg.initialse(tuples, headers)
        # print(df.columns)
        NeedyList = alg.mainFunc(df)
        CourseOverview = alg.CourseStats(df)
        ExamOverview = alg.ExamStats(df)
        #Persistent_Labels = alg.PersistentLabels(df)
        #Performance_Labels = alg.PerformanceLabels(df)
        print(CourseOverview)
        f_all[len(f_all) - 1] = f_all[len(f_all) - 1] + '\n'
        # for i in range(1, len(f_all)):
        #     f_all[i] = f_all[i].rstrip()
        #     f2 = f_all[i].split(',')
        #
        #     Enrollments.objects.create(course_id=co_id, student_id=f2[0], student_name=f2[1], prof_id=pr_id,
        #                                status="not_needy")
        #
        #     for j in range(0, len(f2) - 2):
        #         sid = f2[0]
        #         sname = f2[1]
        #         marks = f2[j + 2]
        #         qname = f1[j + 2]
        #
        #         Marks.objects.create(student_name=sname, student_id=sid, marks=marks, q_name=qname, course_id=co_id,
        #                              prof_id=pr_id)
    #
    # all_quiz_marks_in_a_course()
    # all_quiz_marks_in_all_courses()
    return [CourseOverview, ExamOverview, NeedyList]


#
# def call():
#     print(Marks.objects.filter(q_name="q3"))

#
# def return_tuple(line):
#     req_tuple = ()
#     for n in range(1, len(line)):
#         line[n] = line[n].rstrip()
#         x = tuple(line[n].split(','))
#         req_tuple += (x,)
#     print(req_tuple)

# tup=tuple(a)
# print(tup(0))

# a[0]=tuple(a[0])
# print(type(a[0]))

# tup=tuple(a)
#
# print(tup(0))

# @login_required
def dashboard(request):
    form1 = file_class(request.POST, request.FILES or None)
    if request.method == 'POST':
        if form1.is_valid():
            form1.save()
            print(request.FILES['req_file'])
            file1 = str(request.FILES['req_file'])
            dashboard_stats = add_to_database(file1)
            user = User.objects.get(username=request.user)
            profile = professor_profile.objects.get(professor=user)
            context = {'form':form1,'courseoverview':dashboard_stats[0],'examoverview':dashboard_stats[1],'needystudents':dashboard_stats[2],'username': user.username, 'photo': profile.professor_photo}
            return render(request, "dashboard/dashboard.html",context)
        else:
            return HttpResponse("form is invalidd")
    else:
        # user = User.objects.get(username=request.user)
        user = User.objects.get(username="vineet")
        profile = professor_profile.objects.get(professor=user)
        form1 = file_class()
        return render(request, "dashboard/dashboard.html",
                      {'form': form1, 'username': user.username, 'photo': profile.professor_photo,'courseoverview':('Moderate','Low',[1,2,3,4,5],'46-47',60.09,90.08,50.08),'examoverview':('Medium','High',[1,2,3,4,5],'46-47',62.09,91.08,52.08),'needystudents':[1,2,3,4,5]})


# for student in students:
#     marks = tuple(row)
#     v = ag.initialize(marks, header)
#     CourseStat = CourseStats(marks)
#     ExamStat = ExamStats(marks)
#     Labels = PersistenLabels(v)
#


def needy_list(request):
    return render(request, "dashboard/needy_list.html")


def list_of_students(request):
    return render(request, "dashboard/list_of_students.html")


def custom_404(request):
    return render(request, "dashboard/404.html")


def all_quiz_marks_in_a_course():
    b = Marks.objects.filter(student_id="55", course_id="ASE", prof_id="SUBU").values_list('q_name', 'marks')
    print(b)
    print(type(b))


def all_quiz_marks_in_all_courses():
    print(Marks.objects.filter(student_id="55").values_list('course_id', 'q_name', 'marks'))


def return_firstline_as_tuple(fline):
    print(tuple(fline))


def return_tuple(line):
    req_tuple = []
    for n in range(1, len(line)):
        line[n] = line[n].rstrip()
        x = line[n].split(',')
        y = []
        y.append(x[0])
        y.append(x[1])
        for i in range(2, len(x)):
            y.append(int(x[i]))
        req_tuple += [y]
    #print(req_tuple)
    return req_tuple
