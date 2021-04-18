from django.shortcuts import render,redirect
from .forms import AddSongForm
from .models import Songs

# Create your views here.
from .models import Songs
def list_songs(request):
    list_all_songs = Songs.objects.all()
    context={
        'song_list':list_all_songs
    }
    return render(request,'list_songs_admin.html',context)

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