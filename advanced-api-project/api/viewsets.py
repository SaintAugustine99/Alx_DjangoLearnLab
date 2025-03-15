from rest_framework import viewsets, permissions
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .permissions import IsOwnerOrReadOnly

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