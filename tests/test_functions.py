import unittest
from unittest.mock import patch

from books.third_party import OpenLibrary


class TestOpenLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_data = {
            "num_found": 2,
            "docs": [
                {
                    "title": "Book 1",
                    "author_name": ["Author 1"],
                    "publish_date": ["2023-11-10"],
                    "isbn": ["1234567890"],
                },
                {
                    "title": "Book 2",
                    "author_name": ["Author 2"],
                    "publish_date": ["2023-11-11"],
                    "isbn": ["0987654321"],
                },
            ],
        }

    def test_parse_book_details_found(self):
        result = OpenLibrary.parse_book_details(self.mock_data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Book 1")
        self.assertEqual(result[1]["title"], "Book 2")

    def test_parse_book_details_not_found(self):
        data = {"num_found": 0}
        result = OpenLibrary.parse_book_details(data)
        self.assertEqual(result, "No book found")

    @patch("requests.get")
    def test_fetch_book_details_success(self, mock_get):
        mock_get.return_value.json.return_value = self.mock_data
        result = OpenLibrary.fetch_book_details("1234567890")
        self.assertTrue(result["status"])
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["title"], "Book 1")
        self.assertEqual(result["data"][1]["title"], "Book 2")


if __name__ == "__main__":
    unittest.main()
