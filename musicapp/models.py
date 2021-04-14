from django.db import models

# Create your models here.

class Songs(models.Model):
 
    album_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    image_link = models.CharField(max_length=400)
    def __str__(self):
        return self.album_name
    class Meta:
        verbose_name = 'Album'
        Verbose_name_plural = "Albums