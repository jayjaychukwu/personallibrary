from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["user"]
