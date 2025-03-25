from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, permissions, generics
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q

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
    