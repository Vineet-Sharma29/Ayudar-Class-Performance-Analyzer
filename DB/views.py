
from django.shortcuts import render
from .models import Enrollments
from .models import Marks
from .models import csvfile
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


def uselesspage(request):
    return render(request, 'DB/uselesspage.html')

def output(request):
    if request.method == 'POST' and request.FILES['uploadedfile']:
        myfile = request.FILES['uploadedfile']
        name = myfile.name
        fs = FileSystemStorage()
        s = fs.save(myfile.name, myfile)
        url = fs.url(s)
        print(url)
        return some(url)

def some(path):

    csvfile.objects.create(req_file=path)

    co_id="ASE"
    pr_id = "SUBU"

    Marks.objects.filter(course_id=co_id).delete()
    Enrollments.objects.filter(course_id=co_id).delete()

    with open(path)as f:
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

            for j in range(0, len(f2) - 2):
                sid = f2[0]
                sname = f2[1]
                marks = f2[j + 2]
                qname = f1[j + 2]

                Marks.objects.create(student_name=sname,student_id=sid, marks=marks, q_name=qname, course_id=co_id, prof_id=pr_id)

    all_quiz_marks_in_a_course()
    all_quiz_marks_in_all_courses()
    return HttpResponse("check the database :)")


def all_quiz_marks_in_a_course():
    b=Marks.objects.filter(student_id="063", course_id="ASE", prof_id="SUBU").values_list('q_name','marks')
    print(b)
    print(type(b))



def all_quiz_marks_in_all_courses():
    print(Marks.objects.filter(student_id="063").values_list('course_id','q_name','marks'))



def return_firstline_as_tuple(fline):
    print(tuple(fline))



def return_tuple(line):
    req_tuple = ()
    for n in range(1, len(line)):
        line[n] = line[n].rstrip()
        x = tuple(line[n].split(','))
        req_tuple += (x,)
    print(req_tuple)



