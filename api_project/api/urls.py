# api/urls.py
from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
]

# Creates a router and register our viewset with it

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Routes for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),

    # Includes the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
]