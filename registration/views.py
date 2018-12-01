from django.shortcuts import render, redirect
from .models import professor_profile, User
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from .forms import RegisterForm, LoginForm, ResetForm, ProfileForm, CourseForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import ResetPasswordForm
from dashboard.models import course_dashboard

# login

def login_display(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            emailid = form.cleaned_data.get("emailid")
            password = form.cleaned_data.get('password')
            print(emailid)
            userlog = User.objects.get(email=emailid)
            print(userlog)
            user = authenticate(username=userlog, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard:dashboard')
                else:
                    return HttpResponse('Not registered')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login/login.html', context)


# register


def register_display(request):
    if (request.method == 'POST'):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            email=form.cleaned_data["email"],
                                            password=form.cleaned_data["password"]
                                            )

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]

            user.save()
            p = professor_profile.objects.create(professor=user)
            mail = form.cleaned_data.get('email')
            print(mail)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'iiits2021@gmail.com', [mail])
            return HttpResponse('email has been sent')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'login/register1.html', context)



'''

logout

'''


@login_required
def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')


'''

forgot password

'''


def reset_password(request):
    if request.method == 'POST':
        form1 = ResetForm(request.POST)
        if form1.is_valid():
            mail = form1.cleaned_data.get('email')
            user=  User.objects.get(email=mail)
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Link.'
            message = render_to_string('login/reset_confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'iiits2021@gmail.com', [mail])
            return HttpResponse('Link has been sent to your email')
    else:
        form1 = ResetForm()
    return render(request, 'login/reset_email.html', {'form': form1})


def display_reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        #login(request, user)
        request.session['email']=user.email
        return redirect('registration:save_password')

    else:
        return HttpResponse('Activation link is invalid!')

def save_password(request):
    if request.method=="POST":
        form1 = ResetPasswordForm(request.POST)
        if form1.is_valid():
            mail = request.session['email']
            user = User.objects.get(email=mail)
            print(user)
            user.set_password(form1.cleaned_data.get('password'))
            user.save()
            return HttpResponse("Password has been reset Please login<a href='{{ url 'registrartion:login' }}'>here</a>")
    else:
        form1 = ResetPasswordForm()
    return render(request,'login/reset_password.html',{'form':form1})


def editprofile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        print(user)
        form = ProfileForm(request.POST, request.FILES, instance=professor_profile.objects.get(professor=user))
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
        form1 = ProfileForm(initial={'professor_description': profile.professor_description,
                                     'professor_photo': profile.professor_photo})
        context = {'form': form1}
        return render(request, 'login/profile.html', context)


def show_profile(request):
    user1 = User.objects.get(username=request.user)
    profile1 = professor_profile.objects.get(professor=user1)
    return render(request, 'login/show_profile.html', {'user': user1, 'profile': profile1})


@login_required()
def course_selection(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            profile = professor_profile.objects.get(professor=user)
            profile.professor_course = str(form.cleaned_data['course_id']).upper()
            profile.save()
            course_dashboard.objects.create(professor=user)
            return redirect('dashboard:dashboard')
    else:
        form = CourseForm()
    return render(request, 'login/course.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('registration:course_selection')

    else:
        return HttpResponse('Activation link is invalid!')