from faker import Faker
from rest_framework.test import APITestCase

from accounts.models import User
from books.models import Book


class TestSetup(APITestCase):

    def setUp(self):
        self.fake = Faker()

        # Create a test user
        self.user_dict = {
            "username": self.fake.user_name(),
            "email": self.fake.email(),
            "password": self.fake.password(),
        }

        self.user = User.objects.create_user(**self.user_dict)

        # Create a test book
        self.book_dict = {
            "user": self.user,
            "title": "Test Book",
            "author": "Test Author",
            "ISBN": "1234567890",
            "publication_date": "2023-11-15",
        }

        self.book = Book.objects.create(**self.book_dict)
