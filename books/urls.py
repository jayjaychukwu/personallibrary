from django.urls import path

from .views import BookDetailAPIView, BookDetailsByISBNAPIView, BookListCreateAPIView

urlpatterns = [
    path("", BookListCreateAPIView.as_view(), name="book-list-create"),
    path("<int:pk>/", BookDetailAPIView.as_view(), name="book-detail"),
    path("book-details/<str:isbn>/", BookDetailsByISBNAPIView.as_view(), name="book_details_by_isbn"),
]
