from django.db import models
from django.contrib.auth.models import User


class GeethUsers(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phoneno = models.IntegerField(null=True)
    profile_pic = models.ImageField(default="img.png", null=True, blank=True)

    def __str__(self):
        return self.name


class Songs(models.Model):
    album_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    album_image_link = models.FileField(upload_to='./Album_Images/')
    upload_file = models.FileField(upload_to='./Songs/')
    year = models.IntegerField()
    singer = models.CharField(max_length=200)

    def __str__(self):
        return self.album_name

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = "Albums"