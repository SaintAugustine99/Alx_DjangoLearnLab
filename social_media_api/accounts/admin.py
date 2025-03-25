from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """Custom admin interface for User model."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'follower_count', 'following_count')
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('bio', 'profile_picture')}),
        ('Social Network', {'fields': ('followers',)}),
    )

admin.site.register(User, CustomUserAdmin)