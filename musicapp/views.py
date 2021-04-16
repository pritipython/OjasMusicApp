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
    return render(request,'templates/list_songs_admin.html',context)

def add_songs(request):
    if request.method=='POST':
        form = AddSongForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/list_songs")
            except :
                pass
    else:
        form = AddSongForm()
    return render(request,'addsong.html',{'addsong':form})

def update_songs(request,id):
    update_song = Songs.objects.all(id=id)
    form =  AddSongForm(request.POST,isinstance = update_song)
    if form.is_valid():
        try:
            form.save()
            return redirect("/list_songs")
        except :
            pass
    return render(request,'updatesong.html',{'song_update':update_song})

def delete_songs(request,id):
    delete_song = Songs.objects.all(id=id)
    delete_song.delete()
    return redirect('/list_songs')

    
def index(request):
    return render(request,'base.html')
