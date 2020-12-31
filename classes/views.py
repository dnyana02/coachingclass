from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import *
from .forms import  createUserForm,TeacherForm,TestinomialForm,ResultsliderForm,StudentForm,OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login,logout
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.core.mail import send_mail,send_mass_mail,BadHeaderError
from django.conf import settings
from django import forms
import urllib
import json
from .filters import YclassFilter

# Create your views here.
@allowed_users(allowed_roles = ['admin'])
@admin_only
def dashboard(request):
    contacts = Contact.objects.all()
    teachers = teacher.objects.all()
    testinomials = testinomial.objects.all()
    resultsliders = resultslider.objects.all()
   
    context = {'contacts' : contacts,'teachers': teachers,'testinomials':testinomials,'resultsliders':resultsliders}
    return render(request,'classes/dashboard.html',context)

@allowed_users(allowed_roles = ['admin'])
@admin_only
def dashboardstudent(request):
    student = Student.objects.all()
    myFilter = YclassFilter(request.GET, queryset = student)
    Students = myFilter.qs
    context = {'Students':Students,'myFilter':myFilter}
    return render(request,'classes/dashboardst.html',context)
    
def home(request):
    teachers = teacher.objects.all()
    resultsliders = resultslider.objects.all().order_by('id')[:3]
    testinomials = testinomial.objects.all().order_by('id')[:4]
    context = {'resultsliders':resultsliders, 'teachers' : teachers,'testinomials':testinomials}
    
    if request.method == 'POST':
         name = request.POST['name']
         email = request.POST['email']
         phone = request.POST['phone']
         yclass = request.POST['yclass']
         content = request.POST['content']
         if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)< 3 :
             messages.error(request,'Please fil the form correctly')
         else: 
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
                 contact = Contact(name=name,email=email,yclass= yclass,phone=phone,content=content)
                 contact.save()
                 message1 = (name + '  submitted contact form' , 'his phone no.- ' + phone + ' his email- '+ email + ' message from him - ' + content ,'rspatil0103@gmail.com',
              ['rspatil0103@gmail.com'])
                 message2 = ( 'We Welcome you to Knowledge coaching classes. ',
                'You will recieve our call shortly.',
                 'rspatil0103@gmail.com',
                 [email],)
                 send_mass_mail((message1,message2),fail_silently=False)
                 messages.success(request,'form filled  correctly')
            else:
                messages.error(request, 
                'Invalid reCAPTCHA. Please try again.')
                return redirect('')
    return render(request,'classes/index.html',context)


def registerpage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
                 user = form.save()
                 username = form.cleaned_data.get('username')  
                 messages.success(request,'Account was created for ' + username)
                 return redirect('login')
            else:
                messages.error(request, 
                'Invalid reCAPTCHA. Please try again.')
                return redirect('')
    context ={'form':form}
    return render(request,'classes/register.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username= username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
    

    context = {}
    return render(request,'classes/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@allowed_users(allowed_roles = ['admin'])
@admin_only
def updateteacher(request,pk):
	Teacher = teacher.objects.get(id=pk)
	form = TeacherForm(request.POST,instance=teacher)
	
	if request.method == 'POST':

		form = TeacherForm(request.POST, instance=Teacher)
		if form.is_valid():
			form.save()
			return redirect('dashboard')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)
@allowed_users(allowed_roles = ['admin'])
@admin_only
def updatetestinomial(request,pk):
	Testinomial = testinomial.objects.get(id=pk)
	form = TestinomialForm(request.POST,instance=testinomial)
	
	if request.method == 'POST':

		form = TestinomialForm(request.POST, instance=Testinomial)
		if form.is_valid():
			form.save()
			return redirect('dashboard')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)

@allowed_users(allowed_roles = ['admin'])
@admin_only
def updateresultslider(request,pk):
	Resultslider= resultslider.objects.get(id=pk)
	form = ResultsliderForm(request.POST,instance=resultslider)
	
	if request.method == 'POST':

		form = ResultsliderForm(request.POST, instance=Resultslider)
		if form.is_valid():
			form.save()
			return redirect('dashboard')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)



@allowed_users(allowed_roles = ['admin'])
@admin_only
def create_student(request):
	form = StudentForm(request.POST)
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('dashboardstudent')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)

@allowed_users(allowed_roles = ['admin'])
@admin_only
def updatestudent(request,pk):
	Students = Student.objects.get(sno=pk)
	form = StudentForm(request.POST,instance=Students)
	if request.method == 'POST':

		form = StudentForm(request.POST,instance=Students)
		if form.is_valid():
			form.save()
			return redirect('dashboardstudent')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)
    
def deleteStudent(request,pk):
    student = Student.objects.get(sno=pk)
    context={'item':student}
    if request.method == "POST":
        student.delete()
        return redirect('dashboardstudent')
    return render(request,'classes/delete.html',context)


