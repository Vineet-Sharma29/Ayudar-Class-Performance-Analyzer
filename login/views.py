from django.shortcuts import render,redirect
from .models import professor_profile,course,User
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from .forms import RegisterForm,LoginForm,ResetForm,ProfileForm,CourseForm
from django.contrib.auth import authenticate,login,logout
import random
from django.contrib.auth.decorators import login_required
'''

Home

'''
otp=''
otp2=''

def home_display(request):
    return render(request,'login/home.html',{})
'''
login Home
'''

def inhome_display(request):
    return render(request,'login/hom2.html')


''''
login
'''

def login_display(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            emailid = form.cleaned_data.get("emailid")
            password = form.cleaned_data.get('password')

            print(emailid)
            userlog = User.objects.get(email=emailid)
            print(userlog)
            user = authenticate(username=userlog,password=password)
            if user:
                if user.is_active:
                    login(request,user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('http://127.0.0.1:8000//')
                else:
                    return HttpResponse('Not registered')
    else:
        form = LoginForm()
    context = {
         'form': form
    }
    return render(request, 'login/login.html', context)


'''
register
'''


def register_display(request):
    if (request.method=='POST'):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            email=form.cleaned_data["email"],
                                            password=form.cleaned_data["password"]
                                            )

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]

            user.save()


            mail = form.cleaned_data.get('email')
            print(mail)

            global otp

            for i in range(6):
                otp=otp+str(random.randint(0,9))
            mail_subject ='Otp Verifiaction'
            message = 'Your otp is '+otp
            send_mail(
                mail_subject,
                message,
                'iiits2021@gmail.com',
                [mail],
            )
            request.session['username']=form.cleaned_data.get('username')
            return render(request,'login/otp.html',{})
    else:
        form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request,'login/register1.html',context)

'''

register otp verify

'''


def otp_verify(request):
    global otp
    if request.method=='POST':
        otp1=str(request.POST['otp'])
        otp = otp1.upper()
        if otp==otp1:
            username=request.session['username']
            p = User.objects.get(username=username)
            print(p)
            p.is_active=True
            password = p.password
            print(password)
            q = professor_profile.objects.create(professor=p)
            login(request,p)
            otp=''
            return redirect('http://127.0.0.1:8000/lms/course/')

        else:
            username = request.session['username']
            p = User.objects.get(username=username)
            otp=''
            p.delete()
            return redirect('http://127.0.0.1:8000/lms/register/')
    else:
        return HttpResponse('Please Register')





'''

logout

'''

@login_required
def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/lms/hom/')

'''

forgot password

'''

def reset_password(request):
    if request.method=='POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data.get('email')
            global otp2
            for i in range(6):
                otp2 = otp2 + str(random.randint(0, 9))
            mail_subject = 'Password Reset Otp Verification'
            message = 'Your otp is ' + otp2
            send_mail(
                mail_subject,
                message,
                'iiits2021@gmail.com',
                [mail],
            )
            request.session['email']=mail
            return render(request, 'login/otp2.html')
        else:
            return HttpResponse('Email does not exist')
    else:
        form1 = ResetForm()
        return render(request,'login/reset_email.html',{'form':form1})



def reset_otp_verify(request):
    if request.method=='POST':
        global otp2
        otp=str(request.POST['otp'])
        otp = otp.upper()
        if otp2==otp:
            otp2=''
            return render(request,'login/reset_password.html',{})

        else:
            otp2=''
            del request.session['email']
            return HttpResponse('Worng Otp,to resend click <a href="http://127.0.0.1:8000/lms/reset_password/">here</a>')
    else:
        return HttpResponse('404 error')

def save_password(request):
    mail = request.session['email']
    user = User.objects.get(email=mail)
    user.set_password(request.POST['password'])
    user.save()
    return HttpResponse('Password has been reset Please login<a href="http://127.0.0.1:8000/lms/login/">here</a>')

def editprofile(request):
    if request.method=='POST':
        user = User.objects.get(username=request.user)
        print(user)
        form = ProfileForm(request.POST,request.FILES,instance=professor_profile.objects.get(professor=user))
        if form.is_valid():
            course_id = form.cleaned_data['professor_course']
            profile = form.save(commit=False)
            profile.professor_description = form.cleaned_data['professor_description']
            profile.save()
            return HttpResponse('saved <a href="view-profiles">here</a>')

    else:
        user = User.objects.get(username=request.user)
        profile = professor_profile.objects.get(professor=user
                                                )
        form1 = ProfileForm(initial={'professor_description':profile.professor_description,'professor_photo':profile.professor_photo})
        context = { 'form':form1 }
        return render(request,'login/profile.html',context)

def show_profile(request):
    user1 = User.objects.get(username=request.user)
    profile1 = professor_profile.objects.get(professor=user1)
    return render(request,'login/show_profile.html',{'user':user1,'profile':profile1})

@login_required()
def course_selection(request):
    if request.method=='POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            profile = professor_profile.objects.get(professor=user)
            profile.professor_course=str(form.cleaned_data['Course']).upper()
            profile.save()
            return redirect('http://127.0.0.1:8000/lms/home')
    else:
        myform = CourseForm()
        return render(request,'login/course.html',{'form':myform})
