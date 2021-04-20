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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from musicapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("userdashboard/", views.userdashboard, name="userdashboard"),
    path("admindashboard/", views.admindashboard, name="admindashboard"),
    path('login/', views.login_request, name='login'),
    path('signup/', views.signup_request, name='signup'),
    path('logout/', views.logout_request, name='logout'),
    path('settings/', views.accountSettings, name='settings'),
    path('playlist/', views.list_their_playlist, name='playlist'),
    path('playlist/<str:playlist_name>/', views.playlist_songs, name='playlist_songs'),
    path('list/', views.list_songs_user, name='list'),
    path('create/', views.create_playlist, name='create'),
    path('show/', views.list_their_playlist_to_add, name='show'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)