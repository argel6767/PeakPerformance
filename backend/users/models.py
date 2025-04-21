from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .managers import CustomUserManager
from django.core.exceptions import ValidationError
# Create your models here.

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def send_friend_request(self, to_user):
        """Send a friend request to another user"""
        # Check if there's already a rejected request in the opposite direction
        try:
            rejected_request = Friendship.objects.get(user=to_user, friend=self, status='rejected')
            # If found, delete the relation to update relationship direction
            rejected_request.delete()
        except Friendship.DoesNotExist:
            pass
            
        # Create the new request
        return Friendship.objects.update_or_create(user=self, friend=to_user, defaults={'status': 'pending'})

    def accept_friend_request(self, from_user):
        """Accept a friend request from another user"""
        # Update the incoming request
        Friendship.objects.filter(user=from_user, friend=self, status='pending').update(status='accepted')
        # Create the symmetric relationship
        return Friendship.objects.create(user=self, friend=from_user, status='accepted')

    def reject_friend_request(self, from_user):
        """Reject a friend request from another user"""
        Friendship.objects.filter(user=from_user, friend=self, status='pending').update(status='rejected')
    
    # will get all the relation of a user of a certain status
    def get_all_users_of_status_type(self, status):
        '''Get all friends of this user'''
        return Friendship.objects.filter(user=self, status=status)
    
    def unfriend_user(self, friend_user):
        """Remove a friendship with another user"""
        # Delete both directions of the relationship
        Friendship.objects.filter(user=self, friend=friend_user, status='accepted').delete()
        Friendship.objects.filter(user=friend_user, friend=self, status='accepted').delete()

class Friendship(models.Model):
    STATUS_CHOICES = ( # different states for relationships
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(CustomUser, related_name='friend', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friends_with', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'friend')
        ordering = ['created_at']

    # Prevent self-friendship
    def clean(self):
        if self.user == self.friend:
            raise ValidationError("Users cannot add themselves as friends.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class UserWeight(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_weight')
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['user','created_at']


class TwoFactorCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='two_factor_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reset_token')
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at