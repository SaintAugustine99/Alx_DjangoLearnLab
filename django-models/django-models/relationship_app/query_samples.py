from django.shortcuts import get_object_or_404
from relationship_app.models import Author, Library

def query_books_by_author(author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.book_set.all()
    return books

def list_books_in_library(library_id):
    library = get_object_or_404(Library, id=library_id)
    books = library.books.all()
    return books

def retrieve_librarian_for_library(library_id):
    library = get_object_or_404(Library, id=library_id)
    librarian = library.librarian
    return librarian