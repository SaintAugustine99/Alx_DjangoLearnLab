# Retrieves the book you created
```python
from bookshelf.models import Book

# Retrieve the book you created
book = Book.objects.get(title="1984")
print(book)
# Expected Output: <Book: 1984>
