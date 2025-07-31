from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import Chat

@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-last_updated')
    return render(request, 'chat/index.html', {'chats':chats})

@login_required
def create_chat(request):
    pass
