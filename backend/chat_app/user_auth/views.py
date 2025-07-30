from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    if request.method == 'POST':
        return HttpResponse("Hello world")
    form = AuthenticationForm()
    return render(request, 'user_auth/login.html', {'form':form})