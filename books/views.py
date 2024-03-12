from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Book
from .pagination import BookPagination
from .serializers import BookCreateEditSerializer, BookSerializer


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
        return Book.objects.filter(user=self.request.user)

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
        return Book.objects.filter(user=self.request.user)

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
