from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required

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