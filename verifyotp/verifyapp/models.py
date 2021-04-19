from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    auth_token = models.CharField(max_length = 100)
    reset_token = models.CharField(max_length = 100)
    is_verified = models.BooleanField(default = False)
    time_stamp = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.user.username
    
