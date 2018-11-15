from django.shortcuts import render,redirect
from .models import professor_profile,course,User
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from .forms import RegisterForm,LoginForm,ResetForm
from django.contrib.auth import authenticate,login,logout
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
'''

Home

'''

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
                    return redirect('http://127.0.0.1:8000/lms/home')
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

            otp = ''

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
            otp12 = {'otp1':otp}
            request.session['username']=form.cleaned_data.get('username')
            return render(request,'login/otp.html',otp12)
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
    if request.method=='POST':
        otp=str(request.POST['otp'])
        otp1=str(request.POST['otp1'])
        otp = otp.upper()
        if otp==otp1:
            username=request.session['username']
            p = User.objects.get(username=username)
            print(p)
            p.is_active=True
            password = p.password
            print(password)
            login(request,p)
            return redirect('http://127.0.0.1:8000/lms/home')

        else:
            username = request.session['username']
            p = User.objects.get(username=username)

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
        if form .is_valid():
            mail = form.cleaned_data.email
            otp = ''
            for i in range(6):
                otp = otp + str(random.randint(0, 9))
            mail_subject = 'Password Reset Otp Verification'
            message = 'Your otp is ' + otp
            send_mail(
                mail_subject,
                message,
                'iiits2021@gmail.com',
                [mail],
            )
            otp12 = {'otp1': otp}
            request.session['email']=mail
            return render(request, 'login/otp2.html', otp12)
    else:
        form1 = ResetForm()
        return render(request,'login/reset_email.html',{'form':form1})



def reset_otp_verify(request):
    if request.method=='POST':
        otp=str(request.POST['otp'])
        otp1=str(request.POST['otp1'])
        otp = otp.upper()
        if otp==otp1:
            return render(request,'login/reset_password.html',{})
        else:
            del request.session['email']
            return HttpResponse('Worng Otp,to resend click <a href="http://127.0.0.1:8000/lms/reset_password/">here</a>')
    else:
        return HttpResponse('404 error')

def save_password(request):
    mail = request.session['email']
    user = User.objects.get(email=mail)
    user.password = request.POST['password']

def editprofile(request):
    # if request.method=='Post':
    #     pass
    # else:
    #     form =
    #     context={}
    pass


# def display_user_profile(request):
#     # prof = request.user.profile_set[0]
#     # print(prof)
#     if request.method=='POST':
#         emailid = str(request.session['emailid'])
#         print(emailid)
#         profileMy=professor.objects.get(pk=16).profile_set.first()
#         # if profileMy:
#         #     print("There is a profile")
#         # else:
#         #     print("No profile")
#         # print(profileMy)
#         form = ProfileForm(request.POST, request.FILES,instance=profileMy)
#         print("commit False")
#
#         # print(p)
#         # p.professor = professor.objects.all().first()
#         print("out valid")
#         if form.is_valid():
#             form.save(commit=False)
#             print("in valid")
#             print("commit False")
#             # p.save()
#             return HttpResponse('HIII')
#     else:
#         form = ProfileForm()
#         emailid = str(request.session['emailid'])
#         email_set = professor.objects.filter(emailid=emailid)
#         args={'profile':email_set[0],'form1':form}
#         return render(request,'login/profile.html',args)