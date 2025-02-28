# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView  # Import both views

urlpatterns = [
    # Function-based view URL
    path('books/', list_books, name='list_books'),

    # Class-based view URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]