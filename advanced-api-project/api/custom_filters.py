from rest_framework import filters
import re

class AdvancedSearchFilter(filters.BaseFilterBackend):
    """
    Custom filter backend that supports more complex search operations.
    
    For example, searching for books with exact phrases or excluding certain terms.
    Usage: ?advanced_search=exact:"Harry Potter" -Voldemort
    """
    def filter_queryset(self, request, queryset, view):
        advanced_search = request.query_params.get('advanced_search', None)
        if not advanced_search:
            return queryset
            
        # Process the advanced search query
        # Example implementation for exact phrase search
        exact_matches = re.findall(r'exact:"([^"]+)"', advanced_search)
        for phrase in exact_matches:
            queryset = queryset.filter(title__icontains=phrase)
            
        # Example implementation for excluding terms
        exclude_terms = re.findall(r'-(\w+)', advanced_search)
        for term in exclude_terms:
            queryset = queryset.exclude(title__icontains=term)
            
        return queryset