from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . models import Chat, Message
from . forms import NewChatForm

@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-last_updated')
    return render(request, 'chat/index.html', {'chats':chats})

@login_required
def create_chat(request):
    if request.method == 'POST':
        form = NewChatForm(request.POST, user=request.user)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()
            # add self as participant
            participants = form.cleaned_data['participants']
            chat.participants.add(request.user, *participants)
            chat.save()
            return redirect('chat_home')
    form = NewChatForm(user=request.user)
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
