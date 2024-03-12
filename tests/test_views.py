from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .test_setup import Book, TestSetup


class UserRegistrationAPIViewTestCase(TestSetup):
    def test_user_registration(self):
        # Define test user data
        user_data = {
            "username": self.fake.user_name(),
            "email": self.fake.email(),
            "password": self.fake.password(),
        }

        # Make a POST request to register a new user
        response = self.client.post(self.register_url, user_data, format="json")

        # Check if the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains the expected message and data
        self.assertEqual(response.data["message"], "user registered successfully")
        self.assertIn("access_token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])

        # Verify that the user was created in the database
        self.assertTrue(get_user_model().objects.filter(username=user_data["username"]).exists())


class BookListCreateAPIViewTestCase(TestSetup):

    def setUp(self):
        super().setUp()
        self.book_list_create_url = reverse("book-list-create")
        self.client.force_authenticate(user=self.user)

    def test_create_book(self):
        book_data = {
            "title": "Test Book 2",
            "author": "Test Author 2",
            "ISBN": "12234444212",
            "publication_date": "2023-11-10",
        }
        response = self.client.post(self.book_list_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Test Book 2").exists())

    def test_list_books(self):
        response = self.client.get(self.book_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDetailAPIViewTestCase(TestSetup):

    def setUp(self):
        super().setUp()
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book.id})
        self.client.force_authenticate(user=self.user)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        self.book_dict_copy = self.book_dict.copy()
        self.book_dict_copy["title"] = "Updated Book Title"
        self.book_dict_copy.pop("user")
        response = self.client.put(self.detail_url, self.book_dict_copy, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book Title")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


class BookDetailsByISBNAPIViewTestCase(TestSetup):
    def test_book_details_by_isbn(self):
        url = reverse("book_details_by_isbn", kwargs={"isbn": "9780375846670"})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
