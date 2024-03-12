import json
from typing import Any, Dict, Union

import requests


class OpenLibrary:
    base_url = "https://openlibrary.org"

    @classmethod
    def parse_book_details(cls, data) -> Union[str, Dict[str, Any]]:
        num_found = data.get("num_found", 0)
        if num_found == 0:
            return "No book found"

        books = data.get("docs", [])
        book_details = []
        for book in books:
            title = book.get("title", "")
            author = ", ".join(book.get("author_name", []))
            publish_date = book.get("publish_date", [""])[0]
            isbn = book.get("isbn", [])

            book_details.append({"title": title, "author": author, "publish_date": publish_date, "isbn": isbn})

        return book_details

    @classmethod
    def fetch_book_details(cls, isbn: str):
        url = f"{cls.base_url}/search.json"
        params = {
            "isbn": isbn,
        }

        try:
            r = requests.get(
                url=url,
                params=params,
                timeout=30,
            )

            response = r.json()
            new_response = cls.parse_book_details(data=response)

            data = {
                "status": None,
                "data": new_response,
            }

            if isinstance(new_response, list):
                data["status"] = True
            else:
                data["status"] = False

            return data

        except requests.RequestException as err:
            return {
                "status": False,
                "message": "something went wrong",
                "error": str(err),
            }
