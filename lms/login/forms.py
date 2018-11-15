from django import forms
from .models import professor_profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=(
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def clean_email(self):

        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        email_qset = User.objects.filter(email=email)

        if email_qset.exists() :
            raise forms.ValidationError('Email is taken already')
        return email

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get('confirm_password')

        if password!=confirm_password:
            raise forms.ValidationError('Passwords did not match')
        return confirm_password

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        user_qset = User.objects.filter(username=username)

        if user_qset.exists() :
            raise forms.ValidationError('User name is taken already')
        return username

class LoginForm(forms.Form):
    emailid = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        emailid = cleaned_data.get("emailid")
        email_set = User.objects.filter(email=emailid)

        if not email_set.exists():
            raise forms.ValidationError('Email is not registered')
            return emailid

class ProfileForm(forms.ModelForm):
    professor_description = forms.CharField(max_length=200,widget=forms.Textarea())
    professor_photo = forms.ImageField()
    class Meta:
        model=professor_profile
        fields=('professor_description',
                'professor_photo')
    def clean_professor_description(self):
        cleaned_data =super().clean()
        professor_description = cleaned_data.get('professor_description')
        return professor_description

class ResetForm(forms.ModelForm):
    email = forms.EmailField()
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email_set = User.objects.filter(email=email)

        if not email_set.exists():
            raise forms.ValidationError('Email is not registered')
        return email
