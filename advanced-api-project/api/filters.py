# In api/filters.py
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model to allow filtering on multiple fields.
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    min_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author', 'min_year', 'max_year', 'author_name']