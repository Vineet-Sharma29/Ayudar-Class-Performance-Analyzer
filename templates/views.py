
from django.shortcuts import render
from .models import Marks
from .models import csvfile
from django.http import HttpResponse
#from .forms import file_class
from django.core.files.storage import FileSystemStorage


def uselesspage(request):
    return render(request, 'DB/uselesspage.html')

# def output(request):
#     if request.method == "POST":
#         print("checkedhiohohoerhgrepgjergegergogioioijoi")
#         myform = file_class(request.POST, request.FILES)
#         if myform.is_valid():
#             print("checkedasdfghjkl")
#             tab = csvfile()
#             tab.req_file = myform.cleaned_data["file"]
#             tab.save()
#             #saved = True
#             #instance = csvfile.objects.create(req_file=request.FILES['file'])
#             #instance.save()
#     return HttpResponse("check your database :)")


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
    var = "/home/phani/PycharmProjects/ASE/"
    csvfile.objects.create(req_file=var+pat)
    with open(var+pat)as f:
        f1 = f.readline().split(",")
        f1[len(f1) - 1] = f1[len(f1) - 1].rstrip()
        # print(f1)
        f.seek(0, 0)
        f_all = f.readlines()
        f_all[len(f_all) - 1] = f_all[len(f_all) - 1] + '\n'
        for i in range(1, len(f_all)):
            f_all[i] = f_all[i].rstrip()
            f2 = f_all[i].split(',')
            for j in range(0, len(f2) - 1):
                sid = f2[0]
                cid = 2
                marks = f2[j + 1]
                name = f1[j + 1]
                some =  Marks.objects.create(student_id=sid, marks=marks, q_name=name, course_id=cid)
    #printreq(Marks.objects.all())
    #printreq(v)
    return HttpResponse("check your database :)")

#def printreq(a):
    # tup=tuple(a)
    # print(tup(0))


    # a[0]=tuple(a[0])
    # print(type(a[0]))

    # tup=tuple(a)
    #
    # print(tup(0))


