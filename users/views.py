from django.shortcuts import render, redirect
from . import models as u_models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def Login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("afakjfakjfakjlfas")
            # Redirect to a success page.
            return redirect('profile')
        else:
            print("crtfdcdfcdrfcdrfcdr")
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
            print(user.username)
            print(user_profile.profile_picture.url)
            return render(request, 'profile.html', {'User': user, 'UserProfile': user_profile})
    else:
        print("SO SAD")
        return render(request, 'login212.html')


def Settings(request):
    user = request.user
    user_id = user.id
    user_object = User.objects.get(id=user_id)
    if request.method == 'POST':
        data = request.POST

        if 'change_username' in data.keys():
            new_username = data['username']
            user_object.username = new_username
            user_object.save()
        if 'change_password' in data.keys():
            new_password = data['newpwd']
            new_password1 = data['newpwd1']
            if new_password == new_password1:
                old_password = data['oldpwd']
                if user_object.password == old_password:
                    new_password_hashed = make_password(new_password)
                    user_object.password = new_password_hashed
                    user_object.save()
                else:
                    return render(request, 'settings.html', {'password_error': 'Current password entered is wrong.'})
            else:
                return render(request, 'settings.html', {'password_error': 'Passwords dont match.'})
        if "deactivate_account" in data.keys():
            old_passworddeactiv = data['deactivate_password']
            if user_object.password == old_passworddeactiv:
                user_object.is_active = False
            else:
                return render(request, 'settings.html', {'error': 'Old Password'})
        if "delete_account" in data.keys():
            old_passworddelete = data['delete_password']
            if user_object.password = old_passworddelete:
                # delete acc
                pass
    else:
        return render(request, 'settings.html', {'User': user_object})
