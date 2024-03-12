from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Book
from .pagination import BookPagination
from .serializers import BookCreateEditSerializer, BookDataSerializer, BookSerializer
from .third_party import OpenLibrary


class BookListCreateAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BookPagination
    serializer_classes = {
        "GET": BookSerializer,
        "POST": BookCreateEditSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).prefetch_related("user")

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_classes = {
        "GET": BookSerializer,
        "PUT": BookCreateEditSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Book.objects.filter(user=self.request.user).select_related("user")
        else:
            return Book.objects.none()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookDetailsByISBNAPIView(generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BookDataSerializer

    def get(self, request, isbn):
        book_details = OpenLibrary.fetch_book_details(isbn)
        if book_details.get("status"):
            return Response(book_details, status=status.HTTP_200_OK)
        else:
            return Response(book_details, status=status.HTTP_404_NOT_FOUND)
