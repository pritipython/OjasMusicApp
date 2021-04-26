from django.db import models
from django.contrib.auth.models import User


class GeethUsers(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phoneno = models.IntegerField(null=True)
    auth_token = models.CharField(max_length = 100)
    reset_token = models.CharField(max_length = 100)
    is_verified = models.BooleanField(default = False)
    profile_pic = models.ImageField(default="img.png", null=True, blank=True)

    def __str__(self):
        return self.name