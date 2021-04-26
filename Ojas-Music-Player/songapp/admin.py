from django.contrib import admin

# Register your models here.
from .models import Songs,Favourite

admin.site.register(Songs)
admin.site.register(Favourite)
