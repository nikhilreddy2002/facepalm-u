from django.shortcuts import render, redirect
from users import models as u_models
from . import models as p_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
        # image = data['image']
        new_post = p_models.Post(user_profile=user_profile, header=header, text=text,
                                 link=link, post_type=posttype, post_topic=posttopic)
        new_post.save()
        return redirect('feed')

    else:
        return render(request, 'post.html')


@login_required
def Feed(request):
    user = request.user
    user_profile = u_models.UserProfile.objects.get(user=request.user)
    user_posts = p_models.Post.objects.all().filter(user_profile=user_profile)

    # getting the timestamp of last log in by user
    login_timestamp = u_models.LoginLog.objects.get(user=user_profile)
    get_all_followers = ''' select user_following from users_following where user_follower = {}'''.format(
        user_profile)
    # all the users that this user follows
    following_accounts = tuple(
        u_models.Following.objects.raw(get_all_followers))
    # following account posts
    get_all_posts = '''select * from posts_post where (user_profile in {following_accounts}) and (timestamp between {last_logged_in} and {current_time}) order by timestamp'''.format(
        following_accounts=following_accounts, last_logged_in=login_timestamp, current_time=timezone.now())
    following_ppl_posts = p_models.Post.objects.raw(get_all_posts)
    return render(request, 'home.html', {'posts': user_posts})


'''
    TODO -->
    - check the last time user logged in
    - get todays date
    - get all the posts from all of the following accounts - order by date
    - fix the post page(html)
    - put reload button for new post updates
'''
