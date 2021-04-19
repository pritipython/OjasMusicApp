from verifyapp.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
import time
# Create your views here.

@login_required
def home(request):
    return render(request , 'home.html')

#General pages
def error(request):
    return render(request , 'error.html')

#login Pages
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/verifyapp/login')       
        profile_obj = Profile.objects.filter(user = user_obj ).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/verifyapp/login')
        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/verifyapp/login')        
        login(request , user)
        return redirect('/')
    return render(request , 'login.html')
# Login Page end block

## Registeration Block
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token,reset_token = '0')
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request , 'register.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/verifyapp/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/verifyapp/login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

## Registration end block


# Password reset
def password_reset_email(request):     
    return render(request,'password_reset_email.html')



def password_send(request):
    if request.method == "POST":
        email = request.POST['email']
        user_data = User.objects.get(email=email)
        profile = Profile.objects.get(user=user_data)
        token = str(uuid.uuid4())        
        profile.reset_token = token
        profile.save()
        send_mail_for_reset(email , token )  
        return redirect('password_reset',profile.id)
    return render(request,'password_send.html')

def send_mail_for_reset(email , token):
    subject = 'Reset Link for your '
    message = f'Hi paste the link to verify your account {token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)


def password_reset(request , id):   
    if request.method == "POST":
        code = request.POST['code']
        password = request.POST['password']
        personal = Profile.objects.get(id=id)
        if personal.reset_token == code:
            user_data = User.objects.get(email=personal.user.email)
            user_data.set_password(password)
            user_data.save()
            return redirect('password_confirm')
        else:
            return redirect('error')
    return render(request,'password_reset.html')

def password_confirm(request):
    messages.success(request, 'Your password hass been updated')
    return redirect('/verifyapp/login')
