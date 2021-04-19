from django.shortcuts import render,redirect
from .forms import AddSongForm
from .models import Songs
from django.core.paginator import Paginator

# Create your views here.
from .models import Songs


def list_songs_admin(request):
    list_all_songs = Songs.objects.all()
    context={
        'song_list':list_all_songs
    }
    return render(request,'list_songs_admin.html',context)

def list_songs_user(request):
    list_songs = Songs.objects.all()
    p = Paginator(list_songs, 20)
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

def add_songs(request):
    form = AddSongForm()
    if request.method=="POST":
        form = AddSongForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/list_songs")
    context={'addsong':form}
    return render(request,'addsong.html',context)


def update_songs(request,id):
    update_song = Songs.objects.get(pk=id)
    form =  AddSongForm(request.POST,request.FILES,instance = update_song)
    print("---------------------------------------1",form)

    if form.is_valid():
        print("---------------------------------------2")
        form.save()
        return redirect("/list_songs")
    return render(request,'updatesong.html',{'song_update':update_song})

def delete_songs(request,id):
    delete_song = Songs.objects.get(pk=id)
    delete_song.delete()
    return redirect('/list_songs')

    
def index(request):
    return render(request,'base.html')

def all_songs(request):
    listall = Songs.objects.all()
    context={
        'song_list':listall
    }
    return render(request,'all_songs.html',context)
