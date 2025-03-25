# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    
    # Profile management
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    
    # Follow/unfollow functionality
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow'),
    path('users/<int:user_id>/followers/', views.UserFollowersView.as_view(), name='followers'),
    path('users/<int:user_id>/following/', views.UserFollowingView.as_view(), name='following'),
]