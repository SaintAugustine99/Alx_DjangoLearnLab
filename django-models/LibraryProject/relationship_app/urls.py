# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView  # Import both views

urlpatterns = [
    # Function-based view URL
    path('books/', list_books, name='list_books'),

    # Class-based view URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]

# relationship_app/urls.py
from django.urls import path
from .views import register, user_login, user_logout

urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]