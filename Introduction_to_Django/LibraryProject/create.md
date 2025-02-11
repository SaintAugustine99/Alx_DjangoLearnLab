# Creates a Book instance
```python
from bookshelf.models import Book

# Creates a Book instance
book= Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.save()
print(book)
# Expected Output: <Book: 1984>
