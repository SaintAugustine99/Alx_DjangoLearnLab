# query_samples.py

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    author = Author.objects.filter(name=author_name).first()
    if author:
        books = Book.objects.filter(author=author)
        return books
    return None

def list_books_in_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        books = library.books.all()
        return books
    return None

def retrieve_librarian_for_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        librarian = Librarian.objects.filter(library=library).first()
        return librarian
    return None

# Sample usage
if __name__ == "__main__":
    author_books = query_books_by_author("J.K. Rowling")
    print("Books by J.K. Rowling:", author_books)

    library_books = list_books_in_library("Central Library")
    print("Books in Central Library:", library_books)

    librarian = retrieve_librarian_for_library("Central Library")
    print("Librarian for Central Library:", librarian)