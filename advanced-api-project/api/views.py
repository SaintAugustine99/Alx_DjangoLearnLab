from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters, reverse 
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from .custom_filters import AdvancedSearchFilter
from .pagination import BookPagination
from django_filters import rest_framework
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
import json

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

class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """
    
    def setUp(self):
        """
        Set up test data and authenticate users before each test.
        """
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpassword', is_staff=True)
        
        # Create authentication tokens
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        
        # Set up API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # Define API URLs
        self.book_list_url = reverse('book-list')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.book_create_url = reverse('book-create')
        self.book_update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.book_delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})
        
    def test_get_book_list(self):
        """
        Test retrieving the list of books (unauthenticated).
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Assuming pagination is enabled
    
    def test_get_book_detail(self):
        """
        Test retrieving a specific book by ID (unauthenticated).
        """
        response = self.client.get(self.book_detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter and the Philosopher\'s Stone')
        self.assertEqual(response.data['publication_year'], 1997)
    
    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication (should fail).
        """
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication (should succeed).
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(title='New Test Book').publication_year, 2023)
    
    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication (should fail).
        """
        book_data = {
            'title': 'Updated Title',
            'publication_year': 2000,
            'author': self.author1.id
        }
        response = self.client.put(self.book_update_url(self.book1.id), book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book wasn't updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Philosopher\'s Stone')
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication (should succeed).
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        book_data = {
            'title': 'Updated Title',
            'publication_year': 2000,
            'author': self.author1.id
        }
        response = self.client.put(
            self.book_update_url(self.book1.id), 
            data=json.dumps(book_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify book was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        self.assertEqual(self.book1.publication_year, 2000)
    
    def test_partial_update_book(self):
        """
        Test partially updating a book with PATCH (should succeed).
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        book_data = {
            'title': 'Partially Updated Title'
        }
        response = self.client.patch(
            self.book_update_url(self.book1.id), 
            data=json.dumps(book_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only title was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.publication_year, 1997)  # Should remain unchanged
    
    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication (should fail).
        """
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify book wasn't deleted
        self.assertEqual(Book.objects.filter(id=self.book1.id).exists(), True)
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication (should succeed).
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted
        self.assertEqual(Book.objects.filter(id=self.book1.id).exists(), False)
    
    def test_filtering_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        url = f"{self.book_list_url}?publication_year=1997"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_filtering_by_year_range(self):
        """
        Test filtering books by publication year range.
        """
        url = f"{self.book_list_url}?min_year=1990&max_year=1997"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)
    
    def test_search_functionality(self):
        """
        Test searching for books.
        """
        url = f"{self.book_list_url}?search=Harry"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        url = f"{self.book_list_url}?search=1984"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
    
    def test_search_by_author_name(self):
        """
        Test searching for books by author name.
        """
        url = f"{self.book_list_url}?search=Rowling"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        url = f"{self.book_list_url}?search=Orwell"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        url = f"{self.book_list_url}?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], '1984')
    
    def test_ordering_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        """
        url = f"{self.book_list_url}?ordering=-title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_ordering_by_publication_year(self):
        """
        Test ordering books by publication year.
        """
        url = f"{self.book_list_url}?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['publication_year'], 1949)
        
        url = f"{self.book_list_url}?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['publication_year'], 1998)
    
    def test_combined_filtering_searching_ordering(self):
        """
        Test combining filtering, searching, and ordering.
        """
        url = f"{self.book_list_url}?search=Harry&min_year=1997&ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)
        self.assertEqual(response.data['results'][1]['publication_year'], 1998)
    
    def test_invalid_publication_year(self):
        """
        Test validation for invalid publication year (future date).
        """
        # This test assumes you have validation that prevents future publication years
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        future_year = 2030
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, book_data)
        
        # This should fail validation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_pagination(self):
        """
        Test that pagination works correctly.
        """
        # Create more books to test pagination
        for i in range(10):
            Book.objects.create(
                title=f'Test Book {i}',
                publication_year=2000 + i,
                author=self.author1
            )
        
        # Test first page (default page size should be 10)
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        
        # Test second page
        response = self.client.get(response.data['next'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 13 total books, so 3 on second page
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
        
        # Test custom page size
        url = f"{self.book_list_url}?page_size=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

class AuthorAPITestCase(APITestCase):
    """
    Test case for Author API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data and authenticate users before each test.
        """
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create authentication tokens
        self.user_token = Token.objects.create(user=self.user)
        
        # Set up API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the  Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        
        # Define API URLs
        self.author_list_url = reverse('author-list')
        self.author_detail_url = lambda pk: reverse('author-detail', kwargs={'pk': pk})
    
    def test_get_author_list(self):
        """
        Test retrieving the list of authors.
        """
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming no pagination for authors or adjust if paginated
    
    def test_get_author_detail(self):
        """
        Test retrieving a specific author with nested books.
        """
        response = self.client.get(self.author_detail_url(self.author1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        
        # Check that books are properly nested
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')
        self.assertEqual(response.data['books'][0]['publication_year'], 1997)

class BookViewSetTestCase(APITestCase):
    """
    Test case for BookViewSet endpoints.
    Tests all CRUD operations and filtering using the viewset URLs.
    """
    
    def setUp(self):
        """
        Set up test data and authenticate users before each test.
        """
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create authentication tokens
        self.user_token = Token.objects.create(user=self.user)
        
        # Set up API client
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Prisoner of Azkaban',
            publication_year=1999,
            author=self.author1
        )
        
        # Define API URLs - adjust these to match your actual viewset URLs
        self.books_viewset_url = '/api/books-viewset/'
        self.book_detail_viewset_url = lambda pk: f'/api/books-viewset/{pk}/'
    
    def test_list_books_viewset(self):
        """
        Test listing books through the viewset.
        """
        response = self.client.get(self.books_viewset_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)  # Assuming pagination
    
    def test_retrieve_book_viewset(self):
        """
        Test retrieving a specific book through the viewset.
        """
        response = self.client.get(self.book_detail_viewset_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter and the Prisoner of Azkaban')
    
    def test_create_book_viewset_unauthenticated(self):
        """
        Test creating a book through the viewset without authentication.
        """
        book_data = {
            'title': 'New ViewSet Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(self.books_viewset_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_viewset_authenticated(self):
        """
        Test creating a book through the viewset with authentication.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        book_data = {
            'title': 'New ViewSet Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(self.books_viewset_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(title='New ViewSet Book').count(), 1)
    
    def test_update_book_viewset(self):
        """
        Test updating a book through the viewset.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        book_data = {
            'title': 'Updated ViewSet Book',
            'publication_year': 2000,
            'author': self.author1.id
        }
        response = self.client.put(
            self.book_detail_viewset_url(self.book1.id),
            data=json.dumps(book_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated ViewSet Book')
    
    def test_delete_book_viewset(self):
        """
        Test deleting a book through the viewset.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.delete(self.book_detail_viewset_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.filter(id=self.book1.id).exists(), False)
    
    def test_filtering_viewset(self):
        """
        Test filtering books through the viewset.
        """
        # Add another book for testing filters
        Book.objects.create(
            title='Different Book',
            publication_year=2021,
            author=self.author1
        )
        
        # Test filtering by year
        url = f"{self.books_viewset_url}?publication_year=1999"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Prisoner of Azkaban')
        
        # Test filtering by title
        url = f"{self.books_viewset_url}?title=Different"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Different Book')

class AdvancedFeatureTestCase(APITestCase):
    """
    Test case for testing advanced features like custom actions
    in the ViewSet and other advanced functionality.
    """
    
    def setUp(self):
        """
        Set up test data for advanced feature testing.
        """
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
        # Create test data
        self.author = Author.objects.create(name='Isaac Asimov')
        
        # Create books from different years
        for year in range(2010, 2021):
            Book.objects.create(
                title=f'Book from {year}',
                publication_year=year,
                author=self.author
            )
        
        # URL for the by_year custom action (adjust if your endpoint is different)
        self.by_year_url = '/api/advanced-books/by_year/'
    
    def test_books_by_year_action(self):
        """
        Test the custom action to filter books by year.
        """
        # Test filtering for books from 2015
        url = f"{self.by_year_url}?year=2015"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2015)
        self.assertEqual(response.data[0]['title'], 'Book from 2015')
        
        # Test with invalid year parameter
        url = f"{self.by_year_url}?year=invalid"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test without year parameter
        response = self.client.get(self.by_year_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)