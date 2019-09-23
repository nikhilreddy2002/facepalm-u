from django.shortcuts import render, redirect
from . import models as u_models
from posts import models as p_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
import urllib
# import urllib2
import json

# Create your views here.


def log_login(user):
    user_profile = u_models.UserProfile.objects.get(user=user)
    try:
        log_object = u_models.LoginLog.objects.get(user=user_profile)
        log_object.save()
    except:
        new = u_models.LoginLog(user=user_profile)
        new.save()


def Login(request):
    if request.user.is_authenticated:
        log_login(request.user)
        return redirect('profile')
    else:
        if request.method == 'POST':
            data = request.POST
            username = data['username']
            password = data['password']
            # print(username, password)
            user = authenticate(request, username=username, password=password)
            # print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                user = request.user
                user_id = user.id
                user_object = User.objects.get(id=user_id)
                user_profile = u_models.UserProfile.objects.get(user=user)
                log_login(user)
                if user_object.is_active == False:
                    user_object.is_active = True
                    user_object.save()
                    log_login(user)
                    return render(request, 'profile.html', {'data': 'Account has been reactivated'})
                else:
                    return redirect('profile')
            else:

                return redirect('login')
        else:
            return render(request, 'login212.html')


def Logout(request):
    logout(request)
    return redirect('login')


def Signup(request):
    if request.method == "POST":
        data = request.POST
        # reCAPTCHA
        '''    recaptcha_status = data['g-recaptcha-response']
            url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }'''
        '''data = urllib.urlencode(recaptcha_values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.load(response)'''
        username = data['username']
        email = data['email']
        password = data['password']
        password1 = data['password1']
        dob = data['dob']
        contact = data['contact']
        if password != password1:
            return render(request, 'signup.html', {'error': "Passwords Don’t Match"})
        else:
            password_hashed = make_password(password)
            user = u_models.User(username=username, password=password_hashed)
            user.save()
            user_profile = u_models.UserProfile(
                user=user, birth_date=dob, contact=contact)
            user_profile.save()
            return redirect('login')
    else:
        return render(request, 'signup.html')


def Profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'login' in request.POST.keys():
                return redirect('login')
            elif 'logout' in request.POST.keys():
                return redirect('logout')
            elif 'follow' or 'unfollow' in request.POST.keys():
                return redirect('profile')
        else:
            user = request.user
            user_profile = u_models.UserProfile.objects.get(user=user)
            user_profile_picture = user_profile.picture
            user_profile_picture_url = user_profile_picture.url
            user_pp_clean = user_profile_picture_url[7:]
            return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean})
    else:
        print("SO SAD")
        return render(request, 'login212.html')


def UserProfile(request, username):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(user=current_user)
        user = User.objects.get(username=username)
        followed_account = u_models.UserProfile.objects.get(user=user)
        print(logged_in_user.user.username,
              followed_account.user.username, current_user.username)
        '''
        - get the User model object using the username from the html
        - get the UserProfile object using the User object
        - create the new Following object
        - save it
        '''
        if username != current_user.username:
            if "follow" in data.keys():
                '''
                user_following is the logged in user
                user_follower is the followed account
                '''

                try:
                    person = u_models.Following.objects.get(
                        user_following=logged_in_user, user_follower=followed_account)
                except:
                    add_follower = u_models.Following(
                        user_following=logged_in_user, user_follower=followed_account)
                    add_follower.save()
                    return redirect('userprofile', username=username)
            elif "unfollow" in data.keys():
                u_models.Following.objects.filter(
                    user_following=logged_in_user, user_follower=followed_account
                ).delete()
                return redirect('userprofile', username=username)
        else:
            redirect('profile')
    else:
        current_user = request.user
        logged_in_user = u_models.UserProfile.objects.get(user=current_user)
        user = User.objects.get(username=username)
        user_profile = u_models.UserProfile.objects.get(user=user)
        user_profile_picture = user_profile.picture
        user_profile_picture_url = user_profile_picture.url
        user_pp_clean = user_profile_picture_url[7:]
        user_posts = p_models.Post.objects.all().filter(user_profile=user_profile)
        following = u_models.Following.objects.all().filter(
            user_following=logged_in_user, user_follower=user_profile)
        if following is None:
            return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean, 'posts': user_posts, 'following': ''})
        # print(user_post.user_profile.picture.url, user_pp_clean)
        return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean, 'posts': user_posts, 'following': following})


def Settings(request):
    user = request.user
    user_id = user.id
    user_object = User.objects.get(id=user_id)
    print(user_object.password)
    user_profile = u_models.UserProfile.objects.get(user=user)
    if request.method == 'POST':
        data = request.POST

        if 'change_username' in data.keys():
            new_username = data['username']
            try:
                new_user = u_models.UserProfile.objects.get(
                    username=new_username)
                if new_user is not None:
                    return render(request, 'settings.html', {"username_error": "Username already exists."})
            except:
                user_object.username = new_username
                user_object.save()

                return redirect('settings')
        if 'change_pp' in data.keys():
            print(request.POST)
            new_image = request.FILES.get('image', False)
            user_profile.picture = new_image
            user_profile.save()
            return redirect('settings')

        if 'change_password' in data.keys():
            new_password = data['newpwd']
            new_password1 = data['newpwd1']
            if new_password == new_password1:
                old_password = data['oldpwd']
                # print(new_password, new_password1, old_password)
                if check_password(old_password, user_object.password):
                    new_password_hashed = make_password(new_password)
                    user_object.password = new_password_hashed
                    user_object.save()
                    return redirect('login')
                    # return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})

                else:
                    return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})
            else:
                return render(request, 'settings.html', {'password_error': 'Passwords dont match.'})
        if "deactivate_account" in data.keys():
            old_passworddeactiv = data['deactivate_password']
            if check_password(old_password, user_object.password):
                user_object.is_active = False
                user_object.save()
                return redirect('login')
            else:
                return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})
        if "delete_account" in data.keys():
            old_passworddelete = data['delete_password']
            if user_object.password == old_passworddelete:
                user.delete()

    else:
        user = request.user
        user_profile = u_models.UserProfile.objects.get(user=user)
        user_profile_picture = user_profile.picture
        user_profile_picture_url = user_profile_picture.url
        user_pp_clean = user_profile_picture_url[7:]
        # print(user_profile_picture.user.user.username,user_profile_picture.image.url)
        return render(request, 'settings.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean})


def Search(request):
    if request.method == 'POST':
        data = request.POST
        search_username = data['search']
        get_all_usernames = 'select * from auth_user where username like "% {}"'.format(
            search_username)
        all_usernames = u_models.UserProfile.objects.raw(get_all_usernames)
        for search_results in all_usernames:
            print(search_results)

        '''
        userprofile --> user (Django User Model fkey)
        user
        select * from auth_user where username like '%{}'.format(search_username)
        
    
        '''
    else:
        return render(request, 'search.html')

    # facepalm0069@gmail.com
    # pwd=samshnik
    # https://www.freenom.com/en/freeandpaiddomains.html
