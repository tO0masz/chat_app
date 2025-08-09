from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friends, name='friends'),
    path('friends/accept/<str:username>/', views.accept_friendship, name='accept_friendship'),
    path('friends/reject/<str:username>/', views.reject_friendship, name='reject_friendship')
]