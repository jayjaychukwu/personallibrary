from .test_setup import TestSetup


class BookModelTestCase(TestSetup):
    def test_book_creation(self):
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.ISBN, "1234567890")
        self.assertEqual(str(self.book.publication_date), "2023-11-15")

    def test_str_method(self):
        expected_str = "Test Book by Test Author"
        self.assertEqual(str(self.book), expected_str)
