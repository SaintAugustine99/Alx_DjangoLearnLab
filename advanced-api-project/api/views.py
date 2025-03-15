from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from .custom_filters import AdvancedSearchFilter
from .pagination import BookPagination

class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, 
                      filters.OrderingFilter, AdvancedSearchFilter]

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Generic views for Book model
class BookListView(generics.ListAPIView):
    """
    API endpoint that allows all books to be viewed.
    GET: Return a list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
     pagination_class = BookPagination

class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows a specific book to be viewed.
    GET: Return a specific book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    API endpoint that allows books to be created.
    POST: Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom method to handle the book creation process.
        This allows us to modify how the book is saved if needed.
        """
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint that allows a specific book to be updated.
    PUT: Update all fields of a book
    PATCH: Update partial fields of a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        """
        Custom method to handle the book update process.
        Validates data before saving.
        """
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint that allows a specific book to be deleted.
    DELETE: Remove a book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        """
        Custom method to handle the book deletion process.
        This allows us to perform additional actions before deletion if needed.
        """
        instance.delete()

        class BookListView(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed with filtering, searching, and ordering.
    
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