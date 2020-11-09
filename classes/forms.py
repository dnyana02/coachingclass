from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class TeacherForm(ModelForm):
    class Meta:
        model = teacher
        fields = ['name','education','subject','profile_pic']

class TestinomialForm(ModelForm):
    class Meta:
        model = testinomial
        fields = ['name','result','achive','written','test_pic']

class ResultsliderForm(ModelForm):
    class Meta:
        model = resultslider
        fields = ['yr','result_pic']