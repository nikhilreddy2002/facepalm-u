from django.contrib import admin
from django.urls import path
from . import views
from . import models
from django.contrib.auth.models import User
urlpatterns = [
    path('', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
    path('register', views.Signup, name='signup'),
    path('profile', views.Profile, name='profile'),
]
