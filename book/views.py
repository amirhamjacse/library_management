from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from user_manages.permission import IsAdminUser


class BookListCreateAPIView(APIView):
    """
    API endpoint for listing all books and adding a new book (Admin Only).
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["created_by"] = request.user.id
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """
    API endpoint for retrieving, updating, and deleting a book (Admin Only).
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    def get(self, request, book_id):
        book = self.get_object(book_id)
        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, book_id):
        book = self.get_object(book_id)
        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(
            book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = self.get_object(book_id)
        if not book:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(
            {"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
