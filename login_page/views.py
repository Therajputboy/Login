from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sessions.models import Session
from . import templates

def index(request):
    if request.session.has_key('is_logged'):
        return render(request, 'login_page/dashboard.html')
    else:
        return render(request,'login_page/index.html')

def register(request):
    if request.method == 'POST':
        message = ''
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request, 'User Created')
        else:
            messages.info(request,'Both password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'login_page/registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            request.session['is_logged'] = True
            request.session['username'] = username
            print(request.session.get_expiry_age())
            return render(request,'login_page/dashboard.html')
        else:
            messages.info(request,'Username and Password combination does not exist')
            return redirect('/')
    else:
        if request.session.has_key('is_logged'):
            return render(request,'login_page/dashboard.html')
        else:
            return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')

def forgot(request):
    if request.method == 'POST':
        subject = "Password Reset"
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            #print(user.email)
            recepient = user.email
            message = 'http://127.0.0.1:8000/reset_pass/' + username
            msg = EmailMessage(subject,message,"rksinghkatras1234@mail.com",[recepient])
            msg.content_subtype = 'html'
            msg.send()
            messages.info(request,'Please check your mail for the link')
            return redirect('index')
        else:
            messages.info(request,'Username does not exist')
            return redirect('forgot')
    else:
        return render(request,'login_page/forgot_pass.html')
def reset(request,username):
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        user = User.objects.get(username=username)
        if pass1 == pass2:
            user.set_password(pass1)
            #print(user.password)
            user.save()
            messages.info(request,'Password successfully reset.')
            return redirect('/')
        else:
            messages.info(request,'Both passwords should match.')
            return render(request,'login_page/reset_pass.html',{'username':username})
    else:
        return render(request,'login_page/reset_pass.html',{'username':username})