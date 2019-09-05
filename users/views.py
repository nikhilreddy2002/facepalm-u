from django.shortcuts import render, redirect
from . import models as u_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def Login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            data = request.POST
            username = data['username']
            password = data['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                user = request.user
                user_id = user.id
                user_object = User.objects.get(id=user_id)
                user_profile = u_models.UserProfile.objects.get(user=user)
                if user_object.is_active == False:
                    user_object.is_active = True
                    user_object.save()
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
            user_profile_picture = u_models.UserProfilePicture(
                user=user_profile)
            user_profile_picture.save()
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
        else:
            user = request.user
            user_profile = u_models.UserProfile(user=user)
            user_profile_picture = u_models.UserProfilePicture(
                user=user_profile)
            user_profile_picture_url = user_profile_picture.image.url
            user_pp_clean = user_profile_picture_url[7:]
            print(user_profile_picture.user.user.username,
                  user_profile_picture.image.url)
            return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean})
    else:
        print("SO SAD")
        return render(request, 'login212.html')


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
                new_user = u_models.User.objects.get(username=new_username)
                if new_user is not None:
                    return render(request, 'settings.html', {"username_error": "Username already exists."})
            except:
                user_object.username = new_username
                user_object.save()

                return redirect('settings')
        if 'change_pp' in data.keys():
            print(request.POST)
            new_image = request.FILES.get('image', False)
            user_profile_picture = u_models.UserProfilePicture.objects.get(
                user=user_profile)
            user_profile_picture.image = new_image
            user_profile_picture.save()

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
<<<<<<< HEAD
                    return redirect('login')
=======
                    return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})
>>>>>>> c13ec540f0aeaf6cb5aa486749cbc66f7eb2dd5f
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
        user_profile = u_models.UserProfile(user=user)
        user_profile_picture = u_models.UserProfilePicture(
            user=user_profile)
        user_profile_picture_url = user_profile_picture.image.url
        user_pp_clean = user_profile_picture_url[7:]
        print(user_profile_picture.user.user.username,
              user_profile_picture.image.url)
        return render(request, 'settings.html', {'User': user, 'UserProfile': user_profile, 'UserProfilePictureurl': user_pp_clean})
