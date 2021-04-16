from django.shortcuts import render

# Create your views here.
from .models import Songs
def list_songs(request):
    list_all_songs = Songs.objects.all()
    context={
        'song_list':list_all_songs
    }
    return render(request,'templates/list_songs_admin.html',context)

