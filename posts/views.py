from django.shortcuts import render, redirect
from users import models as u_models
from . import models as p_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def Post(request):
    if request.method == 'POST':
        user = request.user
        user_id = user.id
        user_object = User.objects.get(id=user_id)
        user_profile = u_models.UserProfile.objects.get(user=user)
        data = request.POST
        posttype = data['posttype']
        posttopic = data['posttopic']
        text = data['text']
        header = data['header']
        link = data['link']
        #image = data['image']
        new_post = p_models.Post(user=user, header=header, text=text,
                                 link=link, post_type=posttype, post_topic=posttopic)
        new_post.save()
        return redirect('feed')

    else:
        return render(request, 'post.html')


@login_required
def Feed(request):
    return render(request, 'home.html')
