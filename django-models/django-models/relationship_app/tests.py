from django.test import TestCase
from .models import Author, Book, Library, Librarian

class RelationshipAppTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Author One")
        self.book1 = Book.objects.create(title="Book One", author=self.author)
        self.book2 = Book.objects.create(title="Book Two", author=self.author)
        self.library = Library.objects.create(name="Library One")
        self.library.books.add(self.book1, self.book2)
        self.librarian = Librarian.objects.create(name="Librarian One", library=self.library)

    def test_books_by_author(self):
        books = Book.objects.filter(author=self.author)
        self.assertEqual(list(books), [self.book1, self.book2])

    def test_books_in_library(self):
        books = self.library.books.all()
        self.assertEqual(list(books), [self.book1, self.book2])

    def test_librarian_for_library(self):
        librarian = Librarian.objects.get(library=self.library)
        self.assertEqual(librarian, self.librarian)