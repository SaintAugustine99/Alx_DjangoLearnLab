from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # Register, login, logout, and profile URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),

    # Post CRUD URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

     #Comment URLs with the required structure
    path('post/<int:pk>/comments/new/', views.comment_create, name='comment_create'),

    # Comment URLs
    path('post/<int:post_id>/comments/new/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/update/', views.comment_edit, name='comment_update'),  # Alternative URL pointing to the same view
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # Tag URLs
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('search/', views.search_posts, name='search_posts'),
]