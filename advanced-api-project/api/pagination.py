# In api/pagination.py
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    """
    Custom pagination for Book listings allowing flexible page sizes.
    
    Query Parameters:
    - page: Page number
    - page_size: Number of items per page (max 100)
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100