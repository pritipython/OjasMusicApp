from django.shortcuts import render, redirect
from .forms import AddSongForm, playlistForm
from .models import Favourite, Playlist
from .models import Songs
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from musicapp.decorators import allowed_users
from django.core.paginator import Paginator
from django.contrib import messages


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def list_songs_admin(request):
    list_all_songs = Songs.objects.all()
    context = {
        'song_list': list_all_songs
    }
    return render(request, 'list_songs_admin.html', context)


"""
@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def list_songs_user(request):
    list_songs = Songs.objects.all()
    p = Paginator(list_songs, 6)
    page_number = request.GET.get('page')
    try:
        list_all_songs = p.get_page(page_number)
    except PageNotAnInteger:
        list_all_songs = p.page(1)
    except EmptyPage:
        list_all_songs = p.page(p.num_pages())
    context = {
        'song_list': list_all_songs
    }
    return render(request, 'list_songs_user.html', context)
"""


# list all songs good for convinent design
def list_songs_user(request):
    form = playlistForm(request.POST or None)   ##
    if request.method == 'POST':                ##
        print(form)                             ##use userdashboard view not this view
        if form.is_valid():   ##---------------------->##sita dont use this view use scrape it
            return redirect('createplaylist_addsong', playlistdata=request.POST['playlistname'], songiddata=request.POST['song'])
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct()
    list_songs = Songs.objects.all()
    p = Paginator(list_songs, 7)
    page_number = request.GET.get('page')
    try:
        list_all_songs = p.get_page(page_number)
    except PageNotAnInteger:
        list_all_songs = p.page(1)
    except EmptyPage:
        list_all_songs = p.page(p.num_pages())

    context = {
        'song_list': list_all_songs,
        'playlists': playlists,
        'form': form
    }
    return render(request, 'list_songs_user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users', 'admin'])
def search(request):        
    if request.method == 'GET': # this will be GET now
        songname = request.GET.get('search')    # do some research what it does
        status = Songs.objects.filter(song_name__icontains=songname) | Songs.objects.filter(album_name__icontains=songname)| Songs.objects.filter(singer__icontains=songname)
        return render(request, "search.html", {"songs": status})
    else:
        return render(request, "search.html", {})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_songs(request):
    form = AddSongForm()
    if request.method == "POST":
        form = AddSongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/list_songs_admin")
    context={'addsong': form}
    return render(request, 'addsong.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_songs(request, id):
    delete_song = Songs.objects.get(pk=id)
    delete_song.delete()
    return redirect('/list_songs_admin')


def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def album_view_songs(request, title):
    album_songs = Songs.objects.filter(Q(album_name__iexact=title))
    context = {
        'album_view': album_songs,
        'album_title': title
    }
        
    return render(request, 'album_view_songs.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def album_view(request):
    albums = (Songs.objects.values('album_name').distinct())
    list_albums = []
    dict_albums = {}
    for item in albums:
        list_albums.append(item['album_name'])
    for item in list_albums:
        qs = Songs.objects.raw('select * from songapp_Songs where album_name = %s LIMIT 1', [item])[0]
        if qs:
            dict_albums[qs.album_name] = qs.album_image_link.url
    print(dict_albums)
    context = {
        'album': dict_albums
    }
    return render(request, 'album_view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def favourite(request):
    myfav_songs = Songs.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    context = {
        'myfav_songs': myfav_songs
    }
    return render(request, 'list_myfavourite.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def add_favourite(request, id):
    song_add = Songs.objects.get(pk=id)
    songname = song_add.song_name
    checksongisfav = Favourite.objects.filter(user=request.user, song=song_add, is_fav=True)
    if checksongisfav:
        messages.warning(request, 'song "' + songname + '" is already in whishlist')
    else:
        add_fav = Favourite.objects.create(user=request.user, song=song_add, is_fav=True)
        add_fav.save()
        messages.success(request, 'song "' + songname + '" is successfully added to wishlist')
    return redirect('userdashboard')


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def delete_fav_songs(request, id):
    del_fav = Favourite.objects.filter(user=request.user, song__id=id)
    song_add = Songs.objects.get(pk=id)
    songname = song_add.song_name
    del_fav.delete()
    messages.success(request, 'song "'+songname+'" is sucessfully deleted from wishlist')
    return redirect('myfavourite')


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def addsong_to_playlist(request, playlist_name, song_id):   # add song to previously_created playlist
    song = Songs.objects.get(pk=song_id)
    filterdatatocheck = Playlist.objects.filter(user=request.user, playlist_name=playlist_name, song=song)
    songname = song.song_name
    if filterdatatocheck:
        messages.warning(request, 'your song "'+songname+'" is already in your selected playlist'+playlist_name)
    else:
        w = Playlist.objects.create(user=request.user, playlist_name=playlist_name, song=song)
        w.save()
        messages.success(request, 'your song "' + songname + '" is added succesfully added to playlist')
    return redirect("userdashboard")


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def createplaylist_addsong(request, playlistdata, songiddata):  # create new play list add song to that playlist
    s = Songs.objects.get(pk=songiddata)
    filterdatatocheck = Playlist.objects.filter(user=request.user, playlist_name=playlistdata)
    songname = s.song_name
    if filterdatatocheck:
        messages.warning(request, 'cannot create playlist because playlist "'+playlistdata+'" already present ')
        print("we", filterdatatocheck)
    else:
        e = Playlist.objects.create(user=request.user, playlist_name=playlistdata, song=s)
        e.save()
        messages.success(request, 'your song "'+songname+'" is added sucessfully added to playlist "' + playlistdata+'"')
    return redirect("userdashboard")


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def list_their_playlist(request):   # playlist of that particular user on listing data for only display
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct()
    print("list their playlists", playlists)
    context = {'playlists': playlists}
    return render(request, 'playlist.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def playlist_songs(request, playlist_name): # playlist song only for display
    songs = Songs.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()
    print(playlist_name)
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")
    context = {'playlist_name': playlist_name, 'songs': songs}
    return render(request, 'playlist_songs.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def delete_playlist(request, playlist_name):    # to delete entire playlist
    s = Playlist.objects.filter(user=request.user, playlist_name=playlist_name)
    print("delete", s)
    s.delete()
    messages.success(request, 'Your playlist "'+playlist_name+'" sucessfully deleted!')
    return redirect("playlist")