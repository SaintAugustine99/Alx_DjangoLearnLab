from django.db import models

# Create your models here.
# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Adds additional fields like bio, profile picture, and followers.
    """
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followed_by',
        blank=True
    )

    def follower_count(self):
        return self.followed_by.count()
    
    def following_count(self):
        return self.following.count()
    
    # Add timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Add a user to followers."""
        if user != self:
            self.following.add(user)
    
    def unfollow(self, user):
        """Remove a user from followers."""
        self.following.remove(user)
    
    def is_following(self, user):
        """Check if the user is following another user."""
        return user in self.following.all()
    
    @property
    def follower_count(self):
        """Return the number of followers."""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return the number of users being followed."""
        return self.following.count()