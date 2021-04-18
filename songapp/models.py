from django.db import models

# Create your models here.

class Songs(models.Model):
 
    album_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    album_image_link = models.FileField(upload_to='./Album_Images')
    upload_file = models.FileField(upload_to='./Songs')
    year = models.IntegerField()
    singer= models.CharField(max_length=200)

    def __str__(self):
        return self.album_name
    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = "Albums"
