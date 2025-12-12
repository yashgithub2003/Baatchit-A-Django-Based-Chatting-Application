from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.db import models
from django.contrib.auth.decorators import login_required
from .models import Friendship
from django.db.models import Q
from .models import Friendship

@login_required
def home(request):
    user = request.user

    # All other users except current
    users = User.objects.exclude(id=user.id)

    # Accepted friendships
    friendships = Friendship.objects.filter(
        Q(sender=user) | Q(receiver=user),
        status='accepted'
    )

    # Friends list
    friends = []
    friend_ids = set()
    for f in friendships:
        friend_user = f.receiver if f.sender == user else f.sender
        friends.append(f)
        friend_ids.add(friend_user.id)

    # Pending requests
    received_requests = Friendship.objects.filter(receiver=user, status='sent')
    sent_requests = Friendship.objects.filter(sender=user, status='sent')

    # IDs for template quick lookup
    sent_ids = set(f.receiver.id for f in sent_requests)
    received_ids = set(f.sender.id for f in received_requests)

    # Optional: map received_requests by sender id
    received_requests_dict = {f.sender.id: f.id for f in received_requests}

    context = {
        'users': users,
        'friends': friends,
        'friend_ids': friend_ids,
        'received_requests': received_requests,
        'sent_requests': sent_requests,
        'sent_ids': sent_ids,
        'received_ids': received_ids,
        'received_requests_dict': received_requests_dict,
    }

    return render(request, 'accounts/accounts.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        return redirect('home')

    return render(request, 'accounts/register.html')
def user_logout(request):
    logout(request)
    return redirect('home')

def searched(request):
    query = request.GET.get('query')
    users = User.objects.filter(username__icontains=query)
    return render(request, 'accounts/accounts.html', {'users': users})





def dashboard(request):
    user = request.user

    friends = Friendship.objects.filter(
        (models.Q(sender=user) | models.Q(receiver=user)),
        status='accepted'
    )

    pending_requests = Friendship.objects.filter(
        receiver=user,
        status='sent'
    )

    context = {
        'friends': friends,
        'pending_requests': pending_requests,
    }
    return render(request, 'accounts/dashboard.html', context)


def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    sender = request.user

    if sender == receiver:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('home')

    # Check if request already exists
    if Friendship.objects.filter(sender=sender, receiver=receiver).exists() \
       or Friendship.objects.filter(sender=receiver, receiver=sender).exists():
        messages.info(request, "Friend request already exists.")
        return redirect('home')

    Friendship.objects.create(sender=sender, receiver=receiver, status='sent')
    messages.success(request, f"Friend request sent to {receiver.username}!")
    return redirect('home')

def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)

    if friendship.receiver != request.user:
        messages.error(request, "You are not authorized to accept this request.")
        return redirect('home')

    friendship.status = 'accepted'
    friendship.save()

    messages.success(request, "Friend request accepted!")
    return redirect('home')

def reject_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)

    if friendship.receiver != request.user:
        messages.error(request, "You are not authorized to reject this request.")
        return redirect('home')

    friendship.status = 'rejected'
    friendship.save()

    messages.info(request, "Friend request rejected.")
    return redirect('home')

def cancel_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)

    if friendship.sender != request.user:
        messages.error(request, "You cannot cancel this request.")
        return redirect('home')

    friendship.delete()
    messages.info(request, "Friend request cancelled.")
    return redirect('home')

def unfriend(request, user_id):
    user = request.user
    other = get_object_or_404(User, id=user_id)

    friendship = Friendship.objects.filter(
        Q(sender=user, receiver=other) |
        Q(sender=other, receiver=user),
        status='accepted'
    ).first()

    if friendship:
        friendship.delete()
        messages.success(request, f"You are no longer friends with {other.username}.")
    else:
        messages.info(request, "You are not friends.")

    return redirect('home')
