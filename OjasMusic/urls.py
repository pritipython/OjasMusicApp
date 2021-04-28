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
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from musicapp import views as mv
from songapp import views as sv


urlpatterns = [
    path('admin/', admin.site.urls),
    path("userdashboard/", mv.userdashboard, name="userdashboard"),
    path("admindashboard/", mv.admindashboard, name="admindashboard"),
    path('login/', mv.login_request, name='login'),
    path('signup/', mv.signup_request, name='signup'),
    path('logout/', mv.logout_request, name='logout'),
    path('settings/', mv.accountSettings, name='settings'),
    path('settings/', mv.accountSettings, name='settings'),
    path('token', mv.token_send, name="token_send"),
    path('success', mv.success, name='success'),
    path('verify/<auth_token>', mv.verify, name="verify"),
    path('error', mv.error, name="error"),
    path('password_reset/<int:id>', mv.password_reset, name="password_reset"),
    path('password_reset_email', mv.password_reset_email, name="password_reset_email"),
    path('password_send', mv.password_send, name="password_send"),
    path('password_confirm', mv.password_confirm, name="password_confirm"),

    path("", sv.index, name="index"),
    path('addsong', sv.add_songs, name="addsong"),
    path('list_songs', sv.list_songs_user, name="list_songs"),
    path('list_songs_admin', sv.list_songs_admin),
    path('delete/<int:id>', sv.delete_songs),
    path('album_view_songs/<slug:title>', sv.album_view_songs),
    path('album_view/', sv.album_view),
    path('myfavourite/', sv.favourite, name='myfavourite'),
    path('addfavourite/<int:id>', sv.add_favourite, name='addfavourite'),
    path('myfavourite/delete/<int:id>', sv.delete_fav_songs, name='deletefav'),
    path('search/', sv.search, name='search'),

    path('addsong_to_playlist/<str:playlist_name>/<int:song_id>/', sv.addsong_to_playlist, name='addsong_to_playlist'),
    path('createplaylist_addsong/<str:playlistdata>/<int:songiddata>/', sv.createplaylist_addsong, name='createplaylist_addsong'),
    path('playlist/', sv.list_their_playlist, name='playlist'),
    path('playlist_songs/<str:playlist_name>/', sv.playlist_songs, name='playlist_songs'),
    path('delete_playlist/<str:playlist_name>/', sv.delete_playlist, name='delete_playlist'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

