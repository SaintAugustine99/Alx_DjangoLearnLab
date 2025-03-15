from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import BookFilter

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model providing all CRUD operations.
    This is a more concise alternative to having separate views.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permission method that returns different permission classes
        based on the action being performed.
        """
        if self.action in ['list', 'retrieve']:
            # Allow anyone to view books
            permission_classes = [permissions.AllowAny]
        else:
            # Only authenticated users can create, update, or delete
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Custom method to handle book creation."""
        serializer.save()
        
    def perform_update(self, serializer):
        """Custom method to handle book updates."""
        serializer.save()

        class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model with filtering, searching, and ordering capabilities.
    
    Query Parameters:
    - Filtering: ?author=1&publication_year=2020&min_year=2000&max_year=2022&title=Harry&author_name=Rowling
    - Searching: ?search=Harry
    - Ordering: ?ordering=publication_year or ?ordering=-title (descending)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering