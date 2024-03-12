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


class BookDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    publish_date = serializers.CharField()
    isbn = serializers.ListField(child=serializers.CharField())
