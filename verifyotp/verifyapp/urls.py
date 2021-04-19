from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('' ,  home  , name="home"),
    path('register' , register_attempt , name="register_attempt"),
    path('verifyapp/login/' , login_attempt , name="login_attempt"),
    path('token' , token_send , name="token_send"),
    path('success' , success , name='success'),
    path('verify/<auth_token>' , verify , name="verify"),
    path('error' , error , name="error"),   
    path('password_reset/<str:id>' , password_reset , name="password_reset"),
    path('password_reset_email' , password_reset_email , name="password_reset_email"),
    path('password_send' , password_send , name="password_send"),
    path('password_confirm' , password_confirm , name="password_confirm"),
]