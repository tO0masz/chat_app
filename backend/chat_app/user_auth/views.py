from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import get_friends, Friendship

def home(request):
    if request.method == 'POST':
        username = username=request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_home')
        else:
            # TODO: implement login error, show some data that no user exist
            pass
    form = AuthenticationForm()
    return render(request, 'user_auth/login.html', {'form':form})

@login_required
def logout(request):
    user_logout(request)
    return redirect('login')

def register(request):
    content = {}
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
        except Exception as e:
            print(f"Error creating user: {e}")
            content['error'] = 'register_error'
    return render(request, 'user_auth/register.html', content)

@login_required
def profile(request):
    return render(request, 'user_auth/profile.html', {'user': request.user})

@login_required
def friends(request):
    friends = get_friends(request.user)
    invitations = Friendship.objects.filter(to_user=request.user, accepted=False)
    return render(request, 'user_auth/friends.html', {'friends': friends, 'invitations': invitations})

@login_required
def accept_friendship(request, username):
    user = User.objects.get(username=username)
    friendship = Friendship.objects.get(from_user=user, to_user=request.user)
    friendship.accepted = True
    friendship.save()
    return redirect('friends')

@login_required
def reject_friendship(request, username):
    user = User.objects.get(username=username)
    friendship = Friendship.objects.get(from_user=user, to_user=request.user)
    friendship.delete()
    return redirect('friends')

@login_required
def add_friendship(request, user_id):
    user = User.objects.get(id=user_id)
    Friendship.objects.create(from_user=request.user, to_user=user)
    return redirect('friends')