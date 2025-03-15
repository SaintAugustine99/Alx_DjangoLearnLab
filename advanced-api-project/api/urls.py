from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='books/update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='books/delete'),   
]

router = DefaultRouter()

router.register(r'books', views.BookViewSet)

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    # Add other custom API URLs here if needed
]