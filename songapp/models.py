from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Songs(models.Model):
 
    album_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    album_image_link = models.FileField(upload_to='./Album_Images')
    upload_file = models.FileField(upload_to='./Songs')
    year = models.IntegerField()
    singer = models.CharField(max_length=200)

    def __str__(self):
        return self.song_name

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = "Albums"


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.playlist_name