from django.shortcuts import render

# Create your views here
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, permissions, generics
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.services import create_like_notification, create_comment_notification

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user

class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        user = request.user
        
        # Check if the user already liked the post
        if Like.objects.filter(post=post, user=user).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create like
        serializer = LikeSerializer(
            data={"post": post.id},
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        like = serializer.save()
        
        # Create notification
        create_like_notification(like)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """Unlike a post"""
        post = self.get_object()
        user = request.user
        
        # Find and delete the like
        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        like.delete()
        return Response(
            {"detail": "Post unliked successfully."},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def likers(self, request, pk=None):
        """Get users who liked this post"""
        post = self.get_object()
        likes = Like.objects.filter(post=post)
        
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = LikeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        """
        Optionally filter comments by post
        """
        queryset = Comment.objects.all().order_by('-created_at')
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
        return queryset
    
    def perform_create(self, serializer):
        """Create comment and send notification"""
        comment = serializer.save(author=self.request.user)
        create_comment_notification(comment)
        return comment
    
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        """
        This view returns a list of all posts
        from users that the current user follows,
        ordered by newest first.
        """
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        
        # Get posts from followed users
        # Optionally include your own posts too
        return Post.objects.filter(
            Q(author__in=following_users) | Q(author=self.request.user)
        ).order_by('-created_at')
    
    #posts/views.py doesn't contain: ["Post.objects.filter(author__in=following_users).order_by"]
    