from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Book, Borrow
from .serializers import BookSerializer
from user_manages.permission import IsAdminUser
from datetime import timedelta
from django.utils import timezone


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


class BorrowBookAPIView(APIView):
    """
    API endpoint to borrow a book (Members Only).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        """
        Allows members to borrow a book if they haven't reached the borrow limit.
        """
        book = Book.objects.filter(id=book_id, is_available=True).first()

        if not book:
            return Response(
                {"detail": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already borrowed 5 books
        if Borrow.objects.filter(user=request.user, returned_at__isnull=True).count() >= 5:
            return Response(
                {"detail": "You can only borrow up to 5 books at a time."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new borrow record
        return_deadline = timezone.now() + timedelta(days=14)  # Set return deadline to 14 days from now
        borrow = Borrow.objects.create(
            book=book,
            user=request.user,
            return_deadline=return_deadline
        )

        # Mark the book as unavailable
        book.is_available = False
        book.save()

        return Response(
            BookSerializer(book).data, status=status.HTTP_201_CREATED)


class ReturnBookAPIView(APIView):
    """
    API endpoint to return a borrowed book (Members Only).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        """
        Allows members to return a borrowed book.
        """
        borrow = Borrow.objects.filter(
            book_id=book_id, user=request.user,
            returned_at__isnull=True).first()

        if not borrow:
            return Response(
                {"detail": "You have not borrowed this book."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the book as returned
        borrow.returned_at = timezone.now()
        borrow.save()

        # Calculate fine if overdue
        borrow.calculate_fine()

        # Mark the book as available again
        book = borrow.book
        book.is_available = True
        book.save()

        return Response(
            {"detail": "Book returned successfully.", "fine": borrow.fine}, status=status.HTTP_200_OK)


class BorrowedBooksAPIView(APIView):
    """
    API endpoint for members to view their borrowed books.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves all borrowed books for the logged-in user.
        """
        borrowed_books = Borrow.objects.filter(
            user=request.user, returned_at__isnull=True)
        response_data = []

        for borrow in borrowed_books:
            response_data.append({
                "book_title": borrow.book.title,
                "borrowed_at": borrow.borrowed_at,
                "return_deadline": borrow.return_deadline,
                "fine": borrow.calculate_fine()
            })

        return Response(response_data, status=status.HTTP_200_OK)


