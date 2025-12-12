from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Friend Request Sent'),
        ('accepted', 'Friends'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    )

    sender = models.ForeignKey(
        User, 
        related_name='sent_friend_requests', 
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, 
        related_name='received_friend_requests', 
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='sent'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')  # ensure no duplicate friend requests

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
