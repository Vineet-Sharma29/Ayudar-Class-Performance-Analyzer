
from django.shortcuts import render
from .models import Enrollments
from .models import Marks
from .models import csvfile
from django.http import HttpResponse
#from .forms import file_class
from django.core.files.storage import FileSystemStorage


def uselesspage(request):
    return render(request, 'DB/uselesspage.html')

def output(request):
    if request.method == 'POST' and request.FILES['naam']:
        myfile = request.FILES['naam']
        name = myfile.name
        fs = FileSystemStorage()
        ame = fs.save(myfile.name, myfile)
        url = fs.url(ame)
        print(url)
        return some(url)

def some(pat):
    #var = "/home/phani/PycharmProjects/ASE/"
    csvfile.objects.create(req_file=pat)
    co_id="ASE"
    Marks.objects.filter(course_id=co_id).delete()
    pr_id="Subu"
    with open(pat)as f:
        f1 = f.readline().split(",")
        f1[len(f1) - 1] = f1[len(f1) - 1].rstrip()
        return_firstline_as_tuple(f1)

        f.seek(0,0)
        f_all = f.readlines()
        return_tuple(f_all)
        f_all[len(f_all) - 1] = f_all[len(f_all) - 1] + '\n'

        for i in range(1, len(f_all)):
            f_all[i] = f_all[i].rstrip()
            f2 = f_all[i].split(',')
            Enrollments.objects.create(course_id=co_id,student_id=f2[0],student_name=f2[1],prof_id=pr_id,status="not_needy")
            for j in range(0, len(f2) - 3):
                sid = f2[0]
                sname = f2[1]
                marks = f2[j + 2]
                qname = f1[j + 2]

                Marks.objects.create(student_name=sname,student_id=sid, marks=marks, q_name=qname, course_id=co_id, prof_id=pr_id)
    #printreq1(Marks.objects.all())
    #printreq(v)
    call()
    return HttpResponse("check your database :)")

def call():
    print(Marks.objects.filter(q_name="q3"))

def return_firstline_as_tuple(fline):
    print(tuple(fline))

def return_tuple(line):
    req_tuple = ()
    for n in range(1, len(line)):
        line[n] = line[n].rstrip()
        x = tuple(line[n].split(','))
        req_tuple += (x,)
    print(req_tuple)

  
