"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a UruRL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_display,name='login'),
    path('signup/', views.register_display,name='singup'),
    path('register/otp_verify/',views.otp_verify,name='otp'),
    path('logout/',views.logout_view,name='logout'),
    path('login/reset_password/',views.reset_password,name='reset'),
    path('login/reset_password/reset_otp_verify/',views.reset_otp_verify,name='reset'),
    path('login/reset_password/reset_otp_verify/save_password/',views.save_password,name='save_password'),
    path('dashboard/edit_profile/',views.editprofile,name='edit_profile'),
    path('dashboard/my_profile/',views.show_profile,name='show_profile'),
    path('course/',views.course_selection,name='course_selection')
    ]