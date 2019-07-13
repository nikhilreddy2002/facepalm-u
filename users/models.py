from django.db import models
from django.contrib.auth.models import User
# DJANGO USER MODEL :
# username
# first_name
# last_name
# password
# email
# is_staff
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    contact = models.IntegerField(unique=True, blank=False)
    likes = models.IntegerField(default=0)
    profile_picture = models.ImageField(
        upload_to='images', default='default.png')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user_following = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="follower_user")
    user_follower = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="following_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
