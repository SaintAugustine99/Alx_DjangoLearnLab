from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book_data = {"title": "Test Book", "author": "Test Author"}
        self.update_data = {"title": "Updated Book"}
        self.book = Book.objects.create(**self.book_data)
        self.list_url = reverse("book-list")  # Assumes DRF router naming
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book.id})

    def test_create_book(self):
        response = self.client.post(self.list_url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        response = self.client.patch(self.detail_url, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


# Create your tests here.
