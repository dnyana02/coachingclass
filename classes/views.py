from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import *
from .forms import  createUserForm,TeacherForm,TestinomialForm,ResultsliderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login,logout
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.core.mail import send_mail,send_mass_mail,BadHeaderError
from django.conf import settings
from django import forms
# Create your views here.

@admin_only
def dashboard(request):
    contacts = Contact.objects.all()
    teachers = teacher.objects.all()
    testinomials = testinomial.objects.all()
    resultsliders = resultslider.objects.all()
    context = {'contacts' : contacts,'teachers': teachers,'testinomials':testinomials,'resultsliders':resultsliders}
    return render(request,'classes/dashboard.html',context)


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
             contact = Contact(name=name,email=email,yclass= yclass,phone=phone,content=content)
             contact.save()
             message1 = (name + '  submitted contact form' , 'his phone no.- ' + phone + ' his email- '+ email + ' message from him - ' + content ,'rspatil0103@gmail.com',
              ['rspatil0103@gmail.com'])
             message2 = ( 'We Welcome you to CRM. ',
                'You will recieve our call shortly.',
                 'rspatil0103@gmail.com',
                 [email],)
             send_mass_mail((message1,message2),fail_silently=False)
             messages.success(request,'form filled  correctly')
    return render(request,'classes/index.html',context)


def registerpage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')  
            messages.success(request,'Account was created for ' + username)
            return redirect('login')
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


def updateteacher(request,pk):
	Teacher = teacher.objects.get(id=pk)
	form = TeacherForm(request.POST,instance=teacher)
	
	if request.method == 'POST':

		form = TeacherForm(request.POST, instance=Teacher)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)
def updatetestinomial(request,pk):
	Testinomial = testinomial.objects.get(id=pk)
	form = TestinomialForm(request.POST,instance=testinomial)
	
	if request.method == 'POST':

		form = TestinomialForm(request.POST, instance=Testinomial)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)

def updateresultslider(request,pk):
	Resultslider= resultslider.objects.get(id=pk)
	form = ResultsliderForm(request.POST,instance=resultslider)
	
	if request.method == 'POST':

		form = ResultsliderForm(request.POST, instance=Resultslider)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'classes/order_form.html', context)