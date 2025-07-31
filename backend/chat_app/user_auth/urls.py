from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    path('logout/', views.logout, name='logout')
]