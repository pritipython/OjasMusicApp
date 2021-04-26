from django.contrib import admin

# Register your models here.
from .models import Songs, Favourite, Playlist

admin.site.register(Songs)
admin.site.register(Favourite)
admin.site.register(Playlist)
