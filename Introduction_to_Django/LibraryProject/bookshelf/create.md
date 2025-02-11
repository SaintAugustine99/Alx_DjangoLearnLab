# Creates a Book instance
```python
from bookshelf.models import Book

# Create a Book instance
book.objects.create(title="1984", author="George Orwell"  publication_year=1949)
book.objects.create
book.save()
print(book)
# Expected Output: <Book: 1984>
