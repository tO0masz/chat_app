from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . models import Chat, Message
from . forms import NewChatForm
from django.contrib.auth.models import User
from user_auth.models import get_friends
from user_auth.models import get_friendship_requests_users

@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-last_updated')
    return render(request, 'chat/index.html', {'chats':chats})

@login_required
def create_chat(request, user_id=None):

    if user_id:
        user = User.objects.filter(id=user_id)
        form = NewChatForm(single_user=user)
    else:
        user = request.user
        form = NewChatForm(user=user)

    if request.method == 'POST':
        if user_id:
            form = NewChatForm(request.POST, single_user=user)
        else:
            form = NewChatForm(request.POST, user=user)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()
            # add self as participant
            participants = form.cleaned_data['participants']
            chat.participants.add(request.user, *participants)
            chat.save()
            return redirect('chat_home')
    return render(request, 'chat/new_chat.html', {'form':form})


@login_required
def chat_detail(request, chat_id):
    chat = Chat.objects.filter(id=chat_id, participants=request.user).first()
    if not chat:
        return HttpResponse("You don't have access to this chat")
    
    if request.method == 'POST' and 'message' in request.POST:
        message_content = request.POST['message'].strip()
        if message_content:
            Message.objects.create(
                content=message_content,
                chat=chat,
                sender=request.user
            )
            if request.headers.get('HX-Request'):
                return render(request, 'chat/partials/_messages.html', {'chat': chat})
            
    return render(request, 'chat/chat_detail.html', {'chat': chat})

@login_required
def get_messages(request, chat_id):
    chat = Chat.objects.filter(id=chat_id, participants=request.user).first()
    if not chat:
        return HttpResponse("Chat not found", status=404)
    return render(request, 'chat/partials/_messages.html', {'chat': chat})

@login_required
def search_friends(request):
    exclude_users = get_friends(request.user)
    invitations_users = get_friendship_requests_users(request.user)
    users = User.objects.exclude(id__in=exclude_users).exclude(id=request.user.id).exclude(id__in=invitations_users)
    search_query = request.GET.get('query', '').strip()
    if search_query:
        users = users.filter(username__icontains=search_query)
    return render(request, 'chat/search_friends.html', {'users': users})

@login_required
def delete_chat(request, chat_id):
    chat = Chat.objects.filter(id=chat_id).first()
    if chat:
        chat.delete()
    return redirect('chat_home')

@login_required
def edit_chat(request, chat_id):
    chat = Chat.objects.filter(id=chat_id).first()
    if request.method == 'POST':
        form = NewChatForm(request.POST, chat=chat)
        if form.is_valid():
            chat = form.save()
            return redirect('chat_home')
    form = NewChatForm(instance=chat, chat=Chat.objects.filter(id=chat_id).first())
    return render(request, 'chat/new_chat.html', {'form':form})