from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the conversion of Book model instances to JSON
    and provides validation for the publication_year field.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        
        Args:
            value: The publication year to validate
            
        Returns:
            The validated value if valid
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer includes a nested representation of all books by this author,
    demonstrating how to handle one-to-many relationships in DRF. The books field
    uses the BookSerializer to serialize the related Book objects.
    """
    # Nested serializer for books by this author
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']