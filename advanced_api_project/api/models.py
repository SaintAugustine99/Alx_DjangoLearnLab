from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Author(models.Model):
    """
    Author model representing book authors.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with books (one author can have many books).
    """
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing books in the library.
    
    This model stores information about books including title, publication year,
    and the author (linking to the Author model via a foreign key relationship).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    def clean(self):
        """
        Custom validation to ensure publication_year is not in the future.
        """
        current_year = timezone.now().year
        if self.publication_year > current_year:
            raise ValidationError({'publication_year': 'Publication year cannot be in the future.'})