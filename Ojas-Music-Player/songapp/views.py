from django.shortcuts import render,redirect
from .forms import AddSongForm
from .models import Songs,Favourite
from django.core.paginator import Paginator

# Create your views here.
from .models import Songs
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from musicapp.decorators import unauthenticated_user, allowed_users

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def list_songs_admin(request):
    list_all_songs = Songs.objects.all()
    context={
        'song_list':list_all_songs
    }
    return render(request,'list_songs_admin.html',context)


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
    context={
        'song_list':list_all_songs
    }
    return render(request,'list_songs_user.html',context)

def search(request):        
    if request.method == 'GET': # this will be GET now      
        songname =  request.GET.get('search') # do some research what it does       
        status = Songs.objects.filter(song_name__icontains=songname) | Songs.objects.filter(album_name__icontains=songname)| Songs.objects.filter(singer__icontains=songname)
        return render(request,"search.html",{"songs":status})
    else:
        return render(request,"search.html",{})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_songs(request):
    form = AddSongForm()
    if request.method=="POST":
        form = AddSongForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/list_songs_admin")
    context={'addsong':form}
    return render(request,'addsong.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_songs(request,id):
    delete_song = Songs.objects.get(pk=id)
    delete_song.delete()
    return redirect('/list_songs_admin')
    
def index(request):
    return render(request,'index.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def album_view_songs(request,title):
    album_songs = Songs.objects.filter(Q(album_name__iexact=title))
    context={
        'album_view':album_songs
    }
        
    return render(request,'album_view_songs.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def album_view(request):
    albums = (Songs.objects.values('album_name').distinct())
    list_albums = []
    dict_albums = {}
    for item in albums:
        list_albums.append(item['album_name'])
    for item in list_albums:
        qs = Songs.objects.raw('select * from songapp_Songs where album_name = %s LIMIT 1',[item])[0]
        if qs:
            dict_albums[qs.album_name] = qs.album_image_link.url
    print(dict_albums)
    context = {
        'album':dict_albums
    }
    return render(request, 'album_view.html',context)

def favourite(request):
    myfav_songs = Songs.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    context = {
        'myfav_songs':myfav_songs
    }
    return render(request,'list_myfavourite.html',context)

def add_favourite(request,id):
    song_add = Songs.objects.get(pk=id)
    add_fav = Favourite.objects.create(user=request.user,song=song_add,is_fav=True)
    print(add_fav)
    return redirect('userdashboard')

def delete_fav_songs(request,id):
    del_fav = Favourite.objects.filter(user=request.user,song__id=id)
    del_fav.delete()
    return redirect('myfavourite')