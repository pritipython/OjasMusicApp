from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from .forms import GeethUsersForm, RegistrationForm, UserLoginForm, PlaylistForm
from .models import GeethUsers, Songs, Playlist


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
            GeethUsers.objects.create(user=user, name=username, email=email)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
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
        user = authenticate(request, username=username, password=password)
        login(request, user)
        # messages.info(request, f"You are now logged in  as {user}")
        if user is not None:
            login(request, user)
            print(user)
            if request.user.is_staff:
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')
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
    return render(request, 'userdashboard.html', {})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admindashboard(request):
    return render(request, 'admindashboard.html', {})


@login_required(login_url='login')
@allowed_users(allowed_roles=['users', 'admin'])
def accountSettings(request):
    user = request.user.geethusers
    gform = GeethUsersForm(instance=user)
    if request.method == 'POST':
        gform = GeethUsersForm(request.POST, request.FILES, instance=user)
        if gform.is_valid():
            gform.save()
    context = {'gform': gform}
    return render(request, 'accountSettings.html', context)


def list_their_playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    print(playlists)
    context = {'playlists': playlists}
    return render(request, 'playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Songs.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'playlist_songs.html', context=context)


def list_their_playlist_to_add(request):
    play = Playlist.objects.filter(user=request.user).values('playlist_name').distinct()
    print(play)
    context = {'play': play}
    return render(request, 'list_their_playlist_to_add.html', context=context)

# def add_song_to_playlist(request):


def create_playlist(request):
    user = request.user
    form = PlaylistForm()
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'createplaylist.html', context=context)


def list_songs_user(request):
    list_songs = Songs.objects.all()
    context = {
        'song_list': list_songs
    }
    return render(request,  'list_songs_user.html', context)
