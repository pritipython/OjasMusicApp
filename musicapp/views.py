from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from songapp.forms import playlistForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from musicapp.decorators import unauthenticated_user, allowed_users
from musicapp.forms import GeethUsersForm, RegistrationForm, UserLoginForm
from musicapp.models import GeethUsers
import uuid
from django.conf import settings
from django.core.mail import send_mail
from songapp.models import Songs
from django.core.paginator import Paginator
from songapp.models import Playlist


@unauthenticated_user
def signup_request(request):
    title = "Create Account"
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='users')
            user.groups.add(group)
            auth_token = str(uuid.uuid4())
            profile_obj = GeethUsers.objects.create(user=user, name=username, email=email,auth_token = auth_token)
            send_mail_after_registration(email, auth_token)
            profile_obj.save()
            return redirect('/token')
    else:
        form = RegistrationForm()
    context = {'form': form, 'title': title}
    return render(request, 'authentication/signup.html', context=context)


@unauthenticated_user
def login_request(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    context = {
        'form': form,
        'title': title,
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_obj = User.objects.filter(username = username).first()
        profile_obj = GeethUsers.objects.filter(user = user_obj ).first()
        if profile_obj.is_verified:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect('admindashboard')
                else:
                    return redirect('userdashboard')
        else:
            messages.success(request, 'email is not verified check your mail.')
            return redirect('login')
    else:
        print(form.errors)
    return render(request, 'authentication/login.html', context=context)


@login_required(login_url='login')
def logout_request(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def userdashboard(request):
    form = playlistForm(request.POST or None)
    if request.method == 'POST':
        print(form)
        if form.is_valid():
            return redirect('createplaylist_addsong', playlistdata=request.POST['playlistname'], songiddata=request.POST['song'])
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct()
    list_songs = Songs.objects.all()
    p = Paginator(list_songs, 6)
    page_number = request.GET.get('page')
    try:
        list_songs = p.get_page(page_number)
    except PageNotAnInteger:
        list_songs = p.page(1)
    except EmptyPage:
        list_songs = p.page(p.num_pages())
    context = {
        'song_list': list_songs,
        'playlists': playlists,
        'form': form
    }
    return render(request, 'list_songs_user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admindashboard(request):
    list_all_songs = Songs.objects.all()
    context = {
        'song_list': list_all_songs
    }
    return render(request, 'list_songs_admin.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users', 'admin'])
def accountSettings(request):
    user = request.user.geethusers
    gform = GeethUsersForm(instance=user)
    if request.method == 'POST':
        gform = GeethUsersForm(request.POST, request.FILES, instance=user)
        if gform.is_valid():
            gform.save()
            messages.success(request, "your account details updated sucessfully")
    context = {'gform': gform}
    return render(request, 'accountSettings.html', context)


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = GeethUsers.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')


# Registration end block
# Password reset
def password_reset_email(request):     
    return render(request, 'password_reset_email.html')


def password_send(request):
    if request.method == "POST":
        email = request.POST['email']
        profile = GeethUsers.objects.get(email=email)
        token = str(uuid.uuid4())        
        profile.reset_token = token
        send_mail_for_reset(email, token)
        profile.save()
        return redirect('password_reset', profile.id)
    return render(request, 'password_send.html')


def send_mail_for_reset(email, token):
    subject = 'Reset Code for your password '
    message = f'Hi please copy paste this link in to the browser {token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def password_reset(request, id):
    if request.method == "POST":
        code = request.POST['code']
        password = request.POST['password']
        personal = GeethUsers.objects.get(id=id)
        if personal.reset_token == code:
            user_data = User.objects.get(email=personal.user.email)
            user_data.set_password(password)
            user_data.save()
            return redirect('password_confirm')
        else:
            return redirect('error')
    return render(request, 'password_reset.html')


def password_confirm(request):
    messages.success(request, 'Your password has been updated')
    return redirect('login')


def error(request):
    return render(request, 'error.html')