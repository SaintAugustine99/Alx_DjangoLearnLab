from django.shortcuts import render

# Create your views here.

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow anyone to view the list of books

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Defines different permissions for different actions

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            # Allows anyone to view books
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # Only authenticated users can create books
            permission_classes = [IsAuthenticated]
        else:
            # Only admin users can update or delete books
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    



# Add documentation comments above your classes

"""
Authentication and Permissions in this API:

Token-based authentication is used to identify users.
To obtain a token, send a POST request to /api-token-auth/ with your username and password.

Permission structure:
- List and retrieve (GET): Available to all users, even unauthenticated ones
- Create (POST): Available only to authenticated users
- Update (PUT/PATCH) and Delete (DELETE): Available only to admin users

How to use authentication in requests:
1. Obtain token by sending POST to /api-token-auth/ with credentials
2. Include the token in your request headers as:
   Authorization: Token YOUR_TOKEN_HERE
"""