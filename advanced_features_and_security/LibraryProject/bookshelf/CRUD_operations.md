from bookshelf.models import Book

# Creates a Book instance
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
# Document in create.md
# Output: <Book: 1984>

# Retrieves and display all attributes of the book
book = Book.objects.get(title="1984")
print(book)
# Document in retrieve.md
# Output: <Book: 1984>

# Updates the title of the book
book.title = "Nineteen Eighty-Four"
book.save()
# Document in update.md
# Output: <Book: Nineteen Eighty-Four>

# Deletes the book instance
book.delete()
# Confirm the deletion
print(Book.objects.all())
# Document in delete.md
# Output: <QuerySet []>
