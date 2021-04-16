from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

# is_staff is used to differencitate
@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def userdashboard(request):
    return render(request, 'userdashboard.html', {})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admindashboard(request):
    return render(request, 'admindashboard.html', {})