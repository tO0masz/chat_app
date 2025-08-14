from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chat_home'),
    path('create/', views.create_chat, name='create_chat'),
    path('<int:chat_id>/messages/', views.get_messages, name='get_messages'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('search/', views.search_friends, name='search_friends'),
]