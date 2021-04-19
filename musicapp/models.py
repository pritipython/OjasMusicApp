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
