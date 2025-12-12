
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('searched/', views.searched, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('send-request/<int:user_id>/', views.send_friend_request, name='send_request'),

    path('accept/<int:friendship_id>/', views.accept_friend_request, name='accept_request'),
    path('reject/<int:friendship_id>/', views.reject_friend_request, name='reject_request'),
    path('cancel/<int:friendship_id>/', views.cancel_friend_request, name='cancel_request'),

    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),



]
