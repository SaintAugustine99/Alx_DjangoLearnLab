# Deletes the book instance
```python
from bookshelf.models import Book

# Delete the book instance
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Confirm the deletion
print(Book.objects.all())
# Expected Output: <QuerySet []>
