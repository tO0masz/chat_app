from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chat_home'),
    path('chat/create/', views.create_chat, name='create_chat')
]