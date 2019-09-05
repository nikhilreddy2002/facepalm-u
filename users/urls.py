from django.contrib import admin
from django.urls import path
from . import views
from . import models
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
    path('register', views.Signup, name='signup'),
    path('profile', views.Profile, name='profile'),
    path('settings', views.Settings, name='settings')
] + staticfiles_urlpatterns()
