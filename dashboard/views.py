
from django.shortcuts import render
from .models import Marks
from .models import csvfile
from django.http import HttpResponse
#from .forms import file_class
from django.core.files.storage import FileSystemStorage


from django.shortcuts import render
# import algo as ag





def uselesspage(request):
    return render(request, 'DB/uselesspage.html')

def output(request):
    if request.method == 'POST' and request.FILES['marksFile']:
        myfile = request.FILES['marksFile']
        name = myfile.name
        fs = FileSystemStorage()
        ame = fs.save(myfile.name, myfile)
        url = fs.url(ame)
        print(url)
        return some(url)

def some(pat):
    #var = "/home/phani/PycharmProjects/ASE/"
    csvfile.objects.create(req_file=pat)
    co_id="DSAA"
    Marks.objects.filter(course_id=co_id).delete()
    pr_id=2
    with open(pat)as f:
        f1 = f.readline().split(",")
        f1[len(f1) - 1] = f1[len(f1) - 1].rstrip()
        #printreq(f1)
        f.seek(0,0)
        f_all = f.readlines()
        return_tuple(f_all)
        f_all[len(f_all) - 1] = f_all[len(f_all) - 1] + '\n'
        for i in range(1, len(f_all)):
            f_all[i] = f_all[i].rstrip()
            f2 = f_all[i].split(',')
            for j in range(0, len(f2) - 1):
                sid = f2[0]
                marks = f2[j + 1]
                name = f1[j + 1]

                some =  Marks.objects.create(student_id=sid, marks=marks, q_name=name, course_id=co_id, prof_id=pr_id)
    #printreq1(Marks.objects.all())
    #printreq(v)
    call()
    return HttpResponse("check your database :)")

def call():
    print(Marks.objects.filter(q_name="q3"))

def return_tuple(line):
    req_tuple = ()
    for n in range(1, len(line)):
        line[n] = line[n].rstrip()
        x = tuple(line[n].split(','))
        req_tuple += (x,)
    print(req_tuple)

    # tup=tuple(a)
    # print(tup(0))


    # a[0]=tuple(a[0])
    # print(type(a[0]))

    # tup=tuple(a)
    #
    # print(tup(0))



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


def list_of_students(request):
    return render(request, "dashboard/list_of_students.html")



