"""OjasMusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from musicapp import views as mv
from songapp import views as sv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', mv.login_request, name='login'),
    path('signup/', mv.signup_request, name='signup'),
    path('logout/', mv.logout_request, name='logout'),
    path("",sv.index),
    path('addsong',sv.add_songs),
    path('list_songs',sv.list_songs_user),
    path('list_songs_admin',sv.list_songs_admin),
    path('update/<int:id>',sv.update_songs),
    path('delete/<int:id>',sv.delete_songs),
    path('album_view_songs/<slug:title>',sv.album_view),
    path('album_view/',sv.album_view),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
