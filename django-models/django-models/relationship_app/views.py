from django.shortcuts import render
from .models import Author, Book, Library, Librarian

def author_books(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author)
    return render(request, 'relationship_app/author_books.html', {'author': author, 'books': books})

def library_books(request, library_id):
    library = Library.objects.get(id=library_id)
    books = library.books.all()
    return render(request, 'relationship_app/library_books.html', {'library': library, 'books': books})

def librarian_detail(request, library_id):
    library = Library.objects.get(id=library_id)
    librarian = Librarian.objects.get(library=library)
    return render(request, 'relationship_app/librarian_detail.html', {'library': library, 'librarian': librarian})