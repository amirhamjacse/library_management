from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "is_available",
            "created_by"
            ]
